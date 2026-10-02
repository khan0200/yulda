<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { MapPin, Phone, Weight } from "lucide-vue-next";

import type { CargoPost } from "@/types/cargo";

const props = defineProps<{ post: CargoPost }>();
const { t, d } = useI18n();

const routeLabel = computed(() => props.post.stops.map((s) => s.name).join(" → "));
const departureDate = computed(() => new Date(props.post.departure_at));
const isExpired = computed(() => props.post.status === "EXPIRED");
</script>

<template>
  <div class="card flex flex-col gap-3 p-5" :class="{ 'opacity-60': isExpired }">
    <div class="flex items-center justify-between">
      <span
        class="inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold"
        :class="post.post_type === 'OFFER' ? 'bg-yulda-yellow/15 text-yulda-black' : 'bg-yulda-gray-100 text-yulda-gray-700'"
      >
        {{ t(`cargo.postType.${post.post_type}`) }}
      </span>
      <span v-if="isExpired" class="rounded-full bg-yulda-gray-100 px-2.5 py-1 text-xs font-semibold text-yulda-gray-500">
        {{ t("cargo.status.EXPIRED") }}
      </span>
    </div>

    <div class="flex items-start gap-2">
      <MapPin class="mt-0.5 h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
      <p class="text-sm font-bold leading-snug text-yulda-black">{{ routeLabel }}</p>
    </div>

    <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-yulda-gray-600">
      <span>{{ d(departureDate, { year: "numeric", month: "short", day: "numeric" } as never) }}</span>
      <span v-if="post.max_weight_kg" class="flex items-center gap-1">
        <Weight class="h-3.5 w-3.5" />
        {{ post.max_weight_kg }} kg
      </span>
    </div>

    <div v-if="post.accepted_categories.length > 0" class="flex flex-wrap gap-1.5">
      <span
        v-for="category in post.accepted_categories"
        :key="category"
        class="rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700"
      >
        {{ t(`cargo.category.${category}`) }}
      </span>
    </div>
    <div v-if="post.rejected_categories.length > 0" class="flex flex-wrap gap-1.5">
      <span
        v-for="category in post.rejected_categories"
        :key="category"
        class="rounded-full bg-red-50 px-2 py-0.5 text-xs font-medium text-red-600 line-through"
      >
        {{ t(`cargo.category.${category}`) }}
      </span>
    </div>

    <p v-if="post.price_note" class="text-sm font-semibold text-yulda-black">{{ post.price_note }}</p>
    <p v-if="post.notes" class="text-sm text-yulda-gray-500">{{ post.notes }}</p>

    <div class="mt-1 flex items-center justify-between border-t border-yulda-gray-100 pt-3">
      <span class="text-xs text-yulda-gray-400">{{ t("cargo.postedBy") }} {{ post.owner.name }}</span>
      <a :href="`tel:${post.contact_phone}`" class="btn-primary !px-4 !py-2 text-sm">
        <Phone class="h-3.5 w-3.5" />
        {{ t("cargo.call") }}
      </a>
    </div>
  </div>
</template>
