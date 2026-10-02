import { http } from "@/services/http";
import type { ApiResponse } from "@/types/api";
import type { Place, PlaceCountry } from "@/types/place";

export const placesApi = {
  async search(query: string, country?: PlaceCountry, limit = 8): Promise<Place[]> {
    const { data } = await http.get<ApiResponse<Place[]>>("/places/search", {
      params: { q: query, country, limit },
    });
    return data.data;
  },

  async learn(name: string, country: PlaceCountry): Promise<Place> {
    const { data } = await http.post<ApiResponse<Place>>("/places", { name, country });
    return data.data;
  },
};
