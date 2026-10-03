<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { Package, Search } from "lucide-vue-next";

import CargoCategoryPicker from "@/components/cargo/CargoCategoryPicker.vue";
import CargoPostCard from "@/components/cargo/CargoPostCard.vue";
import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import PlaceAutocomplete from "@/components/common/PlaceAutocomplete.vue";
import PriceInput from "@/components/common/PriceInput.vue";
import RouteStopsBuilder from "@/components/route/RouteStopsBuilder.vue";
import { useAuthStore } from "@/stores/authStore";
import { useCargoStore } from "@/stores/cargoStore";
import type { CargoCategory, CargoPostType } from "@/types/cargo";
import type { RouteStop } from "@/types/route";

const { t } = useI18n();
const auth = useAuthStore();
const store = useCargoStore();

const activeTab = ref<"search" | "post">("search");

const searchForm = reactive({ fromCity: "", toCity: "", date: "" });
const hasSearched = ref(false);

async function runSearch() {
  hasSearched.value = true;
  await store.search({
    from_city: searchForm.fromCity || undefined,
    to_city: searchForm.toCity || undefined,
    date: searchForm.date ? new Date(searchForm.date).toISOString() : undefined,
  });
}

const postForm = reactive({
  post_type: "OFFER" as CargoPostType,
  stops: [
    { name: "", country: "KR" },
    { name: "", country: "UZ" },
  ] as RouteStop[],
  departure_at: "",
  accepted_categories: [] as CargoCategory[],
  rejected_categories: [] as CargoCategory[],
  max_weight_kg: "",
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
      accepted_categories: postForm.accepted_categories,
      rejected_categories: postForm.rejected_categories,
      max_weight_kg: postForm.max_weight_kg ? Number(postForm.max_weight_kg) : undefined,
      price_note: postForm.price_note || undefined,
      notes: postForm.notes || undefined,
      contact_phone: postForm.contact_phone,
    });
    submitSuccess.value = true;
    postForm.stops = [
      { name: "", country: "KR" },
      { name: "", country: "UZ" },
    ];
    postForm.departure_at = "";
    postForm.accepted_categories = [];
    postForm.rejected_categories = [];
    postForm.max_weight_kg = "";
    postForm.price_note = "";
    postForm.notes = "";
  } finally {
    isSubmitting.value = false;
  }
}

function selectTab(tab: "search" | "post") {
  if (tab === "post" && !auth.isAuthenticated) {
    window.location.href = "/login?redirect=/delivery";
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
        <Package class="h-5 w-5" />
      </div>
      <div>
        <h1 class="text-xl font-bold text-yulda-black">{{ t("cargo.pageTitle") }}</h1>
        <p class="text-sm text-yulda-gray-500">{{ t("cargo.pageSubtitle") }}</p>
      </div>
    </div>

    <div class="mt-6 flex gap-2 border-b border-yulda-gray-100">
      <button
        class="border-b-2 px-4 py-2.5 text-sm font-semibold transition-colors"
        :class="activeTab === 'search' ? 'border-yulda-black text-yulda-black' : 'border-transparent text-yulda-gray-400 hover:text-yulda-gray-600'"
        @click="selectTab('search')"
      >
        {{ t("cargo.searchTab") }}
      </button>
      <button
        class="border-b-2 px-4 py-2.5 text-sm font-semibold transition-colors"
        :class="activeTab === 'post' ? 'border-yulda-black text-yulda-black' : 'border-transparent text-yulda-gray-400 hover:text-yulda-gray-600'"
        @click="selectTab('post')"
      >
        {{ t("cargo.postTab") }}
      </button>
    </div>

    <!-- SEARCH TAB -->
    <div v-if="activeTab === 'search'" class="mt-6">
      <div class="card flex flex-col gap-3 p-5 sm:flex-row sm:items-end">
        <div class="flex-1">
          <label class="label">{{ t("cargo.fromCity") }}</label>
          <PlaceAutocomplete v-model="searchForm.fromCity" :placeholder="t('cargo.fromCity')" />
        </div>
        <div class="flex-1">
          <label class="label">{{ t("cargo.toCity") }}</label>
          <PlaceAutocomplete v-model="searchForm.toCity" :placeholder="t('cargo.toCity')" />
        </div>
        <div class="w-full sm:w-44">
          <BaseInput v-model="searchForm.date" type="date" :label="t('cargo.date')" />
        </div>
        <BaseButton class="sm:w-auto" :loading="store.isLoading" @click="runSearch">
          <Search class="h-4 w-4" />
          {{ t("cargo.search") }}
        </BaseButton>
      </div>

      <div v-if="store.isLoading" class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div v-for="i in 4" :key="i" class="card h-48 animate-pulse bg-yulda-gray-100" />
      </div>

      <template v-else-if="hasSearched">
        <div v-if="store.items.length === 0" class="card mt-6 p-10 text-center text-sm text-yulda-gray-500">
          {{ searchForm.date ? t("cargo.noResultsForDate") : t("cargo.noResults") }}
        </div>
        <div v-else class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <CargoPostCard v-for="post in store.items" :key="post.id" :post="post" />
        </div>

        <template v-if="store.suggestedOtherDates.length > 0">
          <p class="mt-8 text-sm font-semibold text-yulda-black">{{ t("cargo.suggestedOtherDates") }}</p>
          <div class="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <CargoPostCard v-for="post in store.suggestedOtherDates" :key="post.id" :post="post" />
          </div>
        </template>
      </template>
    </div>

    <!-- POST TAB -->
    <div v-else class="mt-6">
      <form class="card flex flex-col gap-4 p-6" @submit.prevent="handleSubmit">
        <div>
          <label class="label">{{ t("cargo.postTypeLabel") }}</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="type in (['OFFER', 'REQUEST'] as CargoPostType[])"
              :key="type"
              type="button"
              class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
              :class="postForm.post_type === type ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
              @click="postForm.post_type = type"
            >
              {{ t(`cargo.postType.${type}`) }}
            </button>
          </div>
        </div>

        <div>
          <label class="label">{{ t("cargo.routeLabel") }}</label>
          <RouteStopsBuilder v-model="postForm.stops" />
        </div>

        <BaseInput v-model="postForm.departure_at" type="datetime-local" :label="t('cargo.departureLabel')" required />

        <CargoCategoryPicker v-model="postForm.accepted_categories" :label="t('cargo.acceptedCategories')" />
        <CargoCategoryPicker v-model="postForm.rejected_categories" :label="t('cargo.rejectedCategories')" />

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <BaseInput v-model="postForm.max_weight_kg" type="number" :label="t('cargo.maxWeight')" :placeholder="t('cargo.maxWeightPlaceholder')" />
          <PriceInput v-model="postForm.price_note" :label="t('cargo.priceNote')" :placeholder="t('cargo.priceNotePlaceholder')" />
        </div>

        <BaseTextarea v-model="postForm.notes" :label="t('cargo.notes')" :placeholder="t('cargo.notesPlaceholder')" :rows="3" />
        <BaseInput v-model="postForm.contact_phone" :label="t('cargo.contactPhone')" :placeholder="t('cargo.contactPhonePlaceholder')" required />

        <p v-if="submitSuccess" class="rounded-xl bg-green-50 px-4 py-3 text-sm text-green-700">
          {{ t("cargo.publish") }} ✓
        </p>

        <BaseButton type="submit" full-width :disabled="!canSubmit" :loading="isSubmitting">
          {{ t("cargo.publish") }}
        </BaseButton>
      </form>
    </div>
  </div>
</template>
