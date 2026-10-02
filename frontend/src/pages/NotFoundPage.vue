<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

const { t } = useI18n();
</script>

<template>
  <div class="mx-auto flex max-w-7xl flex-col items-center px-6 py-32 text-center">
    <p class="text-6xl font-extrabold text-yulda-yellow">404</p>
    <h1 class="mt-4 text-2xl font-bold text-yulda-black">{{ t("notFound.title") }}</h1>
    <p class="mt-2 text-yulda-gray-500">{{ t("notFound.subtitle") }}</p>
    <RouterLink to="/" class="btn-primary mt-8">{{ t("notFound.backHome") }}</RouterLink>
  </div>
</template>
