export type PlaceCountry = "KR" | "UZ" | "KZ" | "KG" | "TJ" | "TM" | "RU";

export interface Place {
  id: string;
  name: string;
  country: PlaceCountry;
  admin1: string | null;
  lat: number | null;
  lon: number | null;
  source: "SEED" | "USER";
  usage_count: number;
}
