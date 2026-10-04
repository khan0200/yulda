import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type { AppNotification } from "@/types/notification";

export const notificationApi = {
  async list(page = 1, pageSize = 20): Promise<PaginatedData<AppNotification>> {
    const { data } = await http.get<ApiResponse<PaginatedData<AppNotification>>>("/notifications", {
      params: { page, page_size: pageSize },
    });
    return data.data;
  },

  async unreadCount(): Promise<number> {
    const { data } = await http.get<ApiResponse<{ unread_count: number }>>("/notifications/unread-count");
    return data.data.unread_count;
  },

  async markRead(id: string): Promise<AppNotification> {
    const { data } = await http.post<ApiResponse<AppNotification>>(`/notifications/${id}/read`);
    return data.data;
  },

  async markAllRead(): Promise<void> {
    await http.post("/notifications/read-all");
  },
};
