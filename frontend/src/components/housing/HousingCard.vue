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
      <div class="flex items-center gap-1.5">
        <span class="text-xs font-semibold text-yulda-gray-400">{{ t(`housing.type.${listing.housing_type}`) }}</span>
        <template v-if="listing.floor !== null && listing.total_floors !== null">
          <span class="text-yulda-gray-300">&middot;</span>
          <span class="text-xs font-semibold text-yulda-gray-400">{{ listing.floor }}/{{ listing.total_floors }}{{ t('housing.floor') }}</span>
        </template>
      </div>
      <h3 class="line-clamp-2 text-sm font-bold text-yulda-black">{{ listing.title }}</h3>
      <p class="text-sm font-extrabold text-yulda-black">
        {{ formatKrw(listing.deposit) }} / {{ formatKrw(listing.monthly_rent) }}
      </p>
      <div v-if="listing.area_m2 || listing.room_count || listing.direction" class="flex flex-wrap items-center gap-1.5 text-xs text-yulda-gray-500">
        <span v-if="listing.area_m2">{{ listing.area_m2 }}m²</span>
        <span v-if="listing.area_m2 && (listing.room_count || listing.direction)" class="text-yulda-gray-300">&middot;</span>
        <span v-if="listing.room_count">{{ listing.room_count }}{{ t('housing.roomCount') }}</span>
        <span v-if="listing.room_count && listing.direction" class="text-yulda-gray-300">&middot;</span>
        <span v-if="listing.direction">{{ t(`housing.direction.${listing.direction}`) }}</span>
      </div>
      <div class="mt-auto flex items-center justify-between text-xs text-yulda-gray-400">
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
