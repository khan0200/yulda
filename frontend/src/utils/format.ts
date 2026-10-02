export function formatKrw(amount: number): string {
  return new Intl.NumberFormat("en-US").format(amount) + " ₩";
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
