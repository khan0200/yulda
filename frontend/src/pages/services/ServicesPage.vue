<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { Search, Sparkles } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import PhotoUploader from "@/components/common/PhotoUploader.vue";
import PriceInput from "@/components/common/PriceInput.vue";
import ServicePostCard from "@/components/services/ServicePostCard.vue";
import { favoriteApi } from "@/services/favoriteApi";
import { useAuthStore } from "@/stores/authStore";
import { useServiceStore } from "@/stores/serviceStore";
import type { ServiceCategory } from "@/types/service";

const { t } = useI18n();
const auth = useAuthStore();
const store = useServiceStore();

const categories: ServiceCategory[] = [
  "BEAUTY", "REPAIR", "TUTORING", "CLEANING", "MOVING",
  "PET_CARE", "PHOTOGRAPHY", "DESIGN", "TRANSLATION", "LEGAL_ADMIN", "EVENT", "OTHER",
];

const activeTab = ref<"search" | "post">("search");
const likedIds = ref<Set<string>>(new Set());

const searchForm = reactive({ category: "" as ServiceCategory | "", city: "" });
const hasSearched = ref(false);

async function loadLikedIds() {
  if (!auth.isAuthenticated) return;
  try {
    likedIds.value = new Set(await favoriteApi.listMine("SERVICES"));
  } catch {
    likedIds.value = new Set();
  }
}

async function runSearch() {
  hasSearched.value = true;
  await store.fetchPosts({
    category: searchForm.category || undefined,
    city: searchForm.city || undefined,
    page_size: 24,
  });
}

const postForm = reactive({
  category: "BEAUTY" as ServiceCategory,
  title: "",
  description: "",
  price_note: "",
  city: "",
  photos: [] as string[],
  contact_value: "",
});
const isSubmitting = ref(false);
const submitSuccess = ref(false);

const canSubmit = computed(() => {
  return postForm.title.trim() && postForm.description.trim() && postForm.contact_value.trim();
});

async function handleSubmit() {
  if (!canSubmit.value) return;
  isSubmitting.value = true;
  submitSuccess.value = false;
  try {
    await store.createPost({
      category: postForm.category,
      title: postForm.title,
      description: postForm.description,
      price_note: postForm.price_note || undefined,
      city: postForm.city || undefined,
      photos: postForm.photos,
      contact_value: postForm.contact_value,
    });
    submitSuccess.value = true;
    postForm.title = "";
    postForm.description = "";
    postForm.price_note = "";
    postForm.city = "";
    postForm.photos = [];
    postForm.contact_value = "";
  } finally {
    isSubmitting.value = false;
  }
}

function selectTab(tab: "search" | "post") {
  if (tab === "post" && !auth.isAuthenticated) {
    window.location.href = "/login?redirect=/services";
    return;
  }
  activeTab.value = tab;
}

onMounted(() => {
  runSearch();
  loadLikedIds();
});
</script>

<template>
  <div class="mx-auto max-w-4xl px-6 py-10">
    <div class="flex items-center gap-3">
      <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-yulda-yellow/15 text-yulda-black">
        <Sparkles class="h-5 w-5" />
      </div>
      <div>
        <h1 class="text-xl font-bold text-yulda-black">{{ t("services.pageTitle") }}</h1>
        <p class="text-sm text-yulda-gray-500">{{ t("services.pageSubtitle") }}</p>
      </div>
    </div>

    <div class="mt-6 flex gap-2 border-b border-yulda-gray-100">
      <button
        class="border-b-2 px-4 py-2.5 text-sm font-semibold transition-colors"
        :class="activeTab === 'search' ? 'border-yulda-black text-yulda-black' : 'border-transparent text-yulda-gray-400 hover:text-yulda-gray-600'"
        @click="selectTab('search')"
      >
        {{ t("services.searchTab") }}
      </button>
      <button
        class="border-b-2 px-4 py-2.5 text-sm font-semibold transition-colors"
        :class="activeTab === 'post' ? 'border-yulda-black text-yulda-black' : 'border-transparent text-yulda-gray-400 hover:text-yulda-gray-600'"
        @click="selectTab('post')"
      >
        {{ t("services.postTab") }}
      </button>
    </div>

    <!-- SEARCH TAB -->
    <div v-if="activeTab === 'search'" class="mt-6">
      <div class="card flex flex-wrap items-end gap-3 p-5">
        <div class="w-48">
          <label class="label">{{ t("services.category.label") }}</label>
          <select v-model="searchForm.category" class="input">
            <option value="">{{ t("services.category.all") }}</option>
            <option v-for="c in categories" :key="c" :value="c">{{ t(`services.category.${c}`) }}</option>
          </select>
        </div>
        <div class="w-40">
          <label class="label">{{ t("services.city") }}</label>
          <input v-model="searchForm.city" type="text" class="input" />
        </div>
        <BaseButton :loading="store.isLoading" @click="runSearch">
          <Search class="h-4 w-4" />
          {{ t("services.searchTab") }}
        </BaseButton>
      </div>

      <div v-if="store.isLoading" class="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        <div v-for="i in 8" :key="i" class="card aspect-[3/4] animate-pulse bg-yulda-gray-100" />
      </div>

      <template v-else-if="hasSearched">
        <div v-if="store.posts.length === 0" class="card mt-6 p-10 text-center text-sm text-yulda-gray-500">
          {{ t("services.noResults") }}
        </div>
        <div v-else class="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          <ServicePostCard v-for="post in store.posts" :key="post.id" :post="post" :liked="likedIds.has(post.id)" />
        </div>
      </template>
    </div>

    <!-- POST TAB -->
    <div v-else class="mt-6">
      <form class="card flex flex-col gap-4 p-6" @submit.prevent="handleSubmit">
        <div>
          <label class="label">{{ t("services.category.label") }}</label>
          <select v-model="postForm.category" class="input">
            <option v-for="c in categories" :key="c" :value="c">{{ t(`services.category.${c}`) }}</option>
          </select>
        </div>

        <div>
          <label class="label">{{ t("services.photosLabel") }}</label>
          <PhotoUploader v-model="postForm.photos" folder="community" />
        </div>

        <BaseInput v-model="postForm.title" :label="t('services.titleLabel')" :placeholder="t('services.titlePlaceholder')" required />
        <BaseTextarea v-model="postForm.description" :label="t('services.descriptionLabel')" :placeholder="t('services.descriptionPlaceholder')" :rows="6" required />

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <PriceInput v-model="postForm.price_note" :label="t('services.priceNote')" :placeholder="t('services.priceNotePlaceholder')" />
          <BaseInput v-model="postForm.city" :label="t('services.city')" />
        </div>

        <BaseInput v-model="postForm.contact_value" :label="t('services.contactValueLabel')" :placeholder="t('services.contactValuePlaceholder')" required />

        <p v-if="submitSuccess" class="rounded-xl bg-green-50 px-4 py-3 text-sm text-green-700">
          {{ t("services.publish") }} ✓
        </p>

        <BaseButton type="submit" full-width :disabled="!canSubmit" :loading="isSubmitting">
          {{ t("services.publish") }}
        </BaseButton>
      </form>
    </div>
  </div>
</template>
