import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";
import type { CargoCategory, CargoPost, CargoPostType, CargoSearchResult } from "@/types/cargo";
import type { RouteStop } from "@/types/route";

export interface SearchCargoParams {
  post_type?: CargoPostType;
  from_city?: string;
  to_city?: string;
  date?: string;
  page?: number;
  page_size?: number;
}

export interface CreateCargoPostPayload {
  post_type: CargoPostType;
  stops: RouteStop[];
  departure_at: string;
  accepted_categories?: CargoCategory[];
  rejected_categories?: CargoCategory[];
  max_weight_kg?: number;
  price_note?: string;
  notes?: string;
  contact_phone: string;
}

export const cargoApi = {
  async search(params: SearchCargoParams = {}): Promise<CargoSearchResult> {
    const { data } = await http.get<ApiResponse<CargoSearchResult>>("/cargo/search", { params });
    return data.data;
  },

  async getPost(postId: string): Promise<CargoPost> {
    const { data } = await http.get<ApiResponse<CargoPost>>(`/cargo/${postId}`);
    return data.data;
  },

  async createPost(payload: CreateCargoPostPayload): Promise<CargoPost> {
    const { data } = await http.post<ApiResponse<CargoPost>>("/cargo", payload);
    return data.data;
  },

  async deactivate(postId: string): Promise<CargoPost> {
    const { data } = await http.post<ApiResponse<CargoPost>>(`/cargo/${postId}/deactivate`);
    return data.data;
  },

  async repost(postId: string, departureAt: string): Promise<CargoPost> {
    const { data } = await http.post<ApiResponse<CargoPost>>(`/cargo/${postId}/repost`, {
      departure_at: departureAt,
    });
    return data.data;
  },

  async deletePost(postId: string): Promise<void> {
    await http.delete(`/cargo/${postId}`);
  },
};
