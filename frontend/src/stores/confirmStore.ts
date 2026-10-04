import { ref } from "vue";
import { defineStore } from "pinia";

export interface ConfirmRequest {
  title?: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  danger?: boolean;
}

export const useConfirmStore = defineStore("confirm", () => {
  const request = ref<ConfirmRequest | null>(null);
  let resolver: ((value: boolean) => void) | null = null;

  function ask(req: ConfirmRequest): Promise<boolean> {
    request.value = req;
    return new Promise<boolean>((resolve) => {
      resolver = resolve;
    });
  }

  function confirm(): void {
    resolver?.(true);
    resolver = null;
    request.value = null;
  }

  function cancel(): void {
    resolver?.(false);
    resolver = null;
    request.value = null;
  }

  return { request, ask, confirm, cancel };
});
