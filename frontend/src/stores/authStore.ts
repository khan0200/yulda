import { computed, ref } from "vue";
import { defineStore } from "pinia";

import { authApi, type LoginPayload, type SignupPayload } from "@/services/authApi";
import { clearTokens, getAccessToken, setTokens } from "@/services/http";
import { wsClient } from "@/services/wsClient";
import { useConversationStore } from "@/stores/conversationStore";
import { useNotificationStore } from "@/stores/notificationStore";
import type { Message } from "@/types/conversation";
import type { AppNotification } from "@/types/notification";
import type { User } from "@/types/user";

let realtimeHandlersRegistered = false;

function connectRealtime(): void {
  const token = getAccessToken();
  if (!token) return;
  wsClient.connect(token);

  if (realtimeHandlersRegistered) return;
  realtimeHandlersRegistered = true;

  const notificationStore = useNotificationStore();
  const conversationStore = useConversationStore();

  wsClient.on("notification", (data) => {
    notificationStore.handleIncoming(data.notification as unknown as AppNotification);
  });

  wsClient.on("message", (data) => {
    const conversationId = data.conversation_id as string;
    const message = data.message as unknown as Message;
    const isActiveThread = window.location.pathname === `/messages/${conversationId}`;
    conversationStore.handleIncomingMessage(conversationId, message, isActiveThread);
  });
}

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const isInitialized = ref(false);

  const isAuthenticated = computed(() => Boolean(user.value));
  const roles = computed(() => user.value?.roles ?? []);

  function hasRole(role: string): boolean {
    return roles.value.includes(role as never);
  }

  async function fetchCurrentUser(): Promise<void> {
    if (!getAccessToken()) {
      isInitialized.value = true;
      return;
    }
    isLoading.value = true;
    try {
      user.value = await authApi.me();
      connectRealtime();
    } catch {
      clearTokens();
      user.value = null;
    } finally {
      isLoading.value = false;
      isInitialized.value = true;
    }
  }

  async function signup(payload: SignupPayload): Promise<void> {
    isLoading.value = true;
    try {
      const tokens = await authApi.signup(payload);
      setTokens(tokens);
      user.value = await authApi.me();
      connectRealtime();
    } finally {
      isLoading.value = false;
    }
  }

  async function login(payload: LoginPayload): Promise<void> {
    isLoading.value = true;
    try {
      const tokens = await authApi.login(payload);
      setTokens(tokens);
      user.value = await authApi.me();
      connectRealtime();
    } finally {
      isLoading.value = false;
    }
  }

  function clearSession(): void {
    clearTokens();
    user.value = null;
    wsClient.disconnect();
    useNotificationStore().reset();
    useConversationStore().reset();
  }

  async function logout(): Promise<void> {
    try {
      await authApi.logout();
    } catch {
      // Best-effort server-side logout — local state is cleared below
      // regardless, so a network failure here shouldn't block the user
      // from being logged out of the app.
    } finally {
      clearSession();
    }
  }

  function setUser(updated: User): void {
    user.value = updated;
  }

  return {
    user,
    isLoading,
    isInitialized,
    isAuthenticated,
    roles,
    hasRole,
    fetchCurrentUser,
    signup,
    login,
    logout,
    clearSession,
    setUser,
  };
});
