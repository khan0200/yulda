<script setup lang="ts">
import { CheckCircle2, Info, X, XCircle } from "lucide-vue-next";

import { useToastStore } from "@/stores/toastStore";

const store = useToastStore();
</script>

<template>
  <Teleport to="body">
    <div class="pointer-events-none fixed inset-x-0 top-4 z-[999] flex flex-col items-center gap-2 px-4 sm:items-end sm:right-4 sm:left-auto">
      <TransitionGroup
        enter-active-class="transition-all duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-2 scale-95"
        enter-to-class="opacity-100 translate-y-0 scale-100"
        leave-active-class="transition-all duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        move-class="transition-transform duration-200"
      >
        <div
          v-for="toast in store.toasts"
          :key="toast.id"
          class="pointer-events-auto flex w-full max-w-sm items-start gap-2.5 rounded-xl border bg-white px-4 py-3 shadow-card-hover"
          :class="{
            'border-emerald-200': toast.type === 'success',
            'border-red-200': toast.type === 'error',
            'border-yulda-gray-200': toast.type === 'info',
          }"
        >
          <CheckCircle2 v-if="toast.type === 'success'" class="mt-0.5 h-5 w-5 flex-shrink-0 text-emerald-500" />
          <XCircle v-else-if="toast.type === 'error'" class="mt-0.5 h-5 w-5 flex-shrink-0 text-red-500" />
          <Info v-else class="mt-0.5 h-5 w-5 flex-shrink-0 text-yulda-gray-500" />
          <p class="flex-1 text-sm text-yulda-black">{{ toast.message }}</p>
          <button
            type="button"
            class="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full text-yulda-gray-400 hover:bg-yulda-gray-100 hover:text-yulda-black"
            @click="store.dismiss(toast.id)"
          >
            <X class="h-3.5 w-3.5" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
