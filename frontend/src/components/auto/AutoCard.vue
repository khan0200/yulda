<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { ImageOff } from "lucide-vue-next";

import { useUserLocationStore } from "@/stores/userLocationStore";
import type { AutoListing } from "@/types/auto";
import { formatKrw } from "@/utils/format";

const props = defineProps<{ listing: AutoListing }>();
const { t } = useI18n();
const locationStore = useUserLocationStore();

const isRental = computed(() => props.listing.listing_type === "RENTAL");
const distanceInfo = computed(() =>
  locationStore.getDistanceInfo(props.listing.location?.coordinates, props.listing.city),
);
</script>

<template>
  <RouterLink :to="`/auto/${listing.id}`" class="card flex flex-col overflow-hidden transition-all hover:shadow-card-hover group">
    <div class="relative flex aspect-video items-center justify-center bg-yulda-gray-100 overflow-hidden">
      <img
        v-if="listing.photos[0]"
        :src="listing.photos[0]"
        :alt="listing.model"
        class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
      />
      <ImageOff v-else class="h-8 w-8 text-yulda-gray-300" />

      <!-- Daangn-style local badge -->
      <span
        v-if="distanceInfo.isSameCity"
        class="absolute left-2.5 top-2.5 rounded-lg bg-yulda-black/90 px-2 py-0.5 text-[10px] font-bold text-yulda-yellow shadow-md backdrop-blur"
      >
        ★ Hududingizda
      </span>

      <!-- Accident-free / credit trust badges -->
      <div class="absolute right-2.5 top-2.5 flex flex-col items-end gap-1">
        <span
          v-if="listing.accident_history === 'NONE'"
          class="rounded-lg bg-emerald-500/90 px-2 py-0.5 text-[10px] font-bold text-white shadow-md backdrop-blur"
        >
          {{ t("auto.accidentHistory.NONE") }}
        </span>
        <span
          v-if="listing.credit_available"
          class="rounded-lg bg-white/90 px-2 py-0.5 text-[10px] font-bold text-yulda-black shadow-md backdrop-blur"
        >
          {{ t("auto.creditAvailable") }}
        </span>
      </div>
    </div>
    <div class="flex flex-1 flex-col gap-1.5 p-4">
      <div class="flex items-center gap-1.5 text-xs font-semibold text-yulda-gray-400">
        <span>{{ listing.year }}</span>
        <span>&middot;</span>
        <span>{{ listing.mileage_km.toLocaleString() }} km</span>
        <template v-if="listing.body_type">
          <span>&middot;</span>
          <span>{{ t(`auto.bodyType.${listing.body_type}`) }}</span>
        </template>
      </div>
      <h3 class="line-clamp-2 text-sm font-bold text-yulda-black">{{ listing.make }} {{ listing.model }}</h3>
      <span class="text-xs font-semibold text-yulda-gray-400">{{ t(`auto.fuelType.${listing.fuel_type}`) }}</span>
      <p class="mt-auto text-base font-extrabold text-yulda-black">
        <template v-if="isRental">{{ formatKrw(listing.rental_price_per_day ?? 0) }} {{ t("auto.perDay") }}</template>
        <template v-else>{{ formatKrw(listing.price) }}</template>
      </p>
      <div class="flex items-center justify-between text-xs text-yulda-gray-400">
        <div class="flex items-center gap-1.5 truncate">
          <span v-if="listing.city" class="font-medium text-yulda-gray-600 truncate">{{ listing.city }}</span>
          <span
            v-if="distanceInfo.formatted"
            class="rounded bg-emerald-50 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-700 ring-1 ring-emerald-200 flex-shrink-0"
          >
            {{ distanceInfo.formatted }}
          </span>
        </div>
        <span
          v-if="listing.status !== 'ACTIVE'"
          class="rounded-full bg-yulda-gray-100 px-2 py-0.5 font-semibold text-yulda-gray-600 flex-shrink-0 ml-1"
        >
          {{ t(`auto.status.${listing.status}`) }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>
