import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";
import type { RoutePost, RoutePostType, RouteSearchResult, RouteStop } from "@/types/route";

export interface SearchRoutesParams {
  post_type?: RoutePostType;
  from_city?: string;
  to_city?: string;
  date?: string;
  page?: number;
  page_size?: number;
}

export interface CreateRoutePostPayload {
  post_type: RoutePostType;
  stops: RouteStop[];
  departure_at: string;
  vehicle_info?: string;
  seats?: number;
  has_cargo_space?: boolean;
  price_note?: string;
  notes?: string;
  contact_phone: string;
}

export const routeApi = {
  async search(params: SearchRoutesParams = {}): Promise<RouteSearchResult> {
    const { data } = await http.get<ApiResponse<RouteSearchResult>>("/routes/search", { params });
    return data.data;
  },

  async getPost(postId: string): Promise<RoutePost> {
    const { data } = await http.get<ApiResponse<RoutePost>>(`/routes/${postId}`);
    return data.data;
  },

  async createPost(payload: CreateRoutePostPayload): Promise<RoutePost> {
    const { data } = await http.post<ApiResponse<RoutePost>>("/routes", payload);
    return data.data;
  },

  async deactivate(postId: string): Promise<RoutePost> {
    const { data } = await http.post<ApiResponse<RoutePost>>(`/routes/${postId}/deactivate`);
    return data.data;
  },

  async repost(postId: string, departureAt: string): Promise<RoutePost> {
    const { data } = await http.post<ApiResponse<RoutePost>>(`/routes/${postId}/repost`, {
      departure_at: departureAt,
    });
    return data.data;
  },

  async deletePost(postId: string): Promise<void> {
    await http.delete(`/routes/${postId}`);
  },
};
