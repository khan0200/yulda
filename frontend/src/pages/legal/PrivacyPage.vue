<script setup lang="ts">
import { useI18n } from "vue-i18n";

interface Section {
  heading: string;
  body: string;
}

const { t, tm } = useI18n();
const sections = tm("privacy.sections") as unknown as Section[];
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-10">
    <h1 class="text-2xl font-bold text-yulda-black">{{ t("privacy.title") }}</h1>
    <p class="mt-1 text-sm text-yulda-gray-400">{{ t("privacy.lastUpdated") }}</p>

    <div class="mt-8 flex flex-col gap-6">
      <section v-for="section in sections" :key="section.heading">
        <h2 class="text-sm font-bold text-yulda-black">{{ section.heading }}</h2>
        <p class="mt-1.5 text-sm leading-relaxed text-yulda-gray-600">{{ section.body }}</p>
      </section>
    </div>
  </div>
</template>
