<script setup lang="ts">
import { ref, watch } from "vue";
import { onClickOutside, useDebounceFn } from "@vueuse/core";
import { Loader2, MapPin } from "lucide-vue-next";

import { placesApi } from "@/services/placesApi";
import type { Place, PlaceCountry } from "@/types/place";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    country?: PlaceCountry;
    placeholder?: string;
  }>(),
  {
    country: undefined,
    placeholder: undefined,
  },
);

const emit = defineEmits<{
  "update:modelValue": [value: string];
  select: [place: Place | null];
}>();

const query = ref(props.modelValue);
const suggestions = ref<Place[]>([]);
const isOpen = ref(false);
const isLoading = ref(false);
const highlightedIndex = ref(-1);
const rootEl = ref<HTMLElement | null>(null);
const hasSelected = ref(false);

watch(
  () => props.modelValue,
  (value) => {
    if (value !== query.value) query.value = value;
  },
);

const runSearch = useDebounceFn(async (text: string) => {
  if (!text.trim()) {
    suggestions.value = [];
    isLoading.value = false;
    return;
  }
  isLoading.value = true;
  try {
    suggestions.value = await placesApi.search(text.trim(), props.country);
  } finally {
    isLoading.value = false;
  }
}, 250);

function handleInput(event: Event) {
  const value = (event.target as HTMLInputElement).value;
  query.value = value;
  hasSelected.value = false;
  emit("update:modelValue", value);
  highlightedIndex.value = -1;
  isOpen.value = true;
  runSearch(value);
}

function selectPlace(place: Place) {
  query.value = place.name;
  hasSelected.value = true;
  emit("update:modelValue", place.name);
  emit("select", place);
  isOpen.value = false;
}

async function handleBlur() {
  window.setTimeout(async () => {
    isOpen.value = false;
    const trimmed = query.value.trim();
    if (!trimmed || hasSelected.value || !props.country) return;

    const exactMatch = suggestions.value.find((p) => p.name.toLowerCase() === trimmed.toLowerCase());
    if (exactMatch) {
      selectPlace(exactMatch);
      return;
    }

    const learned = await placesApi.learn(trimmed, props.country);
    hasSelected.value = true;
    emit("select", learned);
  }, 150);
}

function handleKeydown(event: KeyboardEvent) {
  if (!isOpen.value || suggestions.value.length === 0) return;

  if (event.key === "ArrowDown") {
    event.preventDefault();
    highlightedIndex.value = Math.min(highlightedIndex.value + 1, suggestions.value.length - 1);
  } else if (event.key === "ArrowUp") {
    event.preventDefault();
    highlightedIndex.value = Math.max(highlightedIndex.value - 1, 0);
  } else if (event.key === "Enter" && highlightedIndex.value >= 0) {
    event.preventDefault();
    selectPlace(suggestions.value[highlightedIndex.value]);
  } else if (event.key === "Escape") {
    isOpen.value = false;
  }
}

onClickOutside(rootEl, () => {
  isOpen.value = false;
});
</script>

<template>
  <div ref="rootEl" class="relative">
    <div class="flex items-center gap-3 rounded-xl border border-yulda-gray-200 px-4 py-3 focus-within:border-yulda-yellow focus-within:ring-2 focus-within:ring-yulda-yellow">
      <MapPin class="h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
      <input
        :value="query"
        :placeholder="placeholder"
        class="w-full border-none p-0 text-sm focus:outline-none focus:ring-0"
        autocomplete="off"
        @input="handleInput"
        @focus="isOpen = true"
        @blur="handleBlur"
        @keydown="handleKeydown"
      />
      <Loader2 v-if="isLoading" class="h-4 w-4 flex-shrink-0 animate-spin text-yulda-gray-400" />
    </div>

    <ul
      v-if="isOpen && suggestions.length > 0"
      class="absolute left-0 right-0 top-full z-50 mt-1 max-h-64 overflow-y-auto rounded-xl border border-yulda-gray-100 bg-white py-1 shadow-card-hover"
    >
      <li
        v-for="(place, index) in suggestions"
        :key="place.id"
        class="cursor-pointer px-4 py-2.5 text-sm"
        :class="index === highlightedIndex ? 'bg-yulda-yellow/15 text-yulda-black' : 'text-yulda-gray-700 hover:bg-yulda-gray-50'"
        @mousedown.prevent="selectPlace(place)"
      >
        <span class="font-medium">{{ place.name }}</span>
        <span v-if="place.admin1" class="ml-1.5 text-xs text-yulda-gray-400">{{ place.admin1 }}</span>
      </li>
    </ul>
  </div>
</template>
