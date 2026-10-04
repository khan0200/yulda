<script setup lang="ts">
import { useI18n } from "vue-i18n";

import { RouterLink } from "vue-router";

import AppLogo from "@/components/common/AppLogo.vue";
import PublicHeader from "@/components/navigation/PublicHeader.vue";

const { t } = useI18n();
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <PublicHeader />
    <main class="flex-1">
      <slot />
    </main>
    <footer class="border-t border-yulda-gray-100 py-10">
      <div class="mx-auto max-w-7xl px-6">
        <div class="flex flex-col items-start justify-between gap-6 sm:flex-row sm:items-center">
          <AppLogo :size="24" />
          <div class="flex items-center gap-4">
            <RouterLink to="/terms" class="text-sm text-yulda-gray-500 hover:text-yulda-black">{{ t("footer.terms") }}</RouterLink>
            <RouterLink to="/privacy" class="text-sm text-yulda-gray-500 hover:text-yulda-black">{{ t("footer.privacy") }}</RouterLink>
          </div>
          <p class="text-sm text-yulda-gray-500">&copy; {{ new Date().getFullYear() }} Yulda. {{ t("footer.rights") }}</p>
        </div>
      </div>
    </footer>
  </div>
</template>
