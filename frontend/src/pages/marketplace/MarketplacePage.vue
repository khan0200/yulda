<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { Plus } from "lucide-vue-next";

import NeighborhoodBar from "@/components/common/NeighborhoodBar.vue";
import ListingCard from "@/components/marketplace/ListingCard.vue";
import { useMarketplaceStore } from "@/stores/marketplaceStore";
import { useUserLocationStore } from "@/stores/userLocationStore";
import type { ListingCategory, ListingCondition } from "@/types/marketplace";

const { t } = useI18n();
const store = useMarketplaceStore();
const locationStore = useUserLocationStore();

const categories: ListingCategory[] = ["ELECTRONICS", "FURNITURE", "BIKES", "CLOTHING", "FOOD", "FREE", "OTHER"];
const conditions: ListingCondition[] = ["NEW", "USED"];

const activeCategory = ref<ListingCategory | null>(null);
const filters = reactive({ condition: "", minPrice: "", maxPrice: "", city: "" });
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
      category: activeCategory.value ?? undefined,
      condition: (filters.condition as ListingCondition) || undefined,
      min_price: filters.minPrice ? Number(filters.minPrice) : undefined,
      max_price: filters.maxPrice ? Number(filters.maxPrice) : undefined,
      city: filters.city || undefined,
      page: page.value,
      page_size: 24,
    },
    !reset,
  );
}

function selectCategory(category: ListingCategory | null) {
  activeCategory.value = category;
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
        <h1 class="text-2xl font-bold text-yulda-black">{{ t("marketplace.title") }}</h1>
        <p class="mt-1 text-sm text-yulda-gray-500">{{ t("marketplace.subtitle") }}</p>
      </div>
      <RouterLink to="/marketplace/new" class="btn-primary">
        <Plus class="h-4 w-4" />
        {{ t("marketplace.newListing") }}
      </RouterLink>
    </div>

    <!-- Daangn-style Neighborhood bar for local-first listings -->
    <NeighborhoodBar class="mt-6" />

    <div class="mt-6 flex flex-wrap gap-2">
      <button
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeCategory === null ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectCategory(null)"
      >
        {{ t("marketplace.allCategories") }}
      </button>
      <button
        v-for="category in categories"
        :key="category"
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeCategory === category ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectCategory(category)"
      >
        {{ t(`marketplace.category.${category}`) }}
      </button>
    </div>

    <div class="mt-4 flex flex-wrap items-end gap-3 rounded-2xl border border-yulda-gray-100 bg-yulda-gray-50 p-4">
      <div>
        <label class="label">{{ t("marketplace.conditionLabel") }}</label>
        <select v-model="filters.condition" class="input" @change="loadListings(true)">
          <option value="">{{ t("marketplace.allConditions") }}</option>
          <option v-for="condition in conditions" :key="condition" :value="condition">
            {{ t(`marketplace.condition.${condition}`) }}
          </option>
        </select>
      </div>
      <div>
        <label class="label">{{ t("marketplace.minPrice") }}</label>
        <input v-model="filters.minPrice" type="number" class="input w-32" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("marketplace.maxPrice") }}</label>
        <input v-model="filters.maxPrice" type="number" class="input w-32" @change="loadListings(true)" />
      </div>
      <div>
        <label class="label">{{ t("marketplace.city") }}</label>
        <input v-model="filters.city" type="text" class="input w-40" @change="loadListings(true)" />
      </div>
    </div>

    <div v-if="store.isLoading && store.listings.length === 0" class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
      <div v-for="i in 8" :key="i" class="card aspect-[3/4] animate-pulse bg-yulda-gray-100" />
    </div>

    <div v-else-if="store.listings.length === 0" class="card mt-8 p-10 text-center text-sm text-yulda-gray-500">
      {{ t("marketplace.empty") }}
    </div>

    <div v-else>
      <div class="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        <ListingCard v-for="listing in sortedListings" :key="listing.id" :listing="listing" />
      </div>

      <div v-if="store.hasMore" class="mt-6 flex justify-center">
        <button class="btn-outline" :disabled="store.isLoading" @click="loadMore">
          {{ t("marketplace.loadMore") }}
        </button>
      </div>
    </div>
  </div>
</template>
