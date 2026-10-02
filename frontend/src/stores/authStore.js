import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { authApi } from "@/services/authApi";
import { clearTokens, getAccessToken, setTokens } from "@/services/http";
export const useAuthStore = defineStore("auth", () => {
    const user = ref(null);
    const isLoading = ref(false);
    const isInitialized = ref(false);
    const isAuthenticated = computed(() => Boolean(user.value));
    const roles = computed(() => user.value?.roles ?? []);
    function hasRole(role) {
        return roles.value.includes(role);
    }
    async function fetchCurrentUser() {
        if (!getAccessToken()) {
            isInitialized.value = true;
            return;
        }
        isLoading.value = true;
        try {
            user.value = await authApi.me();
        }
        catch {
            clearTokens();
            user.value = null;
        }
        finally {
            isLoading.value = false;
            isInitialized.value = true;
        }
    }
    async function signup(payload) {
        isLoading.value = true;
        try {
            const tokens = await authApi.signup(payload);
            setTokens(tokens);
            user.value = await authApi.me();
        }
        finally {
            isLoading.value = false;
        }
    }
    async function login(payload) {
        isLoading.value = true;
        try {
            const tokens = await authApi.login(payload);
            setTokens(tokens);
            user.value = await authApi.me();
        }
        finally {
            isLoading.value = false;
        }
    }
    async function logout() {
        try {
            await authApi.logout();
        }
        finally {
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
