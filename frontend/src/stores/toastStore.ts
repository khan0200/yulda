import { ref } from "vue";
import { defineStore } from "pinia";

export type ToastType = "success" | "error" | "info";

export interface Toast {
  id: string;
  type: ToastType;
  message: string;
}

const DEFAULT_DURATION_MS = 4000;

export const useToastStore = defineStore("toast", () => {
  const toasts = ref<Toast[]>([]);

  function dismiss(id: string): void {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  }

  function push(type: ToastType, message: string, durationMs = DEFAULT_DURATION_MS): string {
    const id = `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    toasts.value = [...toasts.value, { id, type, message }];
    if (durationMs > 0) {
      window.setTimeout(() => dismiss(id), durationMs);
    }
    return id;
  }

  function success(message: string): string {
    return push("success", message);
  }

  function error(message: string): string {
    return push("error", message);
  }

  function info(message: string): string {
    return push("info", message);
  }

  return { toasts, push, success, error, info, dismiss };
});
