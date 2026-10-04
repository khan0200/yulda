import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";
import type { CommunityPost } from "@/types/community";
import type { MarketplaceListing } from "@/types/marketplace";

export interface SearchResults {
  marketplace: MarketplaceListing[];
  community: CommunityPost[];
}

export const searchApi = {
  async search(query: string): Promise<SearchResults> {
    const { data } = await http.get<ApiResponse<SearchResults>>("/search", { params: { q: query } });
    return data.data;
  },
};
