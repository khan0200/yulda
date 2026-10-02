import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type { AutoListing, AutoListingType, FuelType, TransmissionType } from "@/types/auto";

export interface ListAutoParams {
  listing_type?: AutoListingType;
  make?: string;
  fuel_type?: FuelType;
  transmission?: TransmissionType;
  city?: string;
  min_year?: number;
  max_year?: number;
  min_price?: number;
  max_price?: number;
  page?: number;
  page_size?: number;
}

export interface CreateAutoListingPayload {
  listing_type: AutoListingType;
  make: string;
  model: string;
  year: number;
  mileage_km: number;
  fuel_type: FuelType;
  transmission: TransmissionType;
  price: number;
  rental_price_per_day?: number;
  description: string;
  photos?: string[];
  city?: string;
  contact_value: string;
}

export const autoApi = {
  async listListings(params: ListAutoParams = {}): Promise<PaginatedData<AutoListing>> {
    const { data } = await http.get<ApiResponse<PaginatedData<AutoListing>>>("/auto/listings", { params });
    return data.data;
  },

  async getListing(listingId: string): Promise<AutoListing> {
    const { data } = await http.get<ApiResponse<AutoListing>>(`/auto/listings/${listingId}`);
    return data.data;
  },

  async createListing(payload: CreateAutoListingPayload): Promise<AutoListing> {
    const { data } = await http.post<ApiResponse<AutoListing>>("/auto/listings", payload);
    return data.data;
  },

  async deleteListing(listingId: string): Promise<void> {
    await http.delete(`/auto/listings/${listingId}`);
  },

  async markSold(listingId: string): Promise<AutoListing> {
    const { data } = await http.patch<ApiResponse<AutoListing>>(`/auto/listings/${listingId}`, { status: "SOLD" });
    return data.data;
  },
};
