import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";
import type { BlockedUser } from "@/types/block";

export const blockApi = {
  async list(): Promise<BlockedUser[]> {
    const { data } = await http.get<ApiResponse<BlockedUser[]>>("/blocks");
    return data.data;
  },

  async block(blockedUserId: string): Promise<BlockedUser> {
    const { data } = await http.post<ApiResponse<BlockedUser>>("/blocks", { blocked_user_id: blockedUserId });
    return data.data;
  },

  async unblock(userId: string): Promise<void> {
    await http.delete(`/blocks/${userId}`);
  },
};
