import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type { CommunityComment, CommunityPost, PostCategory } from "@/types/community";

export interface ListPostsParams {
  category?: PostCategory;
  city?: string;
  page?: number;
  page_size?: number;
}

export interface CreatePostPayload {
  category: PostCategory;
  title: string;
  body: string;
  photos?: string[];
  city?: string;
}

export interface CreateCommentPayload {
  body: string;
}

export const communityApi = {
  async listPosts(params: ListPostsParams = {}): Promise<PaginatedData<CommunityPost>> {
    const { data } = await http.get<ApiResponse<PaginatedData<CommunityPost>>>("/community/posts", { params });
    return data.data;
  },

  async getPost(postId: string): Promise<CommunityPost> {
    const { data } = await http.get<ApiResponse<CommunityPost>>(`/community/posts/${postId}`);
    return data.data;
  },

  async createPost(payload: CreatePostPayload): Promise<CommunityPost> {
    const { data } = await http.post<ApiResponse<CommunityPost>>("/community/posts", payload);
    return data.data;
  },

  async deletePost(postId: string): Promise<void> {
    await http.delete(`/community/posts/${postId}`);
  },

  async listComments(postId: string, page = 1, pageSize = 50): Promise<PaginatedData<CommunityComment>> {
    const { data } = await http.get<ApiResponse<PaginatedData<CommunityComment>>>(
      `/community/posts/${postId}/comments`,
      { params: { page, page_size: pageSize } },
    );
    return data.data;
  },

  async addComment(postId: string, payload: CreateCommentPayload): Promise<CommunityComment> {
    const { data } = await http.post<ApiResponse<CommunityComment>>(`/community/posts/${postId}/comments`, payload);
    return data.data;
  },
};
