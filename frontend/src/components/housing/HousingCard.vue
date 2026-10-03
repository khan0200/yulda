<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { ImageOff, MapPin } from "lucide-vue-next";

import { useUserLocationStore } from "@/stores/userLocationStore";
import type { HousingListing } from "@/types/housing";
import { formatKrw } from "@/utils/format";

const props = defineProps<{ listing: HousingListing }>();
const { t } = useI18n();
const locationStore = useUserLocationStore();

const distanceInfo = computed(() =>
  locationStore.getDistanceInfo(props.listing.location?.coordinates, props.listing.city),
);
</script>

<template>
  <RouterLink :to="`/housing/${listing.id}`" class="card flex flex-col overflow-hidden transition-all hover:shadow-card-hover group">
    <div class="relative flex aspect-video items-center justify-center bg-yulda-gray-100 overflow-hidden">
      <img
        v-if="listing.photos[0]"
        :src="listing.photos[0]"
        :alt="listing.title"
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
    </div>
    <div class="flex flex-1 flex-col gap-1.5 p-4">
      <span class="text-xs font-semibold text-yulda-gray-400">{{ t(`housing.type.${listing.housing_type}`) }}</span>
      <h3 class="line-clamp-2 text-sm font-bold text-yulda-black">{{ listing.title }}</h3>
      <p class="mt-auto text-sm font-extrabold text-yulda-black">
        {{ formatKrw(listing.deposit) }} / {{ formatKrw(listing.monthly_rent) }}
      </p>
      <div class="flex items-center justify-between text-xs text-yulda-gray-400">
        <div class="flex items-center gap-1.5 truncate">
          <span v-if="listing.metro_station" class="flex items-center gap-1 truncate font-medium text-yulda-gray-600">
            <MapPin class="h-3 w-3 flex-shrink-0" />
            <span class="truncate">{{ listing.metro_station }}</span>
          </span>
          <span v-else-if="listing.city" class="font-medium text-yulda-gray-600 truncate">{{ listing.city }}</span>
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
          {{ t(`housing.status.${listing.status}`) }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>
