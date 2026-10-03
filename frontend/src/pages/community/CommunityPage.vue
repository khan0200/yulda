<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { Plus } from "lucide-vue-next";

import NeighborhoodBar from "@/components/common/NeighborhoodBar.vue";
import PostCard from "@/components/community/PostCard.vue";
import { favoriteApi } from "@/services/favoriteApi";
import { useAuthStore } from "@/stores/authStore";
import { useCommunityStore } from "@/stores/communityStore";
import { useUserLocationStore } from "@/stores/userLocationStore";
import type { PostCategory } from "@/types/community";

const { t } = useI18n();
const store = useCommunityStore();
const locationStore = useUserLocationStore();
const auth = useAuthStore();
const likedIds = ref<Set<string>>(new Set());

async function loadLikedIds() {
  if (!auth.isAuthenticated) return;
  try {
    likedIds.value = new Set(await favoriteApi.listMine("COMMUNITY"));
  } catch {
    likedIds.value = new Set();
  }
}

const categories: PostCategory[] = [
  "QUESTION",
  "ANNOUNCEMENT",
  "LOST_AND_FOUND",
  "MEETUP",
  "TRAVELER_REQUEST",
  "NEWS",
  "OTHER",
];
const activeCategory = ref<PostCategory | null>(null);
const page = ref(1);

async function loadPosts(reset = true) {
  if (reset) page.value = 1;
  await store.fetchPosts(
    {
      category: activeCategory.value ?? undefined,
      city: locationStore.isLocationEnabled ? locationStore.currentCity || undefined : undefined,
      page: page.value,
      page_size: 20,
    },
    !reset,
  );
}

function selectCategory(category: PostCategory | null) {
  activeCategory.value = category;
  loadPosts(true);
}

async function loadMore() {
  page.value += 1;
  await loadPosts(false);
}

watch(() => [locationStore.isLocationEnabled, locationStore.currentCity], () => loadPosts(true));

onMounted(() => {
  loadPosts(true);
  loadLikedIds();
});
</script>

<template>
  <div class="mx-auto max-w-3xl px-6 py-10">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-yulda-black">{{ t("community.title") }}</h1>
        <p class="mt-1 text-sm text-yulda-gray-500">{{ t("community.subtitle") }}</p>
      </div>
      <RouterLink to="/community/new" class="btn-primary">
        <Plus class="h-4 w-4" />
        {{ t("community.newPost") }}
      </RouterLink>
    </div>

    <!-- Daangn-style Neighborhood bar: filters posts to the selected area -->
    <NeighborhoodBar class="mt-6" />

    <div class="flex flex-wrap gap-2">
      <button
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeCategory === null ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectCategory(null)"
      >
        {{ t("community.allCategories") }}
      </button>
      <button
        v-for="category in categories"
        :key="category"
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeCategory === category ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectCategory(category)"
      >
        {{ t(`community.category.${category}`) }}
      </button>
    </div>

    <div v-if="store.isLoading && store.posts.length === 0" class="mt-8 flex flex-col gap-3">
      <div v-for="i in 4" :key="i" class="card h-28 animate-pulse bg-yulda-gray-100" />
    </div>

    <div v-else-if="store.posts.length === 0" class="card mt-8 p-10 text-center text-sm text-yulda-gray-500">
      {{ t("community.empty") }}
    </div>

    <div v-else class="mt-6 flex flex-col gap-3">
      <PostCard v-for="post in store.posts" :key="post.id" :post="post" :liked="likedIds.has(post.id)" />

      <button
        v-if="store.hasMore"
        class="btn-outline mt-2 self-center"
        :disabled="store.isLoading"
        @click="loadMore"
      >
        {{ t("community.loadMore") }}
      </button>
    </div>
  </div>
</template>
