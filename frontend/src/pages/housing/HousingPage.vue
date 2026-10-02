<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { Plus } from "lucide-vue-next";

import HousingCard from "@/components/housing/HousingCard.vue";
import { useHousingStore } from "@/stores/housingStore";
import type { HousingType } from "@/types/housing";

const { t } = useI18n();
const store = useHousingStore();

const types: HousingType[] = ["ONE_ROOM", "TWO_ROOM", "ROOMMATE", "APARTMENT", "COMMERCIAL"];
const activeType = ref<HousingType | null>(null);
const filters = reactive({ minDeposit: "", maxDeposit: "", minRent: "", maxRent: "", city: "" });
const page = ref(1);

async function loadListings(reset = true) {
  if (reset) page.value = 1;
  await store.fetchListings(
    {
      housing_type: activeType.value ?? undefined,
      min_deposit: filters.minDeposit ? Number(filters.minDeposit) : undefined,
      max_deposit: filters.maxDeposit ? Number(filters.maxDeposit) : undefined,
      min_rent: filters.minRent ? Number(filters.minRent) : undefined,
      max_rent: filters.maxRent ? Number(filters.maxRent) : undefined,
      city: filters.city || undefined,
      page: page.value,
      page_size: 24,
    },
    !reset,
  );
}

function selectType(type: HousingType | null) {
  activeType.value = type;
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
        <h1 class="text-2xl font-bold text-yulda-black">{{ t("housing.title") }}</h1>
        <p class="mt-1 text-sm text-yulda-gray-500">{{ t("housing.subtitle") }}</p>
      </div>
      <RouterLink to="/housing/new" class="btn-primary">
        <Plus class="h-4 w-4" />
        {{ t("housing.newListing") }}
      </RouterLink>
    </div>

    <div class="mt-6 flex flex-wrap gap-2">
      <button
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeType === null ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectType(null)"
      >
        {{ t("housing.allTypes") }}
      </button>
      <button
        v-for="type in types"
        :key="type"
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeType === type ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectType(type)"
      >
        {{ t(`housing.type.${type}`) }}
      </button>
    </div>

    <div class="mt-4 flex flex-wrap items-end gap-3 rounded-2xl border border-yulda-gray-100 bg-yulda-gray-50 p-4">
      <div>
        <label class="label">{{ t("housing.minDeposit") }}</label>
        <input v-model="filters.minDeposit" type="number" class="input w-32" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("housing.maxDeposit") }}</label>
        <input v-model="filters.maxDeposit" type="number" class="input w-32" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("housing.minRent") }}</label>
        <input v-model="filters.minRent" type="number" class="input w-32" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("housing.maxRent") }}</label>
        <input v-model="filters.maxRent" type="number" class="input w-32" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("housing.city") }}</label>
        <input v-model="filters.city" type="text" class="input w-40" @change="loadListings(true)" />
      </div>
    </div>

    <div v-if="store.isLoading && store.listings.length === 0" class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
      <div v-for="i in 8" :key="i" class="card aspect-[3/4] animate-pulse bg-yulda-gray-100" />
    </div>

    <div v-else-if="store.listings.length === 0" class="card mt-8 p-10 text-center text-sm text-yulda-gray-500">
      {{ t("housing.empty") }}
    </div>

    <div v-else>
      <div class="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        <HousingCard v-for="listing in store.listings" :key="listing.id" :listing="listing" />
      </div>

      <div v-if="store.hasMore" class="mt-6 flex justify-center">
        <button class="btn-outline" :disabled="store.isLoading" @click="loadMore">
          {{ t("housing.loadMore") }}
        </button>
      </div>
    </div>
  </div>
</template>
