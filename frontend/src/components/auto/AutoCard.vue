<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { ImageOff } from "lucide-vue-next";

import type { AutoListing } from "@/types/auto";
import { formatKrw } from "@/utils/format";

const props = defineProps<{ listing: AutoListing }>();
const { t } = useI18n();

const isRental = computed(() => props.listing.listing_type === "RENTAL");
</script>

<template>
  <RouterLink :to="`/auto/${listing.id}`" class="card flex flex-col overflow-hidden transition-shadow hover:shadow-card-hover">
    <div class="flex aspect-video items-center justify-center bg-yulda-gray-100">
      <img v-if="listing.photos[0]" :src="listing.photos[0]" :alt="listing.model" class="h-full w-full object-cover" />
      <ImageOff v-else class="h-8 w-8 text-yulda-gray-300" />
    </div>
    <div class="flex flex-1 flex-col gap-1.5 p-4">
      <span class="text-xs font-semibold text-yulda-gray-400">{{ listing.year }} &middot; {{ t(`auto.fuelType.${listing.fuel_type}`) }}</span>
      <h3 class="line-clamp-2 text-sm font-bold text-yulda-black">{{ listing.make }} {{ listing.model }}</h3>
      <p class="mt-auto text-base font-extrabold text-yulda-black">
        <template v-if="isRental">{{ formatKrw(listing.rental_price_per_day ?? 0) }} {{ t("auto.perDay") }}</template>
        <template v-else>{{ formatKrw(listing.price) }}</template>
      </p>
      <div class="flex items-center justify-between text-xs text-yulda-gray-400">
        <span v-if="listing.city">{{ listing.city }}</span>
        <span
          v-if="listing.status !== 'ACTIVE'"
          class="rounded-full bg-yulda-gray-100 px-2 py-0.5 font-semibold text-yulda-gray-600"
        >
          {{ t(`auto.status.${listing.status}`) }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>
