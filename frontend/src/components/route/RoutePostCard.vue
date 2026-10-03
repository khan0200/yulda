<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { Calendar, Car, Clock, MapPin, MessageSquare, Package, Phone, User, Users } from "lucide-vue-next";

import type { RoutePost } from "@/types/route";
import { formatDateOnly, formatPriceNote, formatTimeOnly } from "@/utils/format";

const props = defineProps<{ post: RoutePost }>();
const { t } = useI18n();

const routeLabel = computed(() => props.post.stops.map((s) => s.name).join(" → "));
const isExpired = computed(() => props.post.status === "EXPIRED");
const dateStr = computed(() => formatDateOnly(props.post.departure_at));
const timeStr = computed(() => formatTimeOnly(props.post.departure_at));
</script>

<template>
  <div
    class="card relative flex flex-col justify-between overflow-hidden rounded-2xl border border-yulda-gray-200/90 bg-white p-5 shadow-card transition-all duration-300 hover:-translate-y-1 hover:border-yulda-yellow/70 hover:shadow-card-hover"
    :class="{ 'opacity-60': isExpired }"
  >
    <div class="space-y-3.5">
      <!-- Top Row: Post Type Badge & Price -->
      <div class="flex items-center justify-between gap-2">
        <span
          class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold shadow-2xs"
          :class="post.post_type === 'OFFER' ? 'bg-amber-50 text-amber-900 ring-1 ring-amber-300/70' : 'bg-blue-50 text-blue-900 ring-1 ring-blue-300/70'"
        >
          <Car v-if="post.post_type === 'OFFER'" class="h-3.5 w-3.5 text-amber-600" />
          <Users v-else class="h-3.5 w-3.5 text-blue-600" />
          <span>{{ t(`route.postType.${post.post_type}`) }}</span>
        </span>

        <!-- Price Badge (Prominent top-right) -->
        <div v-if="post.price_note">
          <span class="inline-flex items-center rounded-xl bg-yulda-yellow/20 px-3 py-1 text-sm font-extrabold text-yulda-black ring-1 ring-yulda-yellow/50 shadow-2xs">
            {{ formatPriceNote(post.price_note) }}
          </span>
        </div>
      </div>

      <!-- Route Path -->
      <div class="flex items-start gap-2.5 pt-0.5">
        <div class="mt-0.5 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-lg bg-yulda-gray-100 text-yulda-black">
          <MapPin class="h-3.5 w-3.5 text-emerald-600" />
        </div>
        <p class="text-sm font-extrabold leading-snug text-yulda-black">
          {{ routeLabel }}
        </p>
      </div>

      <!-- Date & Time Chips (Alohida: Sana va Soat) -->
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <!-- Sana chip -->
        <div class="inline-flex items-center gap-1.5 rounded-xl border border-yulda-gray-200 bg-yulda-gray-50/80 px-2.5 py-1 font-semibold text-yulda-gray-800 shadow-3xs">
          <Calendar class="h-3.5 w-3.5 text-yulda-gray-500" />
          <span>{{ dateStr }}</span>
        </div>

        <!-- Soat chip -->
        <div class="inline-flex items-center gap-1.5 rounded-xl border border-yulda-gray-200 bg-yulda-gray-50/80 px-2.5 py-1 font-semibold text-yulda-gray-800 shadow-3xs">
          <Clock class="h-3.5 w-3.5 text-amber-600" />
          <span>{{ timeStr }}</span>
        </div>
      </div>

      <!-- Vehicle, Seats & Cargo Info Chips -->
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <span
          v-if="post.vehicle_info"
          class="inline-flex items-center gap-1.5 rounded-xl border border-yulda-gray-200 bg-white px-2.5 py-1 font-medium text-yulda-gray-700 shadow-3xs"
        >
          <Car class="h-3.5 w-3.5 text-yulda-gray-500" />
          <span>{{ post.vehicle_info }}</span>
        </span>

        <span
          v-if="post.seats !== null"
          class="inline-flex items-center gap-1.5 rounded-xl border border-yulda-gray-200 bg-white px-2.5 py-1 font-medium text-yulda-gray-700 shadow-3xs"
        >
          <Users class="h-3.5 w-3.5 text-yulda-gray-500" />
          <span>{{ post.seats }} {{ t("route.seatsShort") }}</span>
        </span>

        <span
          v-if="post.has_cargo_space"
          class="inline-flex items-center gap-1.5 rounded-xl border border-emerald-200 bg-emerald-50/70 px-2.5 py-1 font-medium text-emerald-800 shadow-3xs"
        >
          <Package class="h-3.5 w-3.5 text-emerald-600" />
          <span>{{ t("route.hasCargoSpace") }}</span>
        </span>
      </div>

      <!-- Notes (if any) -->
      <div v-if="post.notes" class="flex items-start gap-1.5 rounded-xl bg-yulda-gray-50 p-2.5 text-xs text-yulda-gray-600 border border-yulda-gray-100">
        <MessageSquare class="mt-0.5 h-3.5 w-3.5 flex-shrink-0 text-yulda-gray-400" />
        <p class="line-clamp-2 leading-relaxed">{{ post.notes }}</p>
      </div>
    </div>

    <!-- Footer Row: Author & Call Action -->
    <div class="mt-4 flex items-center justify-between border-t border-yulda-gray-100 pt-3">
      <div class="flex items-center gap-2">
        <div class="flex h-7 w-7 items-center justify-center rounded-full bg-yulda-gray-100 text-yulda-gray-700 border border-yulda-gray-200">
          <User class="h-3.5 w-3.5 text-yulda-gray-500" />
        </div>
        <div class="truncate">
          <span class="text-[10px] font-bold text-yulda-gray-400 block leading-none">Joylagan</span>
          <span class="text-xs font-bold text-yulda-black truncate">{{ post.owner.name }}</span>
        </div>
      </div>

      <a
        :href="`tel:${post.contact_phone}`"
        class="btn-primary !px-4 !py-2 text-xs font-bold shadow-md transition-all hover:scale-105 active:scale-95 flex items-center gap-1.5"
      >
        <Phone class="h-3.5 w-3.5" />
        <span>{{ t("route.call") }}</span>
      </a>
    </div>
  </div>
</template>