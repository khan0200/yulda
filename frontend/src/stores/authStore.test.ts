import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { authApi } from "@/services/authApi";
import { clearTokens, getAccessToken, setTokens } from "@/services/http";
import { wsClient } from "@/services/wsClient";
import { useAuthStore } from "@/stores/authStore";
import { useConversationStore } from "@/stores/conversationStore";
import { useNotificationStore } from "@/stores/notificationStore";
import type { User } from "@/types/user";

vi.mock("@/services/authApi", () => ({
  authApi: {
    me: vi.fn(),
    signup: vi.fn(),
    login: vi.fn(),
    logout: vi.fn(),
  },
}));

vi.mock("@/services/http", () => ({
  getAccessToken: vi.fn(),
  setTokens: vi.fn(),
  clearTokens: vi.fn(),
}));

vi.mock("@/services/wsClient", () => ({
  wsClient: {
    connect: vi.fn(),
    disconnect: vi.fn(),
    on: vi.fn(() => () => {}),
  },
}));

function makeUser(overrides: Partial<User> = {}): User {
  return {
    id: "u1",
    email: "user@example.com",
    phone: null,
    name: "Test User",
    avatar: null,
    roles: ["CUSTOMER"],
    verification_status: "UNVERIFIED",
    location: null,
    is_banned: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    ...overrides,
  };
}

describe("authStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("fetchCurrentUser does nothing when there is no stored token", async () => {
    vi.mocked(getAccessToken).mockReturnValue(null);
    const store = useAuthStore();

    await store.fetchCurrentUser();

    expect(store.isInitialized).toBe(true);
    expect(store.user).toBeNull();
    expect(authApi.me).not.toHaveBeenCalled();
  });

  it("fetchCurrentUser loads the user and connects realtime when a token exists", async () => {
    vi.mocked(getAccessToken).mockReturnValue("token-123");
    vi.mocked(authApi.me).mockResolvedValueOnce(makeUser());
    const store = useAuthStore();

    await store.fetchCurrentUser();

    expect(store.user?.id).toBe("u1");
    expect(store.isAuthenticated).toBe(true);
    expect(store.isInitialized).toBe(true);
    expect(wsClient.connect).toHaveBeenCalledWith("token-123");
  });

  it("fetchCurrentUser clears tokens and user when /me fails (stale/invalid token)", async () => {
    vi.mocked(getAccessToken).mockReturnValue("stale-token");
    vi.mocked(authApi.me).mockRejectedValueOnce(new Error("401"));
    const store = useAuthStore();

    await store.fetchCurrentUser();

    expect(store.user).toBeNull();
    expect(clearTokens).toHaveBeenCalled();
  });

  it("signup stores tokens, loads the user, and connects realtime", async () => {
    vi.mocked(authApi.signup).mockResolvedValueOnce({
      access_token: "a",
      refresh_token: "r",
      token_type: "bearer",
    });
    vi.mocked(authApi.me).mockResolvedValueOnce(makeUser({ name: "New User" }));
    const store = useAuthStore();

    await store.signup({ email: "new@example.com", password: "StrongPass123", name: "New User" });

    expect(setTokens).toHaveBeenCalledWith({ access_token: "a", refresh_token: "r", token_type: "bearer" });
    expect(store.user?.name).toBe("New User");
    expect(wsClient.connect).toHaveBeenCalled();
  });

  it("login stores tokens and loads the user", async () => {
    vi.mocked(authApi.login).mockResolvedValueOnce({
      access_token: "a",
      refresh_token: "r",
      token_type: "bearer",
    });
    vi.mocked(authApi.me).mockResolvedValueOnce(makeUser());
    const store = useAuthStore();

    await store.login({ email: "user@example.com", password: "StrongPass123" });

    expect(store.isAuthenticated).toBe(true);
  });

  it("logout clears tokens, user, disconnects realtime, and resets dependent stores", async () => {
    vi.mocked(authApi.logout).mockResolvedValueOnce(undefined);
    const authStore = useAuthStore();
    authStore.setUser(makeUser());
    const notificationStore = useNotificationStore();
    const conversationStore = useConversationStore();
    const notificationResetSpy = vi.spyOn(notificationStore, "reset");
    const conversationResetSpy = vi.spyOn(conversationStore, "reset");

    await authStore.logout();

    expect(authStore.user).toBeNull();
    expect(clearTokens).toHaveBeenCalled();
    expect(wsClient.disconnect).toHaveBeenCalled();
    expect(notificationResetSpy).toHaveBeenCalled();
    expect(conversationResetSpy).toHaveBeenCalled();
  });

  it("logout still clears local state even if the API call fails", async () => {
    vi.mocked(authApi.logout).mockRejectedValueOnce(new Error("network error"));
    const store = useAuthStore();
    store.setUser(makeUser());

    await store.logout();

    expect(store.user).toBeNull();
    expect(clearTokens).toHaveBeenCalled();
  });

  it("hasRole checks the current user's roles", async () => {
    const store = useAuthStore();
    store.setUser(makeUser({ roles: ["CUSTOMER", "DRIVER"] }));

    expect(store.hasRole("DRIVER")).toBe(true);
    expect(store.hasRole("ADMIN")).toBe(false);
  });
});
