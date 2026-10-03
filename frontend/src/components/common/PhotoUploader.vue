<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { ImagePlus, Loader2, X } from "lucide-vue-next";

import CropModal from "@/components/common/CropModal.vue";
import { uploadApi, type UploadFolder } from "@/services/uploadApi";
import { compressImage, normalizeForCropping } from "@/utils/imageCompression";

const props = withDefaults(
  defineProps<{
    modelValue: string[];
    folder: UploadFolder;
    maxPhotos?: number;
  }>(),
  {
    maxPhotos: 9,
  },
);

const emit = defineEmits<{ "update:modelValue": [value: string[]] }>();
const { t } = useI18n();

const fileInput = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const errorMessage = ref("");

// Crop queue: files waiting to be cropped one at a time, like Instagram/LinkedIn.
const cropQueue = ref<File[]>([]);
const cropQueueTotal = ref(0);
const currentCropSrc = ref("");

function openFilePicker() {
  fileInput.value?.click();
}

async function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  const files = Array.from(input.files ?? []);
  input.value = "";
  if (files.length === 0) return;

  const remainingSlots = props.maxPhotos - props.modelValue.length;
  const filesToQueue = files.slice(0, remainingSlots);
  if (filesToQueue.length === 0) return;

  errorMessage.value = "";
  cropQueue.value = filesToQueue;
  cropQueueTotal.value = filesToQueue.length;
  await openNextCrop();
}

async function openNextCrop() {
  const next = cropQueue.value[0];
  if (!next) {
    currentCropSrc.value = "";
    return;
  }
  try {
    const normalized = await normalizeForCropping(next);
    currentCropSrc.value = URL.createObjectURL(normalized);
  } catch {
    // Couldn't even decode it for preview (corrupt/unsupported) — skip it.
    cropQueue.value = cropQueue.value.slice(1);
    await openNextCrop();
  }
}

function revokeCurrentCropSrc() {
  if (currentCropSrc.value) URL.revokeObjectURL(currentCropSrc.value);
}

async function handleCropConfirm(blob: Blob) {
  const sourceFile = cropQueue.value[0];
  revokeCurrentCropSrc();
  cropQueue.value = cropQueue.value.slice(1);
  if (!sourceFile) return;

  const croppedFile = new File([blob], sourceFile.name.replace(/\.(heic|heif|png|webp)$/i, ".jpg"), {
    type: "image/jpeg",
  });

  await uploadOne(croppedFile);
  await openNextCrop();
}

async function handleCropSkip() {
  revokeCurrentCropSrc();
  cropQueue.value = cropQueue.value.slice(1);
  await openNextCrop();
}

function handleCropCancel() {
  revokeCurrentCropSrc();
  cropQueue.value = [];
  currentCropSrc.value = "";
}

async function uploadOne(file: File) {
  isUploading.value = true;
  try {
    const compressed = await compressImage(file);
    const url = await uploadApi.uploadFile(compressed, props.folder);
    emit("update:modelValue", [...props.modelValue, url]);
  } catch {
    errorMessage.value = t("upload.failed");
  } finally {
    isUploading.value = false;
  }
}

function removePhoto(index: number) {
  emit(
    "update:modelValue",
    props.modelValue.filter((_, i) => i !== index),
  );
}
</script>

<template>
  <div>
    <div class="grid grid-cols-2 gap-2 sm:grid-cols-3">
      <div
        v-for="(url, index) in modelValue"
        :key="url"
        class="relative aspect-video overflow-hidden rounded-xl border border-yulda-gray-200"
      >
        <img :src="url" class="h-full w-full object-cover" :alt="`photo-${index}`" />
        <button
          type="button"
          class="absolute right-1 top-1 flex h-6 w-6 items-center justify-center rounded-full bg-black/60 text-white hover:bg-black/80"
          :aria-label="t('upload.remove')"
          @click="removePhoto(index)"
        >
          <X class="h-3.5 w-3.5" />
        </button>
      </div>

      <button
        v-if="modelValue.length < maxPhotos"
        type="button"
        class="flex aspect-video flex-col items-center justify-center gap-1 rounded-xl border-2 border-dashed border-yulda-gray-300 text-yulda-gray-400 hover:border-yulda-gray-400 hover:text-yulda-gray-600"
        :disabled="isUploading"
        @click="openFilePicker"
      >
        <Loader2 v-if="isUploading" class="h-5 w-5 animate-spin" />
        <ImagePlus v-else class="h-5 w-5" />
        <span class="text-xs font-medium">{{ modelValue.length }}/{{ maxPhotos }}</span>
      </button>
    </div>

    <input
      ref="fileInput"
      type="file"
      accept="image/jpeg,image/png,image/webp,image/heic,image/heif,.heic,.heif"
      multiple
      class="hidden"
      @change="handleFileChange"
    />

    <p v-if="errorMessage" class="mt-2 text-sm text-red-500">{{ errorMessage }}</p>

    <CropModal
      v-if="currentCropSrc"
      :image-src="currentCropSrc"
      :current-index="cropQueueTotal - cropQueue.length"
      :total-count="cropQueueTotal"
      @confirm="handleCropConfirm"
      @skip="handleCropSkip"
      @cancel="handleCropCancel"
    />
  </div>
</template>
