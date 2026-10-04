import { describe, expect, it } from "vitest";

import { getCityCoordinates } from "./geo";

describe("getCityCoordinates", () => {
  it("finds a city by exact lowercase match", () => {
    expect(getCityCoordinates("seoul")).toEqual({ lat: 37.5665, lon: 126.978 });
  });

  it("is case-insensitive", () => {
    expect(getCityCoordinates("SEOUL")).toEqual({ lat: 37.5665, lon: 126.978 });
    expect(getCityCoordinates("Busan")).toEqual({ lat: 35.1796, lon: 129.0756 });
  });

  it("trims whitespace before matching", () => {
    expect(getCityCoordinates("  incheon  ")).toEqual({ lat: 37.4563, lon: 126.7052 });
  });

  it("matches when the input contains the city name as a substring", () => {
    expect(getCityCoordinates("Seoul, South Korea")).toEqual({ lat: 37.5665, lon: 126.978 });
  });

  it("matches when the city name contains the (shorter) input", () => {
    expect(getCityCoordinates("busa")).toEqual({ lat: 35.1796, lon: 129.0756 });
  });

  it("resolves Uzbek/English spelling variants to the same coordinates", () => {
    expect(getCityCoordinates("tashkent")).toEqual(getCityCoordinates("toshkent"));
    expect(getCityCoordinates("samarkand")).toEqual(getCityCoordinates("samarqand"));
  });

  it("returns null for a city not in the catalog", () => {
    expect(getCityCoordinates("Atlantis")).toBeNull();
  });

  it("returns the first catalog entry for an empty string (substring-match quirk)", () => {
    // Every city name "includes" the empty string, so the first catalog
    // entry wins. This documents current behavior rather than prescribing it.
    expect(getCityCoordinates("")).toEqual({ lat: 37.5665, lon: 126.978 });
  });
});
