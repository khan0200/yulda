<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { ChevronDown } from "lucide-vue-next";

const props = defineProps<{
  modelValue: string;
  options: string[];
  placeholder?: string;
  disabled?: boolean;
}>();
const emit = defineEmits<{ "update:modelValue": [v: string] }>();

const isOpen = ref(false);
const inputEl = ref<HTMLInputElement | null>(null);
const rootEl = ref<HTMLElement | null>(null);

const filtered = computed(() => {
  const q = props.modelValue.trim().toLowerCase();
  if (!q) return props.options.slice(0, 20);
  return props.options.filter((v) => v.toLowerCase().includes(q)).slice(0, 20);
});

function select(v: string) {
  emit("update:modelValue", v);
  isOpen.value = false;
}

function onBlur() {
  setTimeout(() => { isOpen.value = false; }, 150);
}

function onClickOutside(e: MouseEvent) {
  if (rootEl.value && !rootEl.value.contains(e.target as Node)) {
    isOpen.value = false;
  }
}

onMounted(() => document.addEventListener("mousedown", onClickOutside));
onUnmounted(() => document.removeEventListener("mousedown", onClickOutside));

watch(() => props.disabled, (d) => { if (d) isOpen.value = false; });

function highlightMatch(text: string): string {
  const q = props.modelValue.trim();
  if (!q) return text;
  const idx = text.toLowerCase().indexOf(q.toLowerCase());
  if (idx === -1) return text;
  return (
    text.slice(0, idx) +
    `<mark class="bg-yulda-yellow/60 text-yulda-black rounded px-0.5">${text.slice(idx, idx + q.length)}</mark>` +
    text.slice(idx + q.length)
  );
}
</script>

<template>
  <div ref="rootEl" class="relative">
    <div class="relative">
      <input
        ref="inputEl"
        :value="modelValue"
        type="text"
        :placeholder="placeholder"
        :disabled="disabled"
        class="input pr-9"
        autocomplete="off"
        @input="emit('update:modelValue', ($event.target as HTMLInputElement).value); isOpen = true"
        @focus="!disabled && (isOpen = true)"
        @blur="onBlur"
        @keydown.escape="isOpen = false"
        @keydown.enter.prevent="filtered[0] && select(filtered[0])"
      />
      <ChevronDown class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-yulda-gray-400" />
    </div>
    <Transition
      enter-active-class="transition-all duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition-all duration-100 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <ul
        v-if="isOpen && filtered.length"
        class="absolute z-50 mt-1 max-h-56 w-full overflow-y-auto rounded-xl border border-yulda-gray-100 bg-white shadow-lg"
      >
        <li
          v-for="option in filtered"
          :key="option"
          class="cursor-pointer px-3 py-2.5 text-sm transition-colors hover:bg-yulda-yellow/10"
          @mousedown.prevent="select(option)"
        >
          <span v-html="highlightMatch(option)" />
        </li>
      </ul>
    </Transition>
  </div>
</template>
