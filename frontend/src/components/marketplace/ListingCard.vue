<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { ImageOff } from "lucide-vue-next";

import type { MarketplaceListing } from "@/types/marketplace";
import { formatKrw } from "@/utils/format";

const props = defineProps<{ listing: MarketplaceListing }>();
const { t } = useI18n();

const isFree = computed(() => props.listing.price === 0);
</script>

<template>
  <RouterLink :to="`/marketplace/${listing.id}`" class="card flex flex-col overflow-hidden transition-shadow hover:shadow-card-hover">
    <div class="flex aspect-video items-center justify-center bg-yulda-gray-100">
      <img v-if="listing.photos[0]" :src="listing.photos[0]" :alt="listing.title" class="h-full w-full object-cover" />
      <ImageOff v-else class="h-8 w-8 text-yulda-gray-300" />
    </div>
    <div class="flex flex-1 flex-col gap-1.5 p-4">
      <span class="text-xs font-semibold text-yulda-gray-400">{{ t(`marketplace.category.${listing.category}`) }}</span>
      <h3 class="line-clamp-2 text-sm font-bold text-yulda-black">{{ listing.title }}</h3>
      <p class="mt-auto text-base font-extrabold text-yulda-black">
        <span v-if="isFree" class="text-yulda-gold">{{ t("marketplace.category.FREE") }}</span>
        <span v-else>{{ formatKrw(listing.price) }}</span>
      </p>
      <div class="flex items-center justify-between text-xs text-yulda-gray-400">
        <span v-if="listing.city">{{ listing.city }}</span>
        <span
          v-if="listing.status !== 'ACTIVE'"
          class="rounded-full bg-yulda-gray-100 px-2 py-0.5 font-semibold text-yulda-gray-600"
        >
          {{ t(`marketplace.status.${listing.status}`) }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>
