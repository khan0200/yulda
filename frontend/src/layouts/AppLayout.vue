<script setup lang="ts">
import AppSidebar from "@/components/navigation/AppSidebar.vue";
import PublicHeader from "@/components/navigation/PublicHeader.vue";
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <PublicHeader />
    <div class="flex flex-1">
      <AppSidebar />
      <main class="min-w-0 flex-1 overflow-y-auto bg-yulda-gray-50">
        <slot />
      </main>
    </div>
  </div>
</template>
