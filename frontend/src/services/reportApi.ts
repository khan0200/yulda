import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";
import type { Report, ReportCreatePayload } from "@/types/report";

export const reportApi = {
  async create(payload: ReportCreatePayload): Promise<Report> {
    const { data } = await http.post<ApiResponse<Report>>("/reports", payload);
    return data.data;
  },
};
