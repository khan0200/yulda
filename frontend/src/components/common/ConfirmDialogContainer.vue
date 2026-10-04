<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { AlertTriangle } from "lucide-vue-next";

import { useConfirmStore } from "@/stores/confirmStore";

const { t } = useI18n();
const store = useConfirmStore();
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-150 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-100 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="store.request"
        class="fixed inset-0 z-[998] flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm"
        @click.self="store.cancel"
      >
        <div class="w-full max-w-sm rounded-2xl bg-white p-6 shadow-card-hover">
          <div class="flex items-start gap-3">
            <div
              class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full"
              :class="store.request.danger ? 'bg-red-50 text-red-500' : 'bg-yulda-yellow/15 text-yulda-black'"
            >
              <AlertTriangle class="h-5 w-5" />
            </div>
            <div class="min-w-0 flex-1 pt-1.5">
              <h3 v-if="store.request.title" class="text-sm font-bold text-yulda-black">{{ store.request.title }}</h3>
              <p class="mt-1 text-sm text-yulda-gray-600">{{ store.request.message }}</p>
            </div>
          </div>

          <div class="mt-5 flex justify-end gap-2">
            <button type="button" class="btn-outline !px-4 !py-2 text-sm" @click="store.cancel">
              {{ store.request.cancelLabel ?? t("common.cancel") }}
            </button>
            <button
              type="button"
              class="rounded-xl px-4 py-2 text-sm font-semibold text-white transition-colors"
              :class="store.request.danger ? 'bg-red-500 hover:bg-red-600' : 'bg-yulda-black hover:bg-yulda-charcoal'"
              @click="store.confirm"
            >
              {{ store.request.confirmLabel ?? t("common.confirm") }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
