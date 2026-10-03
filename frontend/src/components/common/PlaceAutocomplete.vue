<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { onClickOutside, useDebounceFn } from "@vueuse/core";
import { Check, Loader2, Map, MapPin, X } from "lucide-vue-next";

import InteractiveMap from "@/components/common/InteractiveMap.vue";
import { placesApi } from "@/services/placesApi";
import type { Place, PlaceCountry } from "@/types/place";
import { getCityCoordinates, type Coordinates, type GeocodedLocation } from "@/utils/geo";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    country?: PlaceCountry;
    placeholder?: string;
    allowMapPicker?: boolean;
  }>(),
  {
    country: undefined,
    placeholder: undefined,
    allowMapPicker: true,
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

const isMapModalOpen = ref(false);
const pendingMapPlace = ref<{ name: string; lat?: number; lon?: number } | null>(null);

const initialMapCoords = computed<Coordinates | undefined>(() => {
  if (query.value) {
    return getCityCoordinates(query.value) ?? undefined;
  }
  return undefined;
});

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

function openMapPicker() {
  isOpen.value = false;
  const existingCoords = query.value ? getCityCoordinates(query.value) : null;
  pendingMapPlace.value = query.value
    ? { name: query.value, lat: existingCoords?.lat, lon: existingCoords?.lon }
    : null;
  isMapModalOpen.value = true;
}

function handleMapSelect(loc: GeocodedLocation) {
  const chosenName = loc.city || loc.name;
  pendingMapPlace.value = {
    name: chosenName,
    lat: loc.lat,
    lon: loc.lon,
  };
}

function confirmMapSelection() {
  if (pendingMapPlace.value?.name) {
    const name = pendingMapPlace.value.name;
    query.value = name;
    hasSelected.value = true;
    emit("update:modelValue", name);
    emit("select", {
      id: `map-${Date.now()}`,
      name,
      country: props.country || "KR",
      admin1: null,
      lat: pendingMapPlace.value.lat ?? null,
      lon: pendingMapPlace.value.lon ?? null,
      source: "USER",
      usage_count: 1,
    });
  }
  isMapModalOpen.value = false;
}

function closeMapModal() {
  isMapModalOpen.value = false;
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

      <!-- Map Picker Button inside Input -->
      <button
        v-if="allowMapPicker"
        type="button"
        class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg text-yulda-gray-400 transition-colors hover:bg-yulda-yellow/20 hover:text-yulda-black"
        :title="placeholder ? `${placeholder} - Xaritadan tanlash` : 'Xaritadan tanlash'"
        @click.stop="openMapPicker"
      >
        <Map class="h-4 w-4" />
      </button>
    </div>

    <!-- Dropdown suggestions -->
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

    <!-- Modal Map Picker -->
    <Teleport to="body">
      <div
        v-if="isMapModalOpen"
        class="fixed inset-0 z-[999] flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
        @click.self="closeMapModal"
      >
        <div class="flex max-h-[90vh] w-full max-w-xl flex-col overflow-hidden rounded-2xl bg-white shadow-2xl">
          <!-- Modal Header -->
          <div class="flex items-center justify-between border-b border-yulda-gray-100 px-5 py-4">
            <div class="flex items-center gap-2.5">
              <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-yulda-yellow/20 text-yulda-black">
                <Map class="h-4 w-4" />
              </div>
              <div>
                <h3 class="text-sm font-bold text-yulda-black">
                  {{ placeholder ? `${placeholder} - Xaritadan tanlash` : "Xaritadan joylashuvni tanlang" }}
                </h3>
                <p class="text-xs text-yulda-gray-400">Xaritani bosib yoki GPS orqali manzilni belgilang</p>
              </div>
            </div>
            <button
              type="button"
              class="flex h-8 w-8 items-center justify-center rounded-xl text-yulda-gray-400 transition-colors hover:bg-yulda-gray-100 hover:text-yulda-black"
              @click="closeMapModal"
            >
              <X class="h-4 w-4" />
            </button>
          </div>

          <!-- Modal Map View -->
          <div class="p-4">
            <InteractiveMap
              mode="picker"
              :initial-location="initialMapCoords"
              height="340px"
              @select="handleMapSelect"
            />
          </div>

          <!-- Modal Footer -->
          <div class="flex items-center justify-between border-t border-yulda-gray-100 bg-yulda-gray-50 px-5 py-3.5">
            <div class="flex items-center gap-2 truncate pr-2">
              <MapPin class="h-4 w-4 flex-shrink-0 text-emerald-600" />
              <span v-if="pendingMapPlace?.name" class="truncate text-xs font-semibold text-yulda-black">
                {{ pendingMapPlace.name }}
              </span>
              <span v-else class="text-xs text-yulda-gray-400">
                Xaritadan nuqtani tanlang...
              </span>
            </div>
            <div class="flex items-center gap-2 flex-shrink-0">
              <button
                type="button"
                class="rounded-xl border border-yulda-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-yulda-gray-600 transition-colors hover:bg-yulda-gray-100"
                @click="closeMapModal"
              >
                Bekor qilish
              </button>
              <button
                type="button"
                class="btn-primary text-xs py-1.5 px-4"
                :disabled="!pendingMapPlace?.name"
                @click="confirmMapSelection"
              >
                <Check class="h-3.5 w-3.5 mr-1" />
                Tanlash
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
