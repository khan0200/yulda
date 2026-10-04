import type { GeoPoint } from "@/types/user";

export type JobPostType = "OFFER" | "REQUEST";
export type JobEmploymentType = "PART_TIME" | "FULL_TIME" | "DAILY" | "CONTRACT";
export type JobCategory =
  | "RESTAURANT_CAFE"
  | "RETAIL"
  | "DELIVERY_LOGISTICS"
  | "CONSTRUCTION_FACTORY"
  | "CLEANING"
  | "CARE_CHILDCARE"
  | "OFFICE_ADMIN"
  | "IT_DESIGN"
  | "EDUCATION_TUTORING"
  | "TRANSLATION"
  | "EVENT_PROMOTION"
  | "OTHER";
export type JobPayType = "HOURLY" | "DAILY" | "MONTHLY" | "PER_PROJECT";
export type JobPostStatus = "ACTIVE" | "CLOSED";
export type JobContactMethod = "PHONE" | "CHAT";
export type VisaType =
  | "E9"
  | "E7"
  | "H2"
  | "F1"
  | "F2"
  | "F3"
  | "F4"
  | "F5"
  | "F6"
  | "D2"
  | "D4"
  | "D10"
  | "G1"
  | "UNDOCUMENTED"
  | "OTHER";
export type HousingOption = "NOT_PROVIDED" | "PROVIDED_FREE" | "PROVIDED_PAID";

export interface OwnerSummary {
  id: string;
  name: string;
  avatar: string | null;
}

export interface JobPost {
  id: string;
  post_type: JobPostType;
  category: JobCategory;
  employment_type: JobEmploymentType;
  title: string;
  description: string;
  pay_type: JobPayType | null;
  pay_amount: number | null;
  overtime_pay_amount: number | null;
  city: string | null;
  location: GeoPoint | null;
  requires_korean: boolean;
  visa_sponsorship: boolean;
  accepted_visas: VisaType[];
  housing_option: HousingOption;
  photos: string[];
  contact_method: JobContactMethod;
  contact_value: string | null;
  status: JobPostStatus;
  owner: OwnerSummary;
  like_count: number;
  created_at: string;
  updated_at: string;
}
