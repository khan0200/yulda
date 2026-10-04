import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type { ServiceCategory, ServicePost, ServiceStatus } from "@/types/service";

export interface ListServicesParams {
  category?: ServiceCategory;
  city?: string;
  page?: number;
  page_size?: number;
}

export interface CreateServicePostPayload {
  category: ServiceCategory;
  title: string;
  description: string;
  price_note?: string;
  city?: string;
  location?: import("@/types/user").GeoPoint;
  photos?: string[];
  contact_value: string;
}

export const serviceApi = {
  async listPosts(params: ListServicesParams = {}): Promise<PaginatedData<ServicePost>> {
    const { data } = await http.get<ApiResponse<PaginatedData<ServicePost>>>("/services/posts", { params });
    return data.data;
  },

  async getPost(serviceId: string): Promise<ServicePost> {
    const { data } = await http.get<ApiResponse<ServicePost>>(`/services/posts/${serviceId}`);
    return data.data;
  },

  async createPost(payload: CreateServicePostPayload): Promise<ServicePost> {
    const { data } = await http.post<ApiResponse<ServicePost>>("/services/posts", payload);
    return data.data;
  },

  async deletePost(serviceId: string): Promise<void> {
    await http.delete(`/services/posts/${serviceId}`);
  },

  async markUnavailable(serviceId: string): Promise<ServicePost> {
    const { data } = await http.patch<ApiResponse<ServicePost>>(`/services/posts/${serviceId}`, {
      status: "UNAVAILABLE",
    });
    return data.data;
  },

  async listMine(page = 1, pageSize = 50): Promise<PaginatedData<ServicePost>> {
    const { data } = await http.get<ApiResponse<PaginatedData<ServicePost>>>("/services/posts/mine", {
      params: { page, page_size: pageSize },
    });
    return data.data;
  },

  async repost(serviceId: string): Promise<ServicePost> {
    const { data } = await http.post<ApiResponse<ServicePost>>(`/services/posts/${serviceId}/repost`);
    return data.data;
  },

  async updatePost(
    serviceId: string,
    payload: Partial<{ title: string; description: string; price_note: string; status: ServiceStatus }>,
  ): Promise<ServicePost> {
    const { data } = await http.patch<ApiResponse<ServicePost>>(`/services/posts/${serviceId}`, payload);
    return data.data;
  },
};
