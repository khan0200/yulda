export type RoutePostType = "OFFER" | "REQUEST";
export type RouteStatus = "ACTIVE" | "EXPIRED";

export interface RouteStop {
  name: string;
  country: string;
}

export interface OwnerSummary {
  id: string;
  name: string;
  avatar: string | null;
}

export interface RoutePost {
  id: string;
  post_type: RoutePostType;
  stops: RouteStop[];
  departure_at: string;
  vehicle_info: string | null;
  seats: number | null;
  has_cargo_space: boolean;
  price_note: string | null;
  notes: string | null;
  contact_phone: string;
  status: RouteStatus;
  owner: OwnerSummary;
  created_at: string;
  updated_at: string;
}

export interface RouteSearchResult {
  items: RoutePost[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
  suggested_other_dates: RoutePost[];
}
