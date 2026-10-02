<script setup lang="ts">
withDefaults(
  defineProps<{
    size?: number;
    showWordmark?: boolean;
  }>(),
  {
    size: 32,
    showWordmark: true,
  },
);
</script>

<template>
  <span class="inline-flex items-center gap-2">
    <img src="/logo.png" alt="Yulda" :style="{ width: `${size}px`, height: `${size}px` }" class="rounded-lg" />
    <span v-if="showWordmark" class="text-xl font-extrabold tracking-tight text-yulda-black">YULDA</span>
  </span>
</template>
