<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { ImageOff, MapPin } from "lucide-vue-next";

import type { HousingListing } from "@/types/housing";
import { formatKrw } from "@/utils/format";

defineProps<{ listing: HousingListing }>();
const { t } = useI18n();
</script>

<template>
  <RouterLink :to="`/housing/${listing.id}`" class="card flex flex-col overflow-hidden transition-shadow hover:shadow-card-hover">
    <div class="flex aspect-[4/3] items-center justify-center bg-yulda-gray-100">
      <img v-if="listing.photos[0]" :src="listing.photos[0]" :alt="listing.title" class="h-full w-full object-cover" />
      <ImageOff v-else class="h-8 w-8 text-yulda-gray-300" />
    </div>
    <div class="flex flex-1 flex-col gap-1.5 p-4">
      <span class="text-xs font-semibold text-yulda-gray-400">{{ t(`housing.type.${listing.housing_type}`) }}</span>
      <h3 class="line-clamp-2 text-sm font-bold text-yulda-black">{{ listing.title }}</h3>
      <p class="mt-auto text-sm font-extrabold text-yulda-black">
        {{ formatKrw(listing.deposit) }} / {{ formatKrw(listing.monthly_rent) }}
      </p>
      <div class="flex items-center justify-between text-xs text-yulda-gray-400">
        <span v-if="listing.metro_station" class="flex items-center gap-1">
          <MapPin class="h-3 w-3" />
          {{ listing.metro_station }}
        </span>
        <span v-else-if="listing.city">{{ listing.city }}</span>
        <span
          v-if="listing.status !== 'ACTIVE'"
          class="rounded-full bg-yulda-gray-100 px-2 py-0.5 font-semibold text-yulda-gray-600"
        >
          {{ t(`housing.status.${listing.status}`) }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>
