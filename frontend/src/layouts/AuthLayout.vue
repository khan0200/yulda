<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

import AppLogo from "@/components/common/AppLogo.vue";
import LanguageSwitcher from "@/components/common/LanguageSwitcher.vue";

const { t } = useI18n();
</script>

<template>
  <div class="grid min-h-screen grid-cols-1 lg:grid-cols-2">
    <div class="flex flex-col justify-center px-8 py-12 sm:px-16 lg:px-24">
      <div class="mb-10 flex items-center justify-between">
        <RouterLink to="/"><AppLogo :size="28" /></RouterLink>
        <LanguageSwitcher />
      </div>
      <div class="w-full max-w-sm">
        <slot />
      </div>
    </div>
    <div class="relative hidden overflow-hidden bg-yulda-black lg:block">
      <svg class="absolute inset-0 h-full w-full" viewBox="0 0 600 900" fill="none" preserveAspectRatio="xMidYMid slice">
        <path d="M60 820 L220 520 L340 680 L520 160" stroke="#FFD600" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" opacity="0.9" />
        <circle cx="60" cy="820" r="8" fill="#FFD600" />
        <circle cx="520" cy="160" r="8" fill="#FFD600" />
      </svg>
      <div class="absolute bottom-16 left-16 right-16 text-white">
        <p class="text-3xl font-bold leading-tight">{{ t("auth.heroLine1") }}</p>
        <p class="mt-3 text-yulda-gray-300">{{ t("auth.heroLine2") }}</p>
      </div>
    </div>
  </div>
</template>
