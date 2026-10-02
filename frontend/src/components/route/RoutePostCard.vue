<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { Car, MapPin, Package, Phone, Users } from "lucide-vue-next";

import type { RoutePost } from "@/types/route";

const props = defineProps<{ post: RoutePost }>();
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
        {{ t(`route.postType.${post.post_type}`) }}
      </span>
      <span v-if="isExpired" class="rounded-full bg-yulda-gray-100 px-2.5 py-1 text-xs font-semibold text-yulda-gray-500">
        {{ t("route.status.EXPIRED") }}
      </span>
    </div>

    <div class="flex items-start gap-2">
      <MapPin class="mt-0.5 h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
      <p class="text-sm font-bold leading-snug text-yulda-black">{{ routeLabel }}</p>
    </div>

    <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-yulda-gray-600">
      <span>{{ d(departureDate, { year: "numeric", month: "short", day: "numeric" } as never) }}</span>
      <span>{{ d(departureDate, { hour: "2-digit", minute: "2-digit" } as never) }}</span>
    </div>

    <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-yulda-gray-600">
      <span v-if="post.vehicle_info" class="flex items-center gap-1">
        <Car class="h-3.5 w-3.5" />
        {{ post.vehicle_info }}
      </span>
      <span v-if="post.seats !== null" class="flex items-center gap-1">
        <Users class="h-3.5 w-3.5" />
        {{ post.seats }} {{ t("route.seatsShort") }}
      </span>
      <span v-if="post.has_cargo_space" class="flex items-center gap-1">
        <Package class="h-3.5 w-3.5" />
      </span>
    </div>

    <p v-if="post.price_note" class="text-sm font-semibold text-yulda-black">{{ post.price_note }}</p>
    <p v-if="post.notes" class="text-sm text-yulda-gray-500">{{ post.notes }}</p>

    <div class="mt-1 flex items-center justify-between border-t border-yulda-gray-100 pt-3">
      <span class="text-xs text-yulda-gray-400">{{ t("route.postedBy") }} {{ post.owner.name }}</span>
      <a :href="`tel:${post.contact_phone}`" class="btn-primary !px-4 !py-2 text-sm">
        <Phone class="h-3.5 w-3.5" />
        {{ t("route.call") }}
      </a>
    </div>
  </div>
</template>
