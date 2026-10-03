import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";

export type FavoriteTargetType = "MARKETPLACE" | "COMMUNITY" | "JOBS" | "SERVICES";

export interface ToggleFavoriteResult {
  is_favorited: boolean;
  like_count: number;
}

export const favoriteApi = {
  async toggle(targetType: FavoriteTargetType, targetId: string): Promise<ToggleFavoriteResult> {
    const { data } = await http.post<ApiResponse<ToggleFavoriteResult>>(
      `/favorites/${targetType}/${targetId}/toggle`,
    );
    return data.data;
  },

  async listMine(targetType: FavoriteTargetType): Promise<string[]> {
    const { data } = await http.get<ApiResponse<string[]>>(`/favorites/${targetType}/mine`);
    return data.data;
  },
};
