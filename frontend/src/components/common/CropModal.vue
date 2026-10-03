<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { Check, X } from "lucide-vue-next";
import { Cropper, type CropperResult } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";

const props = defineProps<{ imageSrc: string; currentIndex: number; totalCount: number }>();
const emit = defineEmits<{ confirm: [blob: Blob]; skip: []; cancel: [] }>();
const { t } = useI18n();

const cropperRef = ref<InstanceType<typeof Cropper> | null>(null);
const isProcessing = ref(false);

function handleConfirm() {
  const result = cropperRef.value?.getResult() as CropperResult | undefined;
  const canvas = result?.canvas;
  if (!canvas) return;

  isProcessing.value = true;
  canvas.toBlob(
    (blob) => {
      isProcessing.value = false;
      if (blob) emit("confirm", blob);
    },
    "image/jpeg",
    0.92,
  );
}
</script>

<template>
  <div class="fixed inset-0 z-50 flex flex-col bg-black/90">
    <div class="flex items-center justify-between px-6 py-4 text-white">
      <button type="button" class="flex items-center gap-1.5 text-sm font-medium hover:text-yulda-gray-300" @click="emit('cancel')">
        <X class="h-4 w-4" />
        {{ t("upload.cropCancel") }}
      </button>
      <span class="text-sm text-yulda-gray-300">
        {{ t("upload.cropProgress", { current: props.currentIndex + 1, total: props.totalCount }) }}
      </span>
      <button type="button" class="flex items-center gap-1.5 text-sm font-semibold text-yulda-yellow hover:text-yulda-gold" :disabled="isProcessing" @click="handleConfirm">
        <Check class="h-4 w-4" />
        {{ t("upload.cropConfirm") }}
      </button>
    </div>

    <div class="relative min-h-0 flex-1 px-4 pb-4">
      <Cropper
        ref="cropperRef"
        class="cropper h-full w-full"
        :src="imageSrc"
        :stencil-props="{ aspectRatio: 16 / 9 }"
        :resize-image="{ adjustStencil: false }"
        image-restriction="fit-area"
      />
    </div>

    <p class="px-6 pb-6 text-center text-xs text-yulda-gray-400">{{ t("upload.cropHint") }}</p>
  </div>
</template>
