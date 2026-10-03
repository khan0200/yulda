<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";

declare global {
  interface Window {
    turnstile?: {
      render: (container: HTMLElement, options: Record<string, unknown>) => string;
      remove: (widgetId: string) => void;
      reset: (widgetId: string) => void;
    };
    onTurnstileLoad?: () => void;
  }
}

const emit = defineEmits<{ verified: [token: string]; expired: []; error: [err: unknown] }>();

const siteKey = import.meta.env.VITE_TURNSTILE_SITE_KEY as string | undefined;
const containerEl = ref<HTMLElement | null>(null);
let widgetId: string | null = null;

const SCRIPT_SRC = "https://challenges.cloudflare.com/turnstile/v0/api.js";
const SCRIPT_ID = "cf-turnstile-script";

function loadScript(): Promise<void> {
  return new Promise((resolve) => {
    if (window.turnstile) {
      resolve();
      return;
    }
    const existing = document.getElementById(SCRIPT_ID);
    if (existing) {
      existing.addEventListener("load", () => resolve());
      return;
    }
    const script = document.createElement("script");
    script.id = SCRIPT_ID;
    script.src = SCRIPT_SRC;
    script.async = true;
    script.defer = true;
    script.onload = () => resolve();
    document.head.appendChild(script);
  });
}

onMounted(async () => {
  if (!siteKey || !containerEl.value) return;
  await loadScript();
  if (!window.turnstile || !containerEl.value) return;

  widgetId = window.turnstile.render(containerEl.value, {
    sitekey: siteKey,
    callback: (token: string) => emit("verified", token),
    "expired-callback": () => emit("expired"),
    "error-callback": (err: unknown) => {
      console.warn("Turnstile notice:", err);
      emit("error", err);
    },
  });
});

onBeforeUnmount(() => {
  if (widgetId && window.turnstile) {
    window.turnstile.remove(widgetId);
  }
});
</script>

<template>
  <div v-if="siteKey" ref="containerEl" class="my-2 flex justify-center min-h-[65px]" />
</template>
