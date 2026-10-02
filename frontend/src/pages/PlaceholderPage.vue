<script setup lang="ts">
import { useI18n } from "vue-i18n";

const props = defineProps<{ titleKey: string; subtitleKey?: string }>();
const { t } = useI18n();
</script>

<template>
  <div class="mx-auto flex max-w-7xl flex-col items-start px-6 py-24">
    <h1 class="text-3xl font-bold text-yulda-black">{{ t(props.titleKey) }}</h1>
    <p v-if="props.subtitleKey" class="mt-2 text-yulda-gray-500">{{ t(props.subtitleKey) }}</p>
    <div class="mt-10 card w-full p-10 text-center text-sm text-yulda-gray-500">
      {{ t("placeholder.comingSoon") }}
    </div>
  </div>
</template>
