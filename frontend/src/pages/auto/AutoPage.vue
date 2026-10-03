<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { useDebounceFn } from "@vueuse/core";
import { Plus } from "lucide-vue-next";

import AutoCard from "@/components/auto/AutoCard.vue";
import NeighborhoodBar from "@/components/common/NeighborhoodBar.vue";
import SimpleAutocomplete from "@/components/common/SimpleAutocomplete.vue";
import { VEHICLE_MAKES } from "@/data/vehicleCatalog";
import { useAutoStore } from "@/stores/autoStore";
import { useUserLocationStore } from "@/stores/userLocationStore";
import type { AccidentHistory, AutoListingType, BodyType, FuelType, TransmissionType } from "@/types/auto";

const { t } = useI18n();
const store = useAutoStore();
const locationStore = useUserLocationStore();

const listingTypes: AutoListingType[] = ["SALE", "RENTAL"];
const fuelTypes: FuelType[] = ["GASOLINE", "DIESEL", "LPG", "HYBRID", "ELECTRIC"];
const transmissions: TransmissionType[] = ["AUTOMATIC", "MANUAL"];
const bodyTypes: BodyType[] = ["SEDAN", "SUV", "HATCHBACK", "WAGON", "MINIVAN", "PICKUP", "COUPE", "CONVERTIBLE", "VAN"];
const accidentHistories: AccidentHistory[] = ["NONE", "MINOR", "MAJOR"];

const activeListingType = ref<AutoListingType | null>(null);
const filters = reactive({
  make: "",
  fuelType: "",
  transmission: "",
  minYear: "",
  maxYear: "",
  minPrice: "",
  maxPrice: "",
  minMileage: "",
  maxMileage: "",
  bodyType: "",
  color: "",
  accidentHistory: "",
  city: "",
});
const page = ref(1);

const sortedListings = computed(() => {
  return locationStore.sortByProximity(
    store.listings,
    (item) => item.location?.coordinates,
    (item) => item.city,
  );
});

async function loadListings(reset = true) {
  if (reset) page.value = 1;
  await store.fetchListings(
    {
      listing_type: activeListingType.value ?? undefined,
      make: filters.make || undefined,
      fuel_type: (filters.fuelType as FuelType) || undefined,
      transmission: (filters.transmission as TransmissionType) || undefined,
      min_year: filters.minYear ? Number(filters.minYear) : undefined,
      max_year: filters.maxYear ? Number(filters.maxYear) : undefined,
      min_price: filters.minPrice ? Number(filters.minPrice) : undefined,
      max_price: filters.maxPrice ? Number(filters.maxPrice) : undefined,
      min_mileage: filters.minMileage ? Number(filters.minMileage) : undefined,
      max_mileage: filters.maxMileage ? Number(filters.maxMileage) : undefined,
      body_type: (filters.bodyType as BodyType) || undefined,
      color: filters.color || undefined,
      accident_history: (filters.accidentHistory as AccidentHistory) || undefined,
      city: filters.city || undefined,
      page: page.value,
      page_size: 24,
    },
    !reset,
  );
}

const debouncedSearch = useDebounceFn(() => loadListings(true), 350);
watch(() => filters.make, debouncedSearch);

function selectListingType(type: AutoListingType | null) {
  activeListingType.value = type;
  loadListings(true);
}

async function loadMore() {
  page.value += 1;
  await loadListings(false);
}

onMounted(() => loadListings(true));
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-10">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-yulda-black">{{ t("auto.title") }}</h1>
        <p class="mt-1 text-sm text-yulda-gray-500">{{ t("auto.subtitle") }}</p>
      </div>
      <RouterLink to="/auto/new" class="btn-primary">
        <Plus class="h-4 w-4" />
        {{ t("auto.newListing") }}
      </RouterLink>
    </div>

    <!-- Daangn-style Neighborhood bar for local-first listings -->
    <NeighborhoodBar class="mt-6" />

    <div class="mt-6 flex flex-wrap gap-2">
      <button
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeListingType === null ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectListingType(null)"
      >
        {{ t("marketplace.allCategories") }}
      </button>
      <button
        v-for="type in listingTypes"
        :key="type"
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeListingType === type ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectListingType(type)"
      >
        {{ t(`auto.listingType.${type}`) }}
      </button>
    </div>

    <div class="mt-4 flex flex-wrap items-end gap-3 rounded-2xl border border-yulda-gray-100 bg-yulda-gray-50 p-4">
      <div class="w-36">
        <label class="label">{{ t("auto.make") }}</label>
        <SimpleAutocomplete v-model="filters.make" :options="VEHICLE_MAKES" placeholder="Hyundai" />
      </div>
      <div>
        <label class="label">{{ t("auto.fuelType.GASOLINE") }}</label>
        <select v-model="filters.fuelType" class="input w-36" @change="loadListings(true)">
          <option value="">{{ t("auto.allFuelTypes") }}</option>
          <option v-for="fuel in fuelTypes" :key="fuel" :value="fuel">{{ t(`auto.fuelType.${fuel}`) }}</option>
        </select>
      </div>
      <div>
        <label class="label">{{ t("auto.transmission.AUTOMATIC") }}</label>
        <select v-model="filters.transmission" class="input w-36" @change="loadListings(true)">
          <option value="">{{ t("auto.allTransmissions") }}</option>
          <option v-for="tr in transmissions" :key="tr" :value="tr">{{ t(`auto.transmission.${tr}`) }}</option>
        </select>
      </div>
      <div>
        <label class="label">{{ t("auto.minYear") }}</label>
        <input v-model="filters.minYear" type="number" class="input w-24" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("auto.maxYear") }}</label>
        <input v-model="filters.maxYear" type="number" class="input w-24" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("auto.minPrice") }}</label>
        <input v-model="filters.minPrice" type="number" class="input w-32" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("auto.maxPrice") }}</label>
        <input v-model="filters.maxPrice" type="number" class="input w-32" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("auto.minMileage") }}</label>
        <input v-model="filters.minMileage" type="number" class="input w-28" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("auto.maxMileage") }}</label>
        <input v-model="filters.maxMileage" type="number" class="input w-28" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("auto.bodyType.label") }}</label>
        <select v-model="filters.bodyType" class="input w-36" @change="loadListings(true)">
          <option value="">{{ t("auto.bodyType.all") }}</option>
          <option v-for="bt in bodyTypes" :key="bt" :value="bt">{{ t(`auto.bodyType.${bt}`) }}</option>
        </select>
      </div>
      <div>
        <label class="label">{{ t("auto.color") }}</label>
        <input v-model="filters.color" type="text" class="input w-28" :placeholder="t('auto.colorPlaceholder')" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("auto.accidentHistory.label") }}</label>
        <select v-model="filters.accidentHistory" class="input w-40" @change="loadListings(true)">
          <option value="">{{ t("auto.accidentHistory.all") }}</option>
          <option v-for="ah in accidentHistories" :key="ah" :value="ah">{{ t(`auto.accidentHistory.${ah}`) }}</option>
        </select>
      </div>
      <div>
        <label class="label">{{ t("auto.city") }}</label>
        <input v-model="filters.city" type="text" class="input w-36" @change="loadListings(true)" />
      </div>
    </div>

    <div v-if="store.isLoading && store.listings.length === 0" class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
      <div v-for="i in 8" :key="i" class="card aspect-[3/4] animate-pulse bg-yulda-gray-100" />
    </div>

    <div v-else-if="store.listings.length === 0" class="card mt-8 p-10 text-center text-sm text-yulda-gray-500">
      {{ t("auto.empty") }}
    </div>

    <div v-else>
      <div class="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        <AutoCard v-for="listing in sortedListings" :key="listing.id" :listing="listing" />
      </div>

      <div v-if="store.hasMore" class="mt-6 flex justify-center">
        <button class="btn-outline" :disabled="store.isLoading" @click="loadMore">
          {{ t("auto.loadMore") }}
        </button>
      </div>
    </div>
  </div>
</template>
