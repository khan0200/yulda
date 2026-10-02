<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
  <div class="mx-auto flex max-w-7xl flex-col items-center px-6 py-32 text-center">
    <p class="text-6xl font-extrabold text-yulda-yellow">404</p>
    <h1 class="mt-4 text-2xl font-bold text-yulda-black">Page not found</h1>
    <p class="mt-2 text-yulda-gray-500">The page you're looking for doesn't exist.</p>
    <RouterLink to="/" class="btn-primary mt-8">Back to home</RouterLink>
  </div>
</template>
