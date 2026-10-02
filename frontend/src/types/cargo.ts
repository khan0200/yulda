import type { OwnerSummary, RouteStop } from "@/types/route";

export type CargoPostType = "OFFER" | "REQUEST";
export type CargoStatus = "ACTIVE" | "EXPIRED";
export type CargoCategory =
  | "DOCUMENTS"
  | "MEDICINE"
  | "PERSONAL_ITEMS"
  | "FOOD"
  | "CLOTHING"
  | "ELECTRONICS"
  | "PHONE"
  | "LAPTOP"
  | "GAME_CONSOLE"
  | "PERFUME"
  | "OTHER";

export interface CargoPost {
  id: string;
  post_type: CargoPostType;
  stops: RouteStop[];
  departure_at: string;
  accepted_categories: CargoCategory[];
  rejected_categories: CargoCategory[];
  max_weight_kg: number | null;
  price_note: string | null;
  notes: string | null;
  contact_phone: string;
  status: CargoStatus;
  owner: OwnerSummary;
  created_at: string;
  updated_at: string;
}

export interface CargoSearchResult {
  items: CargoPost[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
  suggested_other_dates: CargoPost[];
}
