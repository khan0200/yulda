export type ConversationListingType = "MARKETPLACE" | "HOUSING" | "AUTO" | "JOBS" | "SERVICES" | "COMMUNITY";

export interface ParticipantSummary {
  id: string;
  name: string;
  avatar: string | null;
}

export interface Conversation {
  id: string;
  participants: ParticipantSummary[];
  listing_type: ConversationListingType | null;
  listing_id: string | null;
  listing_title: string | null;
  last_message_preview: string | null;
  last_message_at: string | null;
  unread_count: number;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  sender_id: string;
  body: string;
  created_at: string;
  read_at: string | null;
}
