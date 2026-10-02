export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string | null;
}

export interface ApiErrorBody {
  success: false;
  error_code: string;
  message: string;
  details?: unknown;
}

export interface PaginatedData<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}
