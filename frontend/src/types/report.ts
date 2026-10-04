export type ReportTargetType = "USER" | "MARKETPLACE" | "HOUSING" | "AUTO" | "JOBS" | "SERVICES" | "COMMUNITY";

export type ReportReason = "SPAM" | "SCAM" | "INAPPROPRIATE" | "HARASSMENT" | "FAKE_LISTING" | "OTHER";

export type ReportStatus = "PENDING" | "RESOLVED" | "DISMISSED";

export interface ReportCreatePayload {
  target_type: ReportTargetType;
  target_id: string;
  reason: ReportReason;
  details?: string | null;
}

export interface Report {
  id: string;
  reporter: { id: string; name: string };
  target_type: ReportTargetType;
  target_id: string;
  reason: ReportReason;
  details: string | null;
  status: ReportStatus;
  created_at: string;
  resolved_at: string | null;
}
