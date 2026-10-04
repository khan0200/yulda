export type NotificationType = "NEW_MESSAGE" | "LISTING_LIKED";

export interface AppNotification {
  id: string;
  type: NotificationType;
  title: string;
  body: string;
  link: string | null;
  is_read: boolean;
  created_at: string;
}
