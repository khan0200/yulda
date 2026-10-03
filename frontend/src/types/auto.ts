import type { GeoPoint } from "@/types/user";

export type AutoListingType = "SALE" | "RENTAL";
export type FuelType = "GASOLINE" | "DIESEL" | "LPG" | "HYBRID" | "ELECTRIC";
export type TransmissionType = "AUTOMATIC" | "MANUAL";
export type AutoListingStatus = "ACTIVE" | "RESERVED" | "SOLD" | "UNAVAILABLE";
export type BodyType =
  | "SEDAN"
  | "SUV"
  | "HATCHBACK"
  | "WAGON"
  | "MINIVAN"
  | "PICKUP"
  | "COUPE"
  | "CONVERTIBLE"
  | "VAN";
export type AccidentHistory = "NONE" | "MINOR" | "MAJOR";

export interface OwnerSummary {
  id: string;
  name: string;
  avatar: string | null;
}

export interface AutoListing {
  id: string;
  listing_type: AutoListingType;
  make: string;
  model: string;
  year: number;
  mileage_km: number;
  fuel_type: FuelType;
  transmission: TransmissionType;
  price: number;
  rental_price_per_day: number | null;
  description: string;
  photos: string[];
  city: string | null;
  location: GeoPoint | null;
  contact_value: string;
  status: AutoListingStatus;
  owner: OwnerSummary;
  created_at: string;
  updated_at: string;
  body_type: BodyType | null;
  color: string | null;
  accident_history: AccidentHistory | null;
  owner_count: number | null;
  credit_available: boolean;
}
