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
  city: string | null;
  location: GeoPoint | null;
  requires_korean: boolean;
  visa_sponsorship: boolean;
  photos: string[];
  contact_method: JobContactMethod;
  contact_value: string | null;
  status: JobPostStatus;
  owner: OwnerSummary;
  like_count: number;
  created_at: string;
  updated_at: string;
}
