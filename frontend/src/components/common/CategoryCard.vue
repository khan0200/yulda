<script setup lang="ts">
import { RouterLink } from "vue-router";
import type { Component } from "vue";
import { ArrowRight } from "lucide-vue-next";

defineProps<{
  icon: Component;
  title: string;
  description: string;
  cta: string;
  to: string;
  accent?: boolean;
}>();
</script>

<template>
  <RouterLink
    :to="to"
    class="card group flex flex-col justify-between p-8 transition-shadow hover:shadow-card-hover"
    :class="accent ? 'bg-yulda-black text-white border-yulda-black' : ''"
  >
    <div>
      <div
        class="mb-6 flex h-12 w-12 items-center justify-center rounded-xl"
        :class="accent ? 'bg-yulda-yellow text-yulda-black' : 'bg-yulda-yellow/15 text-yulda-black'"
      >
        <component :is="icon" class="h-6 w-6" />
      </div>
      <h3 class="text-xl font-bold">{{ title }}</h3>
      <p class="mt-2 text-sm" :class="accent ? 'text-yulda-gray-300' : 'text-yulda-gray-500'">{{ description }}</p>
    </div>
    <div
      class="mt-8 flex items-center gap-2 text-sm font-semibold"
      :class="accent ? 'text-yulda-yellow' : 'text-yulda-black'"
    >
      {{ cta }}
      <ArrowRight class="h-4 w-4 transition-transform group-hover:translate-x-1" />
    </div>
  </RouterLink>
</template>
