import type { GeoPoint } from "@/types/user";

export type HousingType = "ONE_ROOM" | "TWO_ROOM" | "ROOMMATE" | "APARTMENT" | "COMMERCIAL";
export type HousingAmenity =
  | "FRIDGE"
  | "WASHER"
  | "AC"
  | "PARKING"
  | "TV"
  | "WARDROBE"
  | "BED"
  | "DESK"
  | "SHOE_CABINET"
  | "INDUCTION"
  | "MICROWAVE"
  | "ELEVATOR"
  | "DIGITAL_LOCK"
  | "CCTV"
  | "BALCONY"
  | "VERANDA_EXPANSION"
  | "GAS_RANGE"
  | "INTERNET"
  | "PET_FRIENDLY"
  | "HEATING_FLOOR";
export type HousingStatus = "ACTIVE" | "RESERVED" | "RENTED";
export type HousingDirection =
  | "NORTH"
  | "NORTHEAST"
  | "EAST"
  | "SOUTHEAST"
  | "SOUTH"
  | "SOUTHWEST"
  | "WEST"
  | "NORTHWEST";

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
  area_m2: number | null;
  room_count: number | null;
  floor: number | null;
  total_floors: number | null;
  building_year: number | null;
  direction: HousingDirection | null;
}
