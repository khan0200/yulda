<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { onClickOutside } from "@vueuse/core";
import { Check, Globe } from "lucide-vue-next";

import { SUPPORTED_LOCALES, setLocale, type SupportedLocale } from "@/i18n";

const { locale, t } = useI18n();
const isOpen = ref(false);
const rootEl = ref<HTMLElement | null>(null);

onClickOutside(rootEl, () => {
  isOpen.value = false;
});

function selectLocale(code: SupportedLocale) {
  setLocale(code);
  isOpen.value = false;
}
</script>

<template>
  <div ref="rootEl" class="relative">
    <button
      type="button"
      class="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black"
      :aria-label="t('language')"
      @click="isOpen = !isOpen"
    >
      <Globe class="h-4 w-4" />
      <span class="uppercase">{{ locale }}</span>
    </button>

    <div
      v-if="isOpen"
      class="absolute right-0 top-full z-50 mt-1 w-44 overflow-hidden rounded-xl border border-yulda-gray-100 bg-white py-1 shadow-card-hover"
    >
      <button
        v-for="option in SUPPORTED_LOCALES"
        :key="option.code"
        type="button"
        class="flex w-full items-center justify-between px-4 py-2.5 text-left text-sm hover:bg-yulda-gray-50"
        @click="selectLocale(option.code)"
      >
        <span>{{ option.nativeLabel }}</span>
        <Check v-if="locale === option.code" class="h-4 w-4 text-yulda-black" />
      </button>
    </div>
  </div>
</template>
