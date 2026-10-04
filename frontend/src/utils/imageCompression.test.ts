import { describe, expect, it, vi } from "vitest";

import { normalizeForCropping } from "./imageCompression";

vi.mock("heic2any", () => ({
  default: vi.fn(async () => new Blob(["converted"], { type: "image/jpeg" })),
}));

function makeFile(name: string, type: string): File {
  return new File(["content"], name, { type });
}

describe("normalizeForCropping", () => {
  it("returns non-HEIC files unchanged", async () => {
    const file = makeFile("photo.jpg", "image/jpeg");
    const result = await normalizeForCropping(file);
    expect(result).toBe(file);
  });

  it("returns PNG files unchanged", async () => {
    const file = makeFile("photo.png", "image/png");
    const result = await normalizeForCropping(file);
    expect(result).toBe(file);
  });

  it("converts a file with HEIC MIME type to JPEG", async () => {
    const file = makeFile("photo.heic", "image/heic");
    const result = await normalizeForCropping(file);
    expect(result.type).toBe("image/jpeg");
    expect(result.name).toBe("photo.jpg");
    expect(result).not.toBe(file);
  });

  it("detects HEIC by file extension when MIME type is empty (Safari/iOS quirk)", async () => {
    const file = makeFile("IMG_1234.HEIC", "");
    const result = await normalizeForCropping(file);
    expect(result.type).toBe("image/jpeg");
    expect(result.name).toBe("IMG_1234.jpg");
  });

  it("does not treat a file with empty MIME type and non-HEIC extension as HEIC", async () => {
    const file = makeFile("photo.gif", "");
    const result = await normalizeForCropping(file);
    expect(result).toBe(file);
  });
});
