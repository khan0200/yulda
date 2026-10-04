import { describe, expect, it, vi } from "vitest";

import {
  formatDateOnly,
  formatDateTime,
  formatKrw,
  formatPhoneNumber,
  formatPriceNote,
  formatRelativeTime,
  formatTimeOnly,
} from "./format";

describe("formatKrw", () => {
  it("formats a number with thousands separators and KRW suffix", () => {
    expect(formatKrw(1500000)).toBe("1,500,000 KRW");
  });

  it("formats a numeric string", () => {
    expect(formatKrw("50000")).toBe("50,000 KRW");
  });

  it("returns empty string for null/undefined/empty", () => {
    expect(formatKrw(null)).toBe("");
    expect(formatKrw(undefined)).toBe("");
    expect(formatKrw("")).toBe("");
  });

  it("returns the original string for non-numeric input", () => {
    expect(formatKrw("not-a-number")).toBe("not-a-number");
  });

  it("formats zero correctly", () => {
    expect(formatKrw(0)).toBe("0 KRW");
  });
});

describe("formatPriceNote", () => {
  it("formats a pure number string as KRW", () => {
    expect(formatPriceNote("20000")).toBe("20,000 KRW");
  });

  it("formats 'NNNN won' as KRW", () => {
    expect(formatPriceNote("20000 won")).toBe("20,000 KRW");
  });

  it("leaves free-text pricing untouched", () => {
    expect(formatPriceNote("negotiable")).toBe("negotiable");
  });

  it("leaves mixed currency text untouched (not KRW)", () => {
    expect(formatPriceNote("$50 OBO")).toBe("$50 OBO");
  });

  it("returns empty string for null/undefined/empty", () => {
    expect(formatPriceNote(null)).toBe("");
    expect(formatPriceNote(undefined)).toBe("");
    expect(formatPriceNote("")).toBe("");
  });
});

describe("formatDateOnly", () => {
  it("formats an ISO date string as YYYY-MM-DD", () => {
    expect(formatDateOnly("2026-03-05T10:30:00Z")).toBe("2026-03-05");
  });

  it("returns empty string for null/undefined", () => {
    expect(formatDateOnly(null)).toBe("");
    expect(formatDateOnly(undefined)).toBe("");
  });

  it("returns empty string for an invalid date", () => {
    expect(formatDateOnly("not-a-date")).toBe("");
  });
});

describe("formatTimeOnly", () => {
  it("formats time as HH:MM using local time", () => {
    const date = new Date(2026, 2, 5, 9, 5);
    expect(formatTimeOnly(date)).toBe("09:05");
  });

  it("returns empty string for null/undefined", () => {
    expect(formatTimeOnly(null)).toBe("");
    expect(formatTimeOnly(undefined)).toBe("");
  });
});

describe("formatDateTime", () => {
  it("formats date and time together", () => {
    const date = new Date(2026, 2, 5, 9, 5);
    expect(formatDateTime(date)).toBe("2026-03-05 09:05");
  });

  it("returns empty string for null/undefined", () => {
    expect(formatDateTime(null)).toBe("");
    expect(formatDateTime(undefined)).toBe("");
  });
});

describe("formatRelativeTime", () => {
  it("returns empty string for timestamps less than a minute old", () => {
    const now = new Date().toISOString();
    expect(formatRelativeTime(now, () => "fallback")).toBe("");
  });

  it("returns minutes for timestamps under an hour old", () => {
    const fiveMinAgo = new Date(Date.now() - 5 * 60000).toISOString();
    expect(formatRelativeTime(fiveMinAgo, () => "fallback")).toBe("5m");
  });

  it("returns hours for timestamps under a day old", () => {
    const threeHoursAgo = new Date(Date.now() - 3 * 3600000).toISOString();
    expect(formatRelativeTime(threeHoursAgo, () => "fallback")).toBe("3h");
  });

  it("returns days for timestamps under a week old", () => {
    const twoDaysAgo = new Date(Date.now() - 2 * 86400000).toISOString();
    expect(formatRelativeTime(twoDaysAgo, () => "fallback")).toBe("2d");
  });

  it("falls back to formatDate for timestamps a week or older", () => {
    const tenDaysAgo = new Date(Date.now() - 10 * 86400000).toISOString();
    const formatDate = vi.fn(() => "Mar 1, 2026");
    expect(formatRelativeTime(tenDaysAgo, formatDate)).toBe("Mar 1, 2026");
    expect(formatDate).toHaveBeenCalledOnce();
  });
});

describe("formatPhoneNumber", () => {
  it("formats an 11-digit Korean mobile number (010-XXXX-XXXX)", () => {
    expect(formatPhoneNumber("01012345678")).toBe("010-1234-5678");
  });

  it("formats a 10-digit Korean landline-style number", () => {
    expect(formatPhoneNumber("0212345678")).toBe("021-234-5678");
  });

  it("strips existing separators before reformatting", () => {
    expect(formatPhoneNumber("010-1234-5678")).toBe("010-1234-5678");
  });

  it("returns the original string unchanged for unrecognized formats", () => {
    expect(formatPhoneNumber("+1 555 1234")).toBe("+1 555 1234");
  });

  it("returns empty string for null/undefined", () => {
    expect(formatPhoneNumber(null)).toBe("");
    expect(formatPhoneNumber(undefined)).toBe("");
  });
});
