<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { ArrowLeft, CheckCircle2, ImageOff, Trash2 } from "lucide-vue-next";

import { useAuthStore } from "@/stores/authStore";
import { useMarketplaceStore } from "@/stores/marketplaceStore";
import { formatKrw } from "@/utils/format";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const store = useMarketplaceStore();

const listingId = computed(() => route.params.id as string);
const isOwner = computed(() => {
  return Boolean(auth.user && store.currentListing && store.currentListing.seller.id === auth.user.id);
});
const isFree = computed(() => store.currentListing?.price === 0);

async function handleDelete() {
  if (!confirm(t("marketplace.confirmDelete"))) return;
  await store.deleteListing(listingId.value);
  router.push("/marketplace");
}

async function handleMarkSold() {
  await store.markSold(listingId.value);
}

onMounted(() => store.fetchListing(listingId.value));
</script>

<template>
  <div class="mx-auto max-w-3xl px-6 py-10">
    <RouterLink to="/marketplace" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("marketplace.backToFeed") }}
    </RouterLink>

    <div v-if="store.isLoading && !store.currentListing" class="card mt-6 h-96 animate-pulse bg-yulda-gray-100" />

    <template v-else-if="store.currentListing">
      <div class="card mt-6 overflow-hidden">
        <div class="flex aspect-video items-center justify-center bg-yulda-gray-100">
          <img
            v-if="store.currentListing.photos[0]"
            :src="store.currentListing.photos[0]"
            :alt="store.currentListing.title"
            class="h-full w-full object-cover"
          />
          <ImageOff v-else class="h-10 w-10 text-yulda-gray-300" />
        </div>

        <div class="p-6">
          <div class="flex items-center justify-between">
            <span class="inline-flex items-center rounded-full bg-yulda-yellow/15 px-2.5 py-1 text-xs font-semibold text-yulda-black">
              {{ t(`marketplace.category.${store.currentListing.category}`) }}
            </span>
            <div v-if="isOwner" class="flex items-center gap-4">
              <button
                v-if="store.currentListing.status === 'ACTIVE'"
                class="flex items-center gap-1.5 text-sm text-yulda-gray-600 hover:text-yulda-black"
                @click="handleMarkSold"
              >
                <CheckCircle2 class="h-4 w-4" />
                {{ t("marketplace.markSold") }}
              </button>
              <button class="flex items-center gap-1.5 text-sm text-red-500 hover:text-red-600" @click="handleDelete">
                <Trash2 class="h-4 w-4" />
                {{ t("marketplace.deleteListing") }}
              </button>
            </div>
          </div>

          <h1 class="mt-4 text-xl font-bold text-yulda-black">{{ store.currentListing.title }}</h1>
          <p class="mt-2 text-2xl font-extrabold text-yulda-black">
            <span v-if="isFree" class="text-yulda-gold">{{ t("marketplace.category.FREE") }}</span>
            <span v-else>{{ formatKrw(store.currentListing.price) }}</span>
          </p>
          <span
            v-if="store.currentListing.status !== 'ACTIVE'"
            class="mt-2 inline-block rounded-full bg-yulda-gray-100 px-3 py-1 text-xs font-semibold text-yulda-gray-600"
          >
            {{ t(`marketplace.status.${store.currentListing.status}`) }}
          </span>

          <p class="mt-4 whitespace-pre-wrap text-sm text-yulda-gray-700">{{ store.currentListing.description }}</p>

          <div class="mt-6 flex items-center gap-2 border-t border-yulda-gray-100 pt-4 text-sm text-yulda-gray-500">
            <div class="flex h-6 w-6 items-center justify-center rounded-full bg-yulda-black text-xs font-semibold text-white">
              {{ store.currentListing.seller.name.charAt(0) }}
            </div>
            <span>{{ store.currentListing.seller.name }}</span>
            <span v-if="store.currentListing.city">&middot; {{ store.currentListing.city }}</span>
          </div>

          <div class="mt-4 rounded-xl bg-yulda-gray-50 p-4">
            <p class="text-xs font-semibold uppercase text-yulda-gray-400">
              {{ t(`marketplace.contactMethod.${store.currentListing.contact_method}`) }}
            </p>
            <p class="mt-1 text-sm font-medium text-yulda-black">{{ store.currentListing.contact_value }}</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
