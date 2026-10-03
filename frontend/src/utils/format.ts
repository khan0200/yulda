export function formatKrw(amount: number | string | null | undefined): string {
  if (amount === null || amount === undefined || amount === "") return "";
  const num = typeof amount === "number" ? amount : parseFloat(String(amount).replace(/[^0-9.-]/g, ""));
  if (isNaN(num)) return String(amount);
  return `${new Intl.NumberFormat("en-US").format(num)} KRW`;
}

export function formatPriceNote(val: string | null | undefined): string {
  if (!val) return "";
  const trimmed = val.trim();
  const digitsOnly = trimmed.replace(/[^0-9]/g, "");
  if (digitsOnly && (!/[a-zA-Z\u0400-\u04FF\uAC00-\uD7AF]/.test(trimmed) || /^(krw|won|₩|von|sum)$/i.test(trimmed.replace(/[0-9,\s]/g, "")))) {
    const num = parseInt(digitsOnly, 10);
    return `${new Intl.NumberFormat("en-US").format(num)} KRW`;
  }
  return trimmed;
}

export function formatRelativeTime(isoDate: string, formatDate: (date: Date) => string): string {
  const date = new Date(isoDate);
  const diffMs = Date.now() - date.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "";
  if (diffMin < 60) return `${diffMin}m`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h`;
  const diffDay = Math.floor(diffHr / 24);
  if (diffDay < 7) return `${diffDay}d`;
  return formatDate(date);
}

export function formatDateTime(isoDate: string | Date | null | undefined): string {
  if (!isoDate) return "";
  const date = typeof isoDate === "string" ? new Date(isoDate) : isoDate;
  if (isNaN(date.getTime())) return String(isoDate);
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  const h = String(date.getHours()).padStart(2, "0");
  const min = String(date.getMinutes()).padStart(2, "0");
  return `${y}-${m}-${d} ${h}:${min}`;
}