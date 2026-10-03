const MAX_DIMENSION = 1920;
const JPEG_QUALITY = 0.8;

const HEIC_EXTENSION_RE = /\.(heic|heif)$/i;

function isHeic(file: File): boolean {
  const type = file.type.toLowerCase();
  // Browsers are inconsistent here: Safari/iOS often reports an empty
  // file.type for HEIC, others report "image/heic" or "image/heif".
  return type === "image/heic" || type === "image/heif" || (!type && HEIC_EXTENSION_RE.test(file.name));
}

async function convertHeicToJpeg(file: File): Promise<File> {
  const { default: heic2any } = await import("heic2any");
  const result = await heic2any({ blob: file, toType: "image/jpeg", quality: JPEG_QUALITY });
  const blob = Array.isArray(result) ? result[0] : result;
  const newName = file.name.replace(HEIC_EXTENSION_RE, ".jpg");
  return new File([blob], newName, { type: "image/jpeg" });
}

/**
 * Converts HEIC/HEIF to JPEG so the browser can actually render it (for the
 * crop preview, or an <img> tag). Returns the original file untouched for
 * every other format. Does not resize/compress — that happens after crop.
 */
export async function normalizeForCropping(file: File): Promise<File> {
  if (!isHeic(file)) return file;
  return convertHeicToJpeg(file);
}

/**
 * Downscales and re-encodes an image client-side before upload, via Canvas.
 * HEIC/HEIF (common on iPhone) is converted to JPEG first, since canvas
 * can't decode it directly in most browsers.
 * Falls back to the original (or HEIC-converted) file if compression fails
 * or doesn't shrink it.
 */
export async function compressImage(file: File): Promise<File> {
  let workingFile = file;

  if (isHeic(file)) {
    try {
      workingFile = await convertHeicToJpeg(file);
    } catch {
      return file; // let the backend reject it rather than silently drop it
    }
  } else if (!file.type.startsWith("image/")) {
    return file;
  }

  try {
    const bitmap = await createImageBitmap(workingFile);
    const scale = Math.min(1, MAX_DIMENSION / Math.max(bitmap.width, bitmap.height));
    const width = Math.round(bitmap.width * scale);
    const height = Math.round(bitmap.height * scale);

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d");
    if (!ctx) return workingFile;

    ctx.drawImage(bitmap, 0, 0, width, height);
    bitmap.close();

    const outputType = workingFile.type === "image/png" ? "image/png" : "image/jpeg";
    const blob = await new Promise<Blob | null>((resolve) =>
      canvas.toBlob(resolve, outputType, JPEG_QUALITY),
    );
    if (!blob || blob.size >= workingFile.size) return workingFile;

    const newName = outputType === "image/jpeg" ? workingFile.name.replace(/\.(png|webp)$/i, ".jpg") : workingFile.name;
    return new File([blob], newName, { type: outputType });
  } catch {
    return workingFile;
  }
}
