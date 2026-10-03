import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type { HousingAmenity, HousingDirection, HousingListing, HousingType } from "@/types/housing";

export interface ListHousingParams {
  housing_type?: HousingType;
  city?: string;
  min_deposit?: number;
  max_deposit?: number;
  min_rent?: number;
  max_rent?: number;
  amenities?: HousingAmenity[];
  page?: number;
  page_size?: number;
}

export interface CreateHousingPayload {
  housing_type: HousingType;
  title: string;
  description: string;
  deposit: number;
  monthly_rent: number;
  maintenance_fee?: number;
  amenities?: HousingAmenity[];
  move_in_date?: string;
  photos?: string[];
  city?: string;
  metro_station?: string;
  location?: import("@/types/user").GeoPoint;
  contact_value: string;
  area_m2?: number;
  room_count?: number;
  floor?: number;
  total_floors?: number;
  building_year?: number;
  direction?: HousingDirection;
}

export const housingApi = {
  async listListings(params: ListHousingParams = {}): Promise<PaginatedData<HousingListing>> {
    const { data } = await http.get<ApiResponse<PaginatedData<HousingListing>>>("/housing/listings", {
      params,
      paramsSerializer: { indexes: null },
    });
    return data.data;
  },

  async getListing(listingId: string): Promise<HousingListing> {
    const { data } = await http.get<ApiResponse<HousingListing>>(`/housing/listings/${listingId}`);
    return data.data;
  },

  async createListing(payload: CreateHousingPayload): Promise<HousingListing> {
    const { data } = await http.post<ApiResponse<HousingListing>>("/housing/listings", payload);
    return data.data;
  },

  async deleteListing(listingId: string): Promise<void> {
    await http.delete(`/housing/listings/${listingId}`);
  },

  async markRented(listingId: string): Promise<HousingListing> {
    const { data } = await http.patch<ApiResponse<HousingListing>>(`/housing/listings/${listingId}`, {
      status: "RENTED",
    });
    return data.data;
  },
};
