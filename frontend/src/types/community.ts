import type { GeoPoint } from "@/types/user";

export type PostCategory =
  | "QUESTION"
  | "ANNOUNCEMENT"
  | "LOST_AND_FOUND"
  | "MEETUP"
  | "TRAVELER_REQUEST"
  | "NEWS"
  | "OTHER";

export interface AuthorSummary {
  id: string;
  name: string;
  avatar: string | null;
}

export interface CommunityPost {
  id: string;
  category: PostCategory;
  title: string;
  body: string;
  photos: string[];
  city: string | null;
  location: GeoPoint | null;
  author: AuthorSummary;
  comment_count: number;
  created_at: string;
  updated_at: string;
}

export interface CommunityComment {
  id: string;
  post_id: string;
  body: string;
  author: AuthorSummary;
  created_at: string;
}
