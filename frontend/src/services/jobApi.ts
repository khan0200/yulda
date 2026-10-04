import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type {
  JobCategory,
  JobContactMethod,
  JobEmploymentType,
  JobPayType,
  JobPost,
  JobPostStatus,
  JobPostType,
} from "@/types/job";

export interface ListJobsParams {
  post_type?: JobPostType;
  category?: JobCategory;
  employment_type?: JobEmploymentType;
  city?: string;
  requires_korean?: boolean;
  visa_sponsorship?: boolean;
  page?: number;
  page_size?: number;
}

export interface CreateJobPostPayload {
  post_type: JobPostType;
  category: JobCategory;
  employment_type: JobEmploymentType;
  title: string;
  description: string;
  pay_type?: JobPayType;
  pay_amount?: number;
  city?: string;
  location?: import("@/types/user").GeoPoint;
  requires_korean?: boolean;
  visa_sponsorship?: boolean;
  photos?: string[];
  contact_method: JobContactMethod;
  contact_value?: string;
}

export const jobApi = {
  async listPosts(params: ListJobsParams = {}): Promise<PaginatedData<JobPost>> {
    const { data } = await http.get<ApiResponse<PaginatedData<JobPost>>>("/jobs/posts", { params });
    return data.data;
  },

  async getPost(jobId: string): Promise<JobPost> {
    const { data } = await http.get<ApiResponse<JobPost>>(`/jobs/posts/${jobId}`);
    return data.data;
  },

  async createPost(payload: CreateJobPostPayload): Promise<JobPost> {
    const { data } = await http.post<ApiResponse<JobPost>>("/jobs/posts", payload);
    return data.data;
  },

  async deletePost(jobId: string): Promise<void> {
    await http.delete(`/jobs/posts/${jobId}`);
  },

  async markClosed(jobId: string): Promise<JobPost> {
    const { data } = await http.patch<ApiResponse<JobPost>>(`/jobs/posts/${jobId}`, { status: "CLOSED" });
    return data.data;
  },

  async listMine(page = 1, pageSize = 50): Promise<PaginatedData<JobPost>> {
    const { data } = await http.get<ApiResponse<PaginatedData<JobPost>>>("/jobs/posts/mine", {
      params: { page, page_size: pageSize },
    });
    return data.data;
  },

  async repost(jobId: string): Promise<JobPost> {
    const { data } = await http.post<ApiResponse<JobPost>>(`/jobs/posts/${jobId}/repost`);
    return data.data;
  },

  async updatePost(
    jobId: string,
    payload: Partial<{ title: string; description: string; pay_amount: number; status: JobPostStatus }>,
  ): Promise<JobPost> {
    const { data } = await http.patch<ApiResponse<JobPost>>(`/jobs/posts/${jobId}`, payload);
    return data.data;
  },
};
