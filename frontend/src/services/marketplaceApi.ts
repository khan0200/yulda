import { http } from "@/services/http";
import type { ApiResponse, PaginatedData } from "@/types/api";
import type { ContactMethod, ListingCategory, ListingCondition, MarketplaceListing } from "@/types/marketplace";

export interface ListListingsParams {
  category?: ListingCategory;
  city?: string;
  condition?: ListingCondition;
  min_price?: number;
  max_price?: number;
  page?: number;
  page_size?: number;
}

export interface CreateListingPayload {
  category: ListingCategory;
  title: string;
  description: string;
  price: number;
  condition: ListingCondition;
  photos?: string[];
  city?: string;
  location?: import("@/types/user").GeoPoint;
  contact_method: ContactMethod;
  contact_value: string;
}

export const marketplaceApi = {
  async listListings(params: ListListingsParams = {}): Promise<PaginatedData<MarketplaceListing>> {
    const { data } = await http.get<ApiResponse<PaginatedData<MarketplaceListing>>>("/marketplace/listings", { params });
    return data.data;
  },

  async getListing(listingId: string): Promise<MarketplaceListing> {
    const { data } = await http.get<ApiResponse<MarketplaceListing>>(`/marketplace/listings/${listingId}`);
    return data.data;
  },

  async createListing(payload: CreateListingPayload): Promise<MarketplaceListing> {
    const { data } = await http.post<ApiResponse<MarketplaceListing>>("/marketplace/listings", payload);
    return data.data;
  },

  async deleteListing(listingId: string): Promise<void> {
    await http.delete(`/marketplace/listings/${listingId}`);
  },

  async markSold(listingId: string): Promise<MarketplaceListing> {
    const { data } = await http.patch<ApiResponse<MarketplaceListing>>(`/marketplace/listings/${listingId}`, {
      status: "SOLD",
    });
    return data.data;
  },
};
