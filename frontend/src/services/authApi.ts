import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";
import type { TokenPair, User, UserRole } from "@/types/user";

export interface SignupPayload {
  email: string;
  password: string;
  name: string;
  phone?: string;
  roles?: UserRole[];
  turnstile_token?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export const authApi = {
  async signup(payload: SignupPayload): Promise<TokenPair> {
    const { data } = await http.post<ApiResponse<TokenPair>>("/auth/signup", payload);
    return data.data;
  },

  async login(payload: LoginPayload): Promise<TokenPair> {
    const { data } = await http.post<ApiResponse<TokenPair>>("/auth/login", payload);
    return data.data;
  },

  async logout(): Promise<void> {
    await http.post("/auth/logout");
  },

  async me(): Promise<User> {
    const { data } = await http.get<ApiResponse<User>>("/auth/me");
    return data.data;
  },

  async forgotPassword(email: string): Promise<void> {
    await http.post("/auth/forgot-password", { email });
  },

  async resetPassword(token: string, newPassword: string): Promise<void> {
    await http.post("/auth/reset-password", { token, new_password: newPassword });
  },
};
