<script setup lang="ts">
import PublicHeader from "@/components/navigation/PublicHeader.vue";
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
          <span class="text-lg font-extrabold tracking-tight">YULDA</span>
          <p class="text-sm text-yulda-gray-500">&copy; {{ new Date().getFullYear() }} Yulda. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>
