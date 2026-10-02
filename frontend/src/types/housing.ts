import type { GeoPoint } from "@/types/user";

export type HousingType = "ONE_ROOM" | "TWO_ROOM" | "ROOMMATE" | "APARTMENT" | "COMMERCIAL";
export type HousingAmenity = "FRIDGE" | "WASHER" | "AC" | "PARKING";
export type HousingStatus = "ACTIVE" | "RESERVED" | "RENTED";

export interface OwnerSummary {
  id: string;
  name: string;
  avatar: string | null;
}

export interface HousingListing {
  id: string;
  housing_type: HousingType;
  title: string;
  description: string;
  deposit: number;
  monthly_rent: number;
  maintenance_fee: number;
  amenities: HousingAmenity[];
  move_in_date: string | null;
  photos: string[];
  city: string | null;
  metro_station: string | null;
  location: GeoPoint | null;
  contact_value: string;
  status: HousingStatus;
  owner: OwnerSummary;
  created_at: string;
  updated_at: string;
}
