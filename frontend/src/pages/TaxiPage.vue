<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { Car, Search } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import DatePicker from "@/components/common/DatePicker.vue";
import DateTimePicker from "@/components/common/DateTimePicker.vue";
import InteractiveMap from "@/components/common/InteractiveMap.vue";
import PlaceAutocomplete from "@/components/common/PlaceAutocomplete.vue";
import PriceInput from "@/components/common/PriceInput.vue";
import VehicleAutocomplete from "@/components/common/VehicleAutocomplete.vue";
import RoutePostCard from "@/components/route/RoutePostCard.vue";
import RouteStopsBuilder from "@/components/route/RouteStopsBuilder.vue";
import { useAuthStore } from "@/stores/authStore";
import { useRouteStore } from "@/stores/routeStore";
import type { RoutePostType } from "@/types/route";
import type { RouteStop } from "@/types/route";
import type { GeocodedLocation } from "@/utils/geo";

const { t } = useI18n();
const auth = useAuthStore();
const store = useRouteStore();

const activeTab = ref<"search" | "post">("search");

// YYYY-MM-DD  /  YYYY-MM-DDTHH:MM  helpers
function pad(n: number) { return String(n).padStart(2, "0"); }
const _now = new Date();
const todayDate = `${_now.getFullYear()}-${pad(_now.getMonth() + 1)}-${pad(_now.getDate())}`;
const todayDatetime = `${todayDate}T${pad(_now.getHours())}:${pad(_now.getMinutes())}`;

const searchForm = reactive({ fromCity: "", toCity: "", date: "" });
const hasSearched = ref(false);

const searchRouteStops = computed(() => {
  const list: Array<{ name: string }> = [];
  if (searchForm.fromCity.trim()) list.push({ name: searchForm.fromCity.trim() });
  if (searchForm.toCity.trim()) list.push({ name: searchForm.toCity.trim() });
  return list;
});

function handleLocationSelected(loc: GeocodedLocation) {
  const name = loc.city || loc.name;
  if (!searchForm.fromCity.trim()) {
    searchForm.fromCity = name;
  } else {
    searchForm.toCity = name;
  }
}

async function runSearch() {
  hasSearched.value = true;
  await store.search({
    from_city: searchForm.fromCity || undefined,
    to_city: searchForm.toCity || undefined,
    date: searchForm.date ? new Date(searchForm.date).toISOString() : undefined,
  });
}

const postForm = reactive({
  post_type: "OFFER" as RoutePostType,
  stops: [
    { name: "", country: "KR" },
    { name: "", country: "KR" },
  ] as RouteStop[],
  departure_at: todayDatetime,
  vehicle_info: "",
  seats: "",
  has_cargo_space: false,
  price_note: "",
  notes: "",
  contact_phone: "",
});
const isSubmitting = ref(false);
const submitSuccess = ref(false);

const canSubmit = computed(() => {
  return (
    postForm.stops.length >= 2 &&
    postForm.stops.every((s) => s.name.trim()) &&
    postForm.departure_at &&
    postForm.contact_phone.trim()
  );
});

async function handleSubmit() {
  if (!canSubmit.value) return;
  isSubmitting.value = true;
  submitSuccess.value = false;
  try {
    await store.createPost({
      post_type: postForm.post_type,
      stops: postForm.stops,
      departure_at: new Date(postForm.departure_at).toISOString(),
      vehicle_info: postForm.vehicle_info || undefined,
      seats: postForm.seats ? Number(postForm.seats) : undefined,
      has_cargo_space: postForm.has_cargo_space,
      price_note: postForm.price_note || undefined,
      notes: postForm.notes || undefined,
      contact_phone: postForm.contact_phone,
    });
    submitSuccess.value = true;
    postForm.stops = [
      { name: "", country: "KR" },
      { name: "", country: "KR" },
    ];
    postForm.departure_at = "";
    postForm.vehicle_info = "";
    postForm.seats = "";
    postForm.has_cargo_space = false;
    postForm.price_note = "";
    postForm.notes = "";
  } finally {
    isSubmitting.value = false;
  }
}

function selectTab(tab: "search" | "post") {
  if (tab === "post" && !auth.isAuthenticated) {
    window.location.href = "/login?redirect=/taxi";
    return;
  }
  activeTab.value = tab;
}

onMounted(() => runSearch());
</script>

<template>
  <div class="mx-auto max-w-4xl px-6 py-10">
    <div class="flex items-center gap-3">
      <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-yulda-yellow/15 text-yulda-black">
        <Car class="h-5 w-5" />
      </div>
      <div>
        <h1 class="text-xl font-bold text-yulda-black">{{ t("route.pageTitle") }}</h1>
        <p class="text-sm text-yulda-gray-500">{{ t("route.pageSubtitle") }}</p>
      </div>
    </div>

    <div class="mt-6 flex gap-2 border-b border-yulda-gray-100">
      <button
        class="border-b-2 px-4 py-2.5 text-sm font-semibold transition-colors"
        :class="activeTab === 'search' ? 'border-yulda-black text-yulda-black' : 'border-transparent text-yulda-gray-400 hover:text-yulda-gray-600'"
        @click="selectTab('search')"
      >
        {{ t("route.searchTab") }}
      </button>
      <button
        class="border-b-2 px-4 py-2.5 text-sm font-semibold transition-colors"
        :class="activeTab === 'post' ? 'border-yulda-black text-yulda-black' : 'border-transparent text-yulda-gray-400 hover:text-yulda-gray-600'"
        @click="selectTab('post')"
      >
        {{ t("route.postTab") }}
      </button>
    </div>

    <!-- SEARCH TAB -->
    <div v-if="activeTab === 'search'" class="mt-6">
      <div class="card flex flex-col gap-3 p-5 sm:flex-row sm:items-end">
        <div class="flex-1">
          <label class="label">{{ t("route.fromCity") }}</label>
          <PlaceAutocomplete v-model="searchForm.fromCity" country="KR" :placeholder="t('route.fromCity')" />
        </div>
        <div class="flex-1">
          <label class="label">{{ t("route.toCity") }}</label>
          <PlaceAutocomplete v-model="searchForm.toCity" country="KR" :placeholder="t('route.toCity')" />
        </div>
        <div class="w-full sm:w-44">
          <DatePicker v-model="searchForm.date" :label="t('route.date')" />
        </div>
        <BaseButton class="sm:w-auto" :loading="store.isLoading" @click="runSearch">
          <Search class="h-4 w-4" />
          {{ t("route.search") }}
        </BaseButton>
      </div>

      <!-- Map route preview for search (Always visible) -->
      <div class="mt-4">
        <InteractiveMap
          :mode="searchRouteStops.length >= 1 ? 'route' : 'picker'"
          :route-stops="searchRouteStops"
          :label="searchRouteStops.length >= 2 ? undefined : searchForm.fromCity ? `A: ${searchForm.fromCity} — endi B nuqtani belgilang` : 'Turgan joyingizni tanlang (A nuqta)'"
          aspect-ratio="16/10"
          @select="handleLocationSelected"
        />
      </div>

      <div v-if="store.isLoading" class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div v-for="i in 4" :key="i" class="card h-40 animate-pulse bg-yulda-gray-100" />
      </div>

      <template v-else-if="hasSearched">
        <div v-if="store.items.length === 0" class="card mt-6 p-10 text-center text-sm text-yulda-gray-500">
          {{ searchForm.date ? t("route.noResultsForDate") : t("route.noResults") }}
        </div>
        <div v-else class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <RoutePostCard v-for="post in store.items" :key="post.id" :post="post" />
        </div>

        <template v-if="store.suggestedOtherDates.length > 0">
          <p class="mt-8 text-sm font-semibold text-yulda-black">{{ t("route.suggestedOtherDates") }}</p>
          <div class="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <RoutePostCard v-for="post in store.suggestedOtherDates" :key="post.id" :post="post" />
          </div>
        </template>
      </template>
    </div>

    <!-- POST TAB -->
    <div v-else class="mt-6">
      <form class="card flex flex-col gap-4 p-6" @submit.prevent="handleSubmit">
        <div>
          <label class="label">{{ t("route.postTypeLabel") }}</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="type in (['OFFER', 'REQUEST'] as RoutePostType[])"
              :key="type"
              type="button"
              class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
              :class="postForm.post_type === type ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
              @click="postForm.post_type = type"
            >
              {{ t(`route.postType.${type}`) }}
            </button>
          </div>
        </div>

        <div>
          <label class="label">{{ t("route.routeLabel") }}</label>
          <RouteStopsBuilder v-model="postForm.stops" fixed-country="KR" />
          <!-- Map preview of driver route stops -->
          <div v-if="postForm.stops.filter((s) => s.name.trim()).length >= 2" class="mt-3">
            <InteractiveMap mode="route" :route-stops="postForm.stops" label="Safar marshruti vizualizatsiyasi" aspect-ratio="16/10" />
          </div>
        </div>

        <div>
          <label class="label">{{ t('route.departureLabel') }} <span class="text-yulda-gold">*</span></label>
          <DateTimePicker v-model="postForm.departure_at" :min="todayDatetime" />
        </div>

        <div v-if="postForm.post_type === 'OFFER'" class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label class="label">{{ t('route.vehicleInfo') }}</label>
            <VehicleAutocomplete v-model="postForm.vehicle_info" :placeholder="t('route.vehicleInfoPlaceholder')" />
          </div>
          <BaseInput v-model="postForm.seats" type="number" :label="t('route.seats')" />
        </div>

        <label class="flex items-center gap-2 text-sm text-yulda-gray-700">
          <input v-model="postForm.has_cargo_space" type="checkbox" class="h-4 w-4 rounded border-yulda-gray-300" />
          {{ t("route.hasCargoSpace") }}
        </label>

        <PriceInput v-model="postForm.price_note" :label="t('route.priceNote')" :placeholder="t('route.priceNotePlaceholder')" />
        <BaseTextarea v-model="postForm.notes" :label="t('route.notes')" :placeholder="t('route.notesPlaceholder')" :rows="3" />
        <BaseInput v-model="postForm.contact_phone" :label="t('route.contactPhone')" :placeholder="t('route.contactPhonePlaceholder')" required />

        <p v-if="submitSuccess" class="rounded-xl bg-green-50 px-4 py-3 text-sm text-green-700">
          {{ t("route.publish") }} ✓
        </p>

        <BaseButton type="submit" full-width :disabled="!canSubmit" :loading="isSubmitting">
          {{ t("route.publish") }}
        </BaseButton>
      </form>
    </div>
  </div>
</template>
