<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { Building2, Car, CarFront, Package, ShoppingBag, Store, Users, Wrench } from "lucide-vue-next";

import PostCard from "@/components/community/PostCard.vue";
import { useCommunityStore } from "@/stores/communityStore";

const { t } = useI18n();
const communityStore = useCommunityStore();

const menuItems = computed(() => [
  { icon: Car, label: t("nav.taxi"), to: "/taxi" },
  { icon: Package, label: t("nav.delivery"), to: "/delivery" },
  { icon: Store, label: t("nav.marketplace"), to: "/marketplace" },
  { icon: Building2, label: t("nav.housing"), to: "/housing" },
  { icon: CarFront, label: t("nav.auto"), to: "/auto" },
  { icon: ShoppingBag, label: t("nav.jobs"), to: "/jobs" },
  { icon: Wrench, label: t("nav.services"), to: "/services" },
  { icon: Users, label: t("nav.community"), to: "/community" },
]);

onMounted(() => {
  communityStore.fetchPosts({ page_size: 4 });
});
</script>

<template>
  <div>
    <section class="border-b border-yulda-gray-100">
      <div class="mx-auto max-w-7xl px-6 py-5">
        <div class="grid grid-cols-4 gap-2 sm:grid-cols-8 sm:gap-3">
          <RouterLink
            v-for="item in menuItems"
            :key="item.to"
            :to="item.to"
            class="flex flex-col items-center gap-2 rounded-xl px-2 py-3 text-center transition-colors hover:bg-yulda-gray-50"
          >
            <span class="flex h-11 w-11 items-center justify-center rounded-full bg-yulda-yellow/15 text-yulda-black">
              <component :is="item.icon" class="h-5 w-5" />
            </span>
            <span class="text-xs font-semibold text-yulda-gray-700">{{ item.label }}</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="relative overflow-hidden">
      <div class="mx-auto max-w-7xl px-6 pb-16 pt-16 sm:pt-20">
        <div class="max-w-3xl">
          <h1 class="text-5xl font-extrabold leading-[1.1] tracking-tight text-yulda-black sm:text-6xl">
            {{ t("home.heroTitlePrefix") }} <span class="relative inline-block">{{ t("home.heroTitleHighlight") }}
              <svg class="absolute -bottom-2 left-0 w-full" height="10" viewBox="0 0 220 10" fill="none" preserveAspectRatio="none">
                <path d="M2 8C40 2 160 2 218 8" stroke="#FFD600" stroke-width="5" stroke-linecap="round"/>
              </svg>
            </span>
          </h1>
          <p class="mt-6 max-w-xl text-lg text-yulda-gray-600">
            {{ t("home.heroSubtitle") }}
          </p>
          <div class="mt-10 flex flex-wrap gap-3">
            <RouterLink to="/taxi" class="btn-primary">{{ t("home.bookRide") }}</RouterLink>
            <RouterLink to="/signup" class="btn-outline">{{ t("home.getStarted") }}</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 pb-24">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-yulda-black">{{ t("home.latestCommunity") }}</h2>
        <RouterLink to="/community" class="text-sm font-semibold text-yulda-black hover:underline">
          {{ t("home.viewAll") }}
        </RouterLink>
      </div>

      <div v-if="communityStore.isLoading" class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div v-for="i in 4" :key="i" class="card h-40 animate-pulse bg-yulda-gray-100" />
      </div>

      <div v-else-if="communityStore.posts.length === 0" class="card mt-6 p-10 text-center text-sm text-yulda-gray-500">
        {{ t("home.noCommunityPosts") }}
      </div>

      <div v-else class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <PostCard v-for="post in communityStore.posts" :key="post.id" :post="post" />
      </div>
    </section>
  </div>
</template>
