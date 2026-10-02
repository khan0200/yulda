import { computed, ref } from "vue";
import { defineStore } from "pinia";

import { authApi, type LoginPayload, type SignupPayload } from "@/services/authApi";
import { clearTokens, getAccessToken, setTokens } from "@/services/http";
import type { User } from "@/types/user";

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
    } finally {
      isLoading.value = false;
    }
  }

  async function logout(): Promise<void> {
    try {
      await authApi.logout();
    } finally {
      clearTokens();
      user.value = null;
    }
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
  };
});
