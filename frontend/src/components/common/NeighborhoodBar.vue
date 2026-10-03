<script setup lang="ts">
import { ref } from "vue";
import { Check, ChevronDown, LocateFixed, MapPin, X } from "lucide-vue-next";

import { useUserLocationStore } from "@/stores/userLocationStore";

const locationStore = useUserLocationStore();
const isSelectorOpen = ref(false);

const POPULAR_CITIES = [
  "Seoul",
  "Ansan",
  "Incheon",
  "Suwon",
  "Cheongju",
  "Baran",
  "Cheonan",
  "Daegu",
  "Busan",
  "Gimhae",
  "Pyeongtaek",
  "Toshkent",
  "Samarqand",
  "Andijon",
];

async function handleGPS() {
  await locationStore.enableLocationWithGPS();
  isSelectorOpen.value = false;
}

function handleSelectCity(city: string) {
  locationStore.setManualCity(city);
  isSelectorOpen.value = false;
}
</script>

<template>
  <div class="relative mb-6 rounded-2xl border border-yulda-gray-200 bg-white p-3 shadow-sm transition-all">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <!-- Left: Active Neighborhood Indicator -->
      <div class="flex items-center gap-2.5">
        <div
          class="flex h-9 w-9 items-center justify-center rounded-xl transition-colors"
          :class="locationStore.isLocationEnabled ? 'bg-emerald-50 text-emerald-600' : 'bg-yulda-gray-100 text-yulda-gray-500'"
        >
          <MapPin class="h-4 w-4" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold text-yulda-gray-400 uppercase tracking-wider">Mening hududim</span>
            <span
              v-if="locationStore.isLocationEnabled"
              class="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700 ring-1 ring-emerald-200"
            >
              <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
              TOP saralash faol
            </span>
          </div>
          <button
            type="button"
            class="flex items-center gap-1.5 text-sm font-bold text-yulda-black hover:text-yulda-gold transition-colors"
            @click="isSelectorOpen = !isSelectorOpen"
          >
            <span>{{ locationStore.currentCity || "Barcha hududlar (Lokatsiyani yoqish)" }}</span>
            <ChevronDown class="h-3.5 w-3.5 text-yulda-gray-400 transition-transform" :class="{ 'rotate-180': isSelectorOpen }" />
          </button>
        </div>
      </div>

      <!-- Right: Action Buttons -->
      <div class="flex items-center gap-2">
        <button
          type="button"
          class="flex items-center gap-1.5 rounded-xl border border-yulda-gray-200 bg-yulda-gray-50 px-3 py-1.5 text-xs font-semibold text-yulda-black transition-colors hover:bg-yulda-gray-100"
          :disabled="locationStore.isDetecting"
          @click="handleGPS"
        >
          <LocateFixed class="h-3.5 w-3.5 text-emerald-600" :class="{ 'animate-spin': locationStore.isDetecting }" />
          <span>{{ locationStore.isDetecting ? "Aniqlanmoqda..." : "GPS orqali aniqlash" }}</span>
        </button>

        <button
          v-if="locationStore.isLocationEnabled"
          type="button"
          class="flex h-8 w-8 items-center justify-center rounded-xl text-yulda-gray-400 hover:bg-yulda-gray-100 hover:text-yulda-black transition-colors"
          title="Barcha hududlarni ko'rish (Filtrni o'chirish)"
          @click="locationStore.disableLocation"
        >
          <X class="h-4 w-4" />
        </button>
      </div>
    </div>

    <!-- Dropdown / Popover for choosing city manually -->
    <div
      v-if="isSelectorOpen"
      class="mt-3 border-t border-yulda-gray-100 pt-3"
    >
      <p class="text-xs font-medium text-yulda-gray-500 mb-2">Ommabop hududlardan tanlang (Daangn uslubida):</p>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="city in POPULAR_CITIES"
          :key="city"
          type="button"
          class="inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-medium transition-all"
          :class="
            locationStore.currentCity.toLowerCase() === city.toLowerCase()
              ? 'bg-yulda-black text-white shadow-sm'
              : 'bg-yulda-gray-100 text-yulda-gray-700 hover:bg-yulda-gray-200'
          "
          @click="handleSelectCity(city)"
        >
          <span>{{ city }}</span>
          <Check v-if="locationStore.currentCity.toLowerCase() === city.toLowerCase()" class="h-3 w-3 text-yulda-yellow" />
        </button>
      </div>
    </div>
  </div>
</template>
