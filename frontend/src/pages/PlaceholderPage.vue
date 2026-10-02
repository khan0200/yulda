<script setup lang="ts">
defineProps<{ title: string; subtitle?: string }>();
</script>

<template>
  <div class="mx-auto flex max-w-7xl flex-col items-start px-6 py-24">
    <h1 class="text-3xl font-bold text-yulda-black">{{ title }}</h1>
    <p v-if="subtitle" class="mt-2 text-yulda-gray-500">{{ subtitle }}</p>
    <div class="mt-10 card w-full p-10 text-center text-sm text-yulda-gray-500">
      This module is coming soon.
    </div>
  </div>
</template>
