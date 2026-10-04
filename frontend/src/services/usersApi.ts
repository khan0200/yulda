import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";
import type { User } from "@/types/user";

export interface UpdateProfilePayload {
  name?: string;
  phone?: string;
  avatar?: string;
}

export interface ChangePasswordPayload {
  current_password: string;
  new_password: string;
}

export const usersApi = {
  async updateProfile(payload: UpdateProfilePayload): Promise<User> {
    const { data } = await http.patch<ApiResponse<User>>("/users/me", payload);
    return data.data;
  },

  async changePassword(payload: ChangePasswordPayload): Promise<void> {
    await http.post("/users/me/change-password", payload);
  },

  async deleteAccount(password: string): Promise<void> {
    await http.delete("/users/me", { data: { password } });
  },
};
