<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { ArrowLeft, CheckCircle2, ImageOff, Trash2 } from "lucide-vue-next";

import { useAuthStore } from "@/stores/authStore";
import { useHousingStore } from "@/stores/housingStore";
import { formatKrw } from "@/utils/format";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const store = useHousingStore();

const listingId = computed(() => route.params.id as string);
const isOwner = computed(() => {
  return Boolean(auth.user && store.currentListing && store.currentListing.owner.id === auth.user.id);
});

async function handleDelete() {
  if (!confirm(t("housing.confirmDelete"))) return;
  await store.deleteListing(listingId.value);
  router.push("/housing");
}

async function handleMarkRented() {
  await store.markRented(listingId.value);
}

onMounted(() => store.fetchListing(listingId.value));
</script>

<template>
  <div class="mx-auto max-w-3xl px-6 py-10">
    <RouterLink to="/housing" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("housing.backToFeed") }}
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
              {{ t(`housing.type.${store.currentListing.housing_type}`) }}
            </span>
            <div v-if="isOwner" class="flex items-center gap-4">
              <button
                v-if="store.currentListing.status === 'ACTIVE'"
                class="flex items-center gap-1.5 text-sm text-yulda-gray-600 hover:text-yulda-black"
                @click="handleMarkRented"
              >
                <CheckCircle2 class="h-4 w-4" />
                {{ t("housing.status.RENTED") }}
              </button>
              <button class="flex items-center gap-1.5 text-sm text-red-500 hover:text-red-600" @click="handleDelete">
                <Trash2 class="h-4 w-4" />
                {{ t("housing.deleteListing") }}
              </button>
            </div>
          </div>

          <h1 class="mt-4 text-xl font-bold text-yulda-black">{{ store.currentListing.title }}</h1>

          <div class="mt-3 grid grid-cols-3 gap-3 rounded-xl bg-yulda-gray-50 p-4 text-center">
            <div>
              <p class="text-xs text-yulda-gray-400">{{ t("housing.deposit") }}</p>
              <p class="mt-1 text-sm font-bold text-yulda-black">{{ formatKrw(store.currentListing.deposit) }}</p>
            </div>
            <div>
              <p class="text-xs text-yulda-gray-400">{{ t("housing.monthlyRent") }}</p>
              <p class="mt-1 text-sm font-bold text-yulda-black">{{ formatKrw(store.currentListing.monthly_rent) }}</p>
            </div>
            <div>
              <p class="text-xs text-yulda-gray-400">{{ t("housing.maintenanceFee") }}</p>
              <p class="mt-1 text-sm font-bold text-yulda-black">{{ formatKrw(store.currentListing.maintenance_fee) }}</p>
            </div>
          </div>

          <span
            v-if="store.currentListing.status !== 'ACTIVE'"
            class="mt-3 inline-block rounded-full bg-yulda-gray-100 px-3 py-1 text-xs font-semibold text-yulda-gray-600"
          >
            {{ t(`housing.status.${store.currentListing.status}`) }}
          </span>

          <p class="mt-4 whitespace-pre-wrap text-sm text-yulda-gray-700">{{ store.currentListing.description }}</p>

          <div v-if="store.currentListing.amenities.length > 0" class="mt-4 flex flex-wrap gap-2">
            <span
              v-for="amenity in store.currentListing.amenities"
              :key="amenity"
              class="rounded-full bg-yulda-gray-100 px-3 py-1 text-xs font-medium text-yulda-gray-700"
            >
              {{ t(`housing.amenity.${amenity}`) }}
            </span>
          </div>

          <div class="mt-6 flex items-center gap-2 border-t border-yulda-gray-100 pt-4 text-sm text-yulda-gray-500">
            <div class="flex h-6 w-6 items-center justify-center rounded-full bg-yulda-black text-xs font-semibold text-white">
              {{ store.currentListing.owner.name.charAt(0) }}
            </div>
            <span>{{ store.currentListing.owner.name }}</span>
            <span v-if="store.currentListing.metro_station">&middot; {{ store.currentListing.metro_station }}</span>
            <span v-else-if="store.currentListing.city">&middot; {{ store.currentListing.city }}</span>
          </div>

          <div class="mt-4 rounded-xl bg-yulda-gray-50 p-4">
            <p class="text-xs font-semibold uppercase text-yulda-gray-400">{{ t("housing.contactValueLabel") }}</p>
            <p class="mt-1 text-sm font-medium text-yulda-black">{{ store.currentListing.contact_value }}</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
