<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";
import { Search } from "lucide-vue-next";

import PostCard from "@/components/community/PostCard.vue";
import ListingCard from "@/components/marketplace/ListingCard.vue";
import { searchApi, type SearchResults } from "@/services/searchApi";

const { t } = useI18n();
const route = useRoute();

const results = ref<SearchResults>({ marketplace: [], community: [] });
const isLoading = ref(false);
const hasSearched = ref(false);

async function runSearch() {
  const q = (route.query.q as string | undefined)?.trim();
  if (!q) {
    results.value = { marketplace: [], community: [] };
    hasSearched.value = false;
    return;
  }
  isLoading.value = true;
  hasSearched.value = true;
  try {
    results.value = await searchApi.search(q);
  } finally {
    isLoading.value = false;
  }
}

watch(() => route.query.q, runSearch);
onMounted(runSearch);
</script>

<template>
  <div class="mx-auto max-w-5xl px-6 py-10">
    <div class="flex items-center gap-3">
      <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-yulda-yellow/15 text-yulda-black">
        <Search class="h-5 w-5" />
      </div>
      <div>
        <h1 class="text-xl font-bold text-yulda-black">{{ t("search.title") }}</h1>
        <p class="text-sm text-yulda-gray-500">"{{ route.query.q }}"</p>
      </div>
    </div>

    <div v-if="isLoading" class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
      <div v-for="i in 8" :key="i" class="card aspect-[3/4] animate-pulse bg-yulda-gray-100" />
    </div>

    <template v-else-if="hasSearched">
      <div
        v-if="results.marketplace.length === 0 && results.community.length === 0"
        class="card mt-8 p-10 text-center text-sm text-yulda-gray-500"
      >
        {{ t("search.noResults") }}
      </div>

      <template v-else>
        <section v-if="results.marketplace.length > 0" class="mt-8">
          <h2 class="text-sm font-bold uppercase tracking-wide text-yulda-gray-500">
            {{ t("search.marketplaceSection") }}
          </h2>
          <div class="mt-3 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
            <ListingCard v-for="item in results.marketplace" :key="item.id" :listing="item" />
          </div>
        </section>

        <section v-if="results.community.length > 0" class="mt-10">
          <h2 class="text-sm font-bold uppercase tracking-wide text-yulda-gray-500">
            {{ t("search.communitySection") }}
          </h2>
          <div class="mt-3 flex flex-col gap-3">
            <PostCard v-for="item in results.community" :key="item.id" :post="item" />
          </div>
        </section>
      </template>
    </template>
  </div>
</template>
