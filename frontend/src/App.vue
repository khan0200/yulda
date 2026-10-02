<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

import AppLayout from "@/layouts/AppLayout.vue";
import AuthLayout from "@/layouts/AuthLayout.vue";
import PublicLayout from "@/layouts/PublicLayout.vue";

const route = useRoute();

const layout = computed(() => {
  switch (route.meta.layout) {
    case "auth":
      return AuthLayout;
    case "app":
      return AppLayout;
    default:
      return PublicLayout;
  }
});
</script>

<template>
  <component :is="layout">
    <RouterView />
  </component>
</template>
