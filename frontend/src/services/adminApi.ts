import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type { Report, ReportStatus } from "@/types/report";
import type { User } from "@/types/user";

export const adminApi = {
  async listUsers(search: string, page = 1, pageSize = 20): Promise<PaginatedData<User>> {
    const { data } = await http.get<ApiResponse<PaginatedData<User>>>("/admin/users", {
      params: { search: search || undefined, page, page_size: pageSize },
    });
    return data.data;
  },

  async banUser(userId: string): Promise<User> {
    const { data } = await http.post<ApiResponse<User>>(`/admin/users/${userId}/ban`);
    return data.data;
  },

  async unbanUser(userId: string): Promise<User> {
    const { data } = await http.post<ApiResponse<User>>(`/admin/users/${userId}/unban`);
    return data.data;
  },

  async removeContent(targetType: string, contentId: string): Promise<void> {
    await http.delete(`/admin/content/${targetType}/${contentId}`);
  },

  async listReports(status: ReportStatus | "", page = 1, pageSize = 20): Promise<PaginatedData<Report>> {
    const { data } = await http.get<ApiResponse<PaginatedData<Report>>>("/reports", {
      params: { status: status || undefined, page, page_size: pageSize },
    });
    return data.data;
  },

  async resolveReport(reportId: string, status: "RESOLVED" | "DISMISSED"): Promise<Report> {
    const { data } = await http.post<ApiResponse<Report>>(`/reports/${reportId}/resolve`, { status });
    return data.data;
  },
};
