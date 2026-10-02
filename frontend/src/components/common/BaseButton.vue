<script setup lang="ts">
import { computed } from "vue";
import { Loader2 } from "lucide-vue-next";

const props = withDefaults(
  defineProps<{
    variant?: "primary" | "secondary" | "outline" | "ghost";
    type?: "button" | "submit" | "reset";
    loading?: boolean;
    disabled?: boolean;
    fullWidth?: boolean;
  }>(),
  {
    variant: "primary",
    type: "button",
    loading: false,
    disabled: false,
    fullWidth: false,
  },
);

const classes = computed(() => [
  `btn-${props.variant}`,
  props.fullWidth ? "w-full" : "",
]);
</script>

<template>
  <button :type="type" :class="classes" :disabled="disabled || loading">
    <Loader2 v-if="loading" class="h-4 w-4 animate-spin" />
    <slot />
  </button>
</template>
