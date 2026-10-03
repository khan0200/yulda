import type { GeoPoint } from "@/types/user";

export type ListingCategory = "ELECTRONICS" | "FURNITURE" | "BIKES" | "CLOTHING" | "FOOD" | "FREE" | "OTHER";
export type ListingCondition = "NEW" | "USED";
export type ContactMethod = "PHONE" | "CHAT" | "KAKAOTALK";
export type ListingStatus = "ACTIVE" | "RESERVED" | "SOLD";

export interface SellerSummary {
  id: string;
  name: string;
  avatar: string | null;
}

export interface MarketplaceListing {
  id: string;
  category: ListingCategory;
  title: string;
  description: string;
  price: number;
  condition: ListingCondition;
  photos: string[];
  city: string | null;
  location: GeoPoint | null;
  contact_method: ContactMethod;
  contact_value: string;
  status: ListingStatus;
  seller: SellerSummary;
  created_at: string;
  updated_at: string;
  like_count: number;
}
