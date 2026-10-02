export type UserRole =
  | "CUSTOMER"
  | "DRIVER"
  | "COURIER"
  | "EMPLOYER"
  | "WORKER"
  | "SERVICE_PROVIDER"
  | "BUSINESS"
  | "ADMIN";

export type VerificationStatus = "UNVERIFIED" | "PENDING" | "VERIFIED" | "REJECTED";

export interface GeoPoint {
  type: "Point";
  coordinates: [number, number];
}

export interface User {
  id: string;
  email: string;
  phone: string | null;
  name: string;
  avatar: string | null;
  roles: UserRole[];
  verification_status: VerificationStatus;
  location: GeoPoint | null;
  created_at: string;
  updated_at: string;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
