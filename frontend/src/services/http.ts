import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";

import { useToastStore } from "@/stores/toastStore";
import type { ApiErrorBody } from "@/types/api";
import type { TokenPair } from "@/types/user";

const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export const http = axios.create({ baseURL });

declare module "axios" {
  export interface AxiosRequestConfig {
    /** Set true on a per-request basis to suppress the automatic error toast
     * (e.g. when the calling form already renders its own inline error). */
    skipErrorToast?: boolean;
  }
}

const ACCESS_TOKEN_KEY = "yulda_access_token";
const REFRESH_TOKEN_KEY = "yulda_refresh_token";

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setTokens(tokens: TokenPair): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
}

export function clearTokens(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

http.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let refreshPromise: Promise<string> | null = null;

async function refreshAccessToken(): Promise<string> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    throw new Error("No refresh token available");
  }
  const response = await axios.post<{ data: TokenPair }>(`${baseURL}/auth/refresh`, {
    refresh_token: refreshToken,
  });
  setTokens(response.data.data);
  return response.data.data.access_token;
}

http.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiErrorBody>) => {
    const originalRequest = error.config as (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined;

    if (error.response?.status === 401 && originalRequest && !originalRequest._retry && getRefreshToken()) {
      originalRequest._retry = true;
      try {
        refreshPromise ??= refreshAccessToken();
        const newAccessToken = await refreshPromise;
        refreshPromise = null;
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return http(originalRequest);
      } catch (refreshError) {
        refreshPromise = null;
        clearTokens();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    if (!originalRequest?.skipErrorToast && error.response?.status !== 401) {
      const message = error.response?.data?.message || "Something went wrong. Please try again.";
      useToastStore().error(message);
    }

    return Promise.reject(error);
  },
);
