<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import { Check, ChevronDown } from "lucide-vue-next";

const props = defineProps<{
  modelValue: string[];
  options: { value: string; label: string }[];
  label: string;
  clearLabel?: string;
}>();
const emit = defineEmits<{ "update:modelValue": [v: string[]] }>();

const isOpen = ref(false);
const rootEl = ref<HTMLElement | null>(null);

function toggle(value: string) {
  const next = props.modelValue.includes(value)
    ? props.modelValue.filter((v) => v !== value)
    : [...props.modelValue, value];
  emit("update:modelValue", next);
}

function clear() {
  emit("update:modelValue", []);
}

function onClickOutside(e: MouseEvent) {
  if (rootEl.value && !rootEl.value.contains(e.target as Node)) {
    isOpen.value = false;
  }
}

onMounted(() => document.addEventListener("mousedown", onClickOutside));
onUnmounted(() => document.removeEventListener("mousedown", onClickOutside));
</script>

<template>
  <div ref="rootEl" class="relative">
    <button
      type="button"
      class="input flex w-48 items-center justify-between gap-2 text-left"
      @click="isOpen = !isOpen"
    >
      <span class="truncate">
        {{ label }}<span v-if="modelValue.length" class="ml-1 font-semibold text-yulda-black">({{ modelValue.length }})</span>
      </span>
      <ChevronDown class="h-4 w-4 flex-shrink-0 text-yulda-gray-400" :class="{ 'rotate-180': isOpen }" />
    </button>

    <Transition
      enter-active-class="transition-all duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition-all duration-100 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="absolute z-50 mt-1 max-h-72 w-64 overflow-y-auto rounded-xl border border-yulda-gray-100 bg-white p-1.5 shadow-lg"
      >
        <button
          v-for="opt in options"
          :key="opt.value"
          type="button"
          class="flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-left text-sm transition-colors hover:bg-yulda-gray-50"
          @click="toggle(opt.value)"
        >
          <span
            class="flex h-4 w-4 flex-shrink-0 items-center justify-center rounded border"
            :class="modelValue.includes(opt.value) ? 'border-yulda-black bg-yulda-black' : 'border-yulda-gray-300'"
          >
            <Check v-if="modelValue.includes(opt.value)" class="h-3 w-3 text-white" />
          </span>
          <span class="truncate text-yulda-gray-700">{{ opt.label }}</span>
        </button>

        <div v-if="modelValue.length" class="mt-1 border-t border-yulda-gray-100 pt-1.5">
          <button
            type="button"
            class="w-full rounded-lg px-2.5 py-1.5 text-left text-xs font-medium text-yulda-gray-400 hover:bg-yulda-gray-50 hover:text-yulda-black"
            @click="clear"
          >
            {{ clearLabel ?? "Clear" }}
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>
