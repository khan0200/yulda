<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { Calendar, Car, MapPin, Package, Phone, Users } from "lucide-vue-next";

import type { RoutePost } from "@/types/route";
import { formatDateTime, formatPriceNote } from "@/utils/format";

const props = defineProps<{ post: RoutePost }>();
const { t } = useI18n();

const routeLabel = computed(() => props.post.stops.map((s) => s.name).join(" → "));
const isExpired = computed(() => props.post.status === "EXPIRED");
</script>

<template>
  <div class="card flex flex-col gap-3.5 p-5 transition-all hover:shadow-card-hover" :class="{ 'opacity-60': isExpired }">
    <div class="flex items-center justify-between">
      <span
        class="inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold"
        :class="post.post_type === 'OFFER' ? 'bg-yulda-yellow/20 text-yulda-black' : 'bg-yulda-gray-100 text-yulda-gray-700'"
      >
        {{ t(`route.postType.${post.post_type}`) }}
      </span>
      <span v-if="isExpired" class="rounded-full bg-yulda-gray-100 px-2.5 py-1 text-xs font-semibold text-yulda-gray-500">
        {{ t("route.status.EXPIRED") }}
      </span>
    </div>

    <!-- Route path -->
    <div class="flex items-start gap-2">
      <MapPin class="mt-0.5 h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
      <p class="text-sm font-bold leading-snug text-yulda-black">{{ routeLabel }}</p>
    </div>

    <!-- Departure date & time -->
    <div class="flex items-center gap-2 text-xs font-medium text-yulda-gray-500">
      <Calendar class="h-3.5 w-3.5 text-yulda-gray-400" />
      <span>{{ formatDateTime(post.departure_at) }}</span>
    </div>

    <!-- Details (Vehicle, Seats, Cargo) -->
    <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-yulda-gray-600">
      <span v-if="post.vehicle_info" class="flex items-center gap-1 font-medium">
        <Car class="h-3.5 w-3.5 text-yulda-gray-400" />
        {{ post.vehicle_info }}
      </span>
      <span v-if="post.seats !== null" class="flex items-center gap-1">
        <Users class="h-3.5 w-3.5 text-yulda-gray-400" />
        {{ post.seats }} {{ t("route.seatsShort") }}
      </span>
      <span v-if="post.has_cargo_space" class="flex items-center gap-1">
        <Package class="h-3.5 w-3.5 text-yulda-gray-400" />
      </span>
    </div>

    <!-- Price note -->
    <div v-if="post.price_note" class="mt-0.5">
      <span class="inline-block rounded-lg bg-yulda-gray-100 px-2.5 py-1 text-sm font-bold text-yulda-black">
        {{ formatPriceNote(post.price_note) }}
      </span>
    </div>

    <p v-if="post.notes" class="text-xs text-yulda-gray-500">{{ post.notes }}</p>

    <!-- Footer -->
    <div class="mt-1 flex items-center justify-between border-t border-yulda-gray-100 pt-3">
      <span class="text-xs text-yulda-gray-400">{{ t("route.postedBy") }} {{ post.owner.name }}</span>
      <a :href="`tel:${post.contact_phone}`" class="btn-primary !px-4 !py-2 text-sm">
        <Phone class="h-3.5 w-3.5" />
        {{ t("route.call") }}
      </a>
    </div>
  </div>
</template>