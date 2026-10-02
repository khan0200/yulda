import axios, { AxiosError } from "axios";
const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";
export const http = axios.create({ baseURL });
const ACCESS_TOKEN_KEY = "yulda_access_token";
const REFRESH_TOKEN_KEY = "yulda_refresh_token";
export function getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
}
export function getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
}
export function setTokens(tokens) {
    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
}
export function clearTokens() {
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
let refreshPromise = null;
async function refreshAccessToken() {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
        throw new Error("No refresh token available");
    }
    const response = await axios.post(`${baseURL}/auth/refresh`, {
        refresh_token: refreshToken,
    });
    setTokens(response.data.data);
    return response.data.data.access_token;
}
http.interceptors.response.use((response) => response, async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && originalRequest && !originalRequest._retry && getRefreshToken()) {
        originalRequest._retry = true;
        try {
            refreshPromise ??= refreshAccessToken();
            const newAccessToken = await refreshPromise;
            refreshPromise = null;
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return http(originalRequest);
        }
        catch (refreshError) {
            refreshPromise = null;
            clearTokens();
            window.location.href = "/login";
            return Promise.reject(refreshError);
        }
    }
    return Promise.reject(error);
});
