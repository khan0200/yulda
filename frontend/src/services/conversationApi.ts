import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type { Conversation, ConversationListingType, Message } from "@/types/conversation";

export interface StartConversationPayload {
  target_user_id: string;
  listing_type?: ConversationListingType;
  listing_id?: string;
  listing_title?: string;
}

export const conversationApi = {
  async list(page = 1, pageSize = 20): Promise<PaginatedData<Conversation>> {
    const { data } = await http.get<ApiResponse<PaginatedData<Conversation>>>("/conversations", {
      params: { page, page_size: pageSize },
    });
    return data.data;
  },

  async start(payload: StartConversationPayload): Promise<Conversation> {
    const { data } = await http.post<ApiResponse<Conversation>>("/conversations", payload);
    return data.data;
  },

  async listMessages(conversationId: string, page = 1, pageSize = 50): Promise<PaginatedData<Message>> {
    const { data } = await http.get<ApiResponse<PaginatedData<Message>>>(
      `/conversations/${conversationId}/messages`,
      { params: { page, page_size: pageSize } },
    );
    return data.data;
  },

  async sendMessage(conversationId: string, body: string): Promise<Message> {
    const { data } = await http.post<ApiResponse<Message>>(`/conversations/${conversationId}/messages`, { body });
    return data.data;
  },

  async markRead(conversationId: string): Promise<void> {
    await http.post(`/conversations/${conversationId}/read`);
  },
};
