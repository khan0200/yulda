import axios from "axios";

import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";

export type UploadFolder = "marketplace" | "housing" | "auto" | "community";

interface PresignResponse {
  upload_url: string;
  public_url: string;
}

export const uploadApi = {
  async uploadFile(file: File, folder: UploadFolder): Promise<string> {
    const { data } = await http.post<ApiResponse<PresignResponse>>("/uploads/presign", {
      filename: file.name,
      content_type: file.type,
      folder,
    });

    const { upload_url, public_url } = data.data;

    // Direct-to-R2 upload, not through our backend — must bypass the shared
    // axios instance (no auth header, no baseURL) since this goes straight
    // to the storage endpoint with a presigned, pre-authorized URL.
    await axios.put(upload_url, file, {
      headers: { "Content-Type": file.type },
    });

    return public_url;
  },
};
