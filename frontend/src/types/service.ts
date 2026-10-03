import type { GeoPoint } from "@/types/user";

export type ServiceCategory =
  | "BEAUTY"
  | "REPAIR"
  | "TUTORING"
  | "CLEANING"
  | "MOVING"
  | "PET_CARE"
  | "PHOTOGRAPHY"
  | "DESIGN"
  | "TRANSLATION"
  | "LEGAL_ADMIN"
  | "EVENT"
  | "OTHER";
export type ServiceStatus = "ACTIVE" | "UNAVAILABLE";

export interface OwnerSummary {
  id: string;
  name: string;
  avatar: string | null;
}

export interface ServicePost {
  id: string;
  category: ServiceCategory;
  title: string;
  description: string;
  price_note: string | null;
  city: string | null;
  location: GeoPoint | null;
  photos: string[];
  contact_value: string;
  status: ServiceStatus;
  owner: OwnerSummary;
  like_count: number;
  created_at: string;
  updated_at: string;
}
