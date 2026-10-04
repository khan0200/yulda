export interface BlockedUser {
  id: string;
  blocked_user: { id: string; name: string; avatar: string | null };
  created_at: string;
}
