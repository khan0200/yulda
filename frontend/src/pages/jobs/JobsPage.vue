<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { Briefcase, Search } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import PhotoUploader from "@/components/common/PhotoUploader.vue";
import JobPostCard from "@/components/jobs/JobPostCard.vue";
import { favoriteApi } from "@/services/favoriteApi";
import { useAuthStore } from "@/stores/authStore";
import { useJobStore } from "@/stores/jobStore";
import type { JobCategory, JobEmploymentType, JobPayType, JobPostType } from "@/types/job";

const { t } = useI18n();
const auth = useAuthStore();
const store = useJobStore();

const categories: JobCategory[] = [
  "RESTAURANT_CAFE", "RETAIL", "DELIVERY_LOGISTICS", "CONSTRUCTION_FACTORY",
  "CLEANING", "CARE_CHILDCARE", "OFFICE_ADMIN", "IT_DESIGN",
  "EDUCATION_TUTORING", "TRANSLATION", "EVENT_PROMOTION", "OTHER",
];
const employmentTypes: JobEmploymentType[] = ["PART_TIME", "FULL_TIME", "DAILY", "CONTRACT"];
const payTypes: JobPayType[] = ["HOURLY", "DAILY", "MONTHLY", "PER_PROJECT"];

const activeTab = ref<"search" | "post">("search");
const likedIds = ref<Set<string>>(new Set());

const searchForm = reactive({
  postType: "" as JobPostType | "",
  category: "" as JobCategory | "",
  employmentType: "" as JobEmploymentType | "",
  city: "",
});
const hasSearched = ref(false);

async function loadLikedIds() {
  if (!auth.isAuthenticated) return;
  try {
    likedIds.value = new Set(await favoriteApi.listMine("JOBS"));
  } catch {
    likedIds.value = new Set();
  }
}

async function runSearch() {
  hasSearched.value = true;
  await store.fetchPosts({
    post_type: searchForm.postType || undefined,
    category: searchForm.category || undefined,
    employment_type: searchForm.employmentType || undefined,
    city: searchForm.city || undefined,
    page_size: 24,
  });
}

const postForm = reactive({
  post_type: "OFFER" as JobPostType,
  category: "RESTAURANT_CAFE" as JobCategory,
  employment_type: "PART_TIME" as JobEmploymentType,
  title: "",
  description: "",
  pay_type: "" as JobPayType | "",
  pay_amount: "",
  city: "",
  requires_korean: false,
  visa_sponsorship: false,
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
      post_type: postForm.post_type,
      category: postForm.category,
      employment_type: postForm.employment_type,
      title: postForm.title,
      description: postForm.description,
      pay_type: postForm.pay_type || undefined,
      pay_amount: postForm.pay_amount ? Number(postForm.pay_amount) : undefined,
      city: postForm.city || undefined,
      requires_korean: postForm.requires_korean,
      visa_sponsorship: postForm.visa_sponsorship,
      photos: postForm.photos,
      contact_value: postForm.contact_value,
    });
    submitSuccess.value = true;
    postForm.title = "";
    postForm.description = "";
    postForm.pay_type = "";
    postForm.pay_amount = "";
    postForm.city = "";
    postForm.requires_korean = false;
    postForm.visa_sponsorship = false;
    postForm.photos = [];
    postForm.contact_value = "";
  } finally {
    isSubmitting.value = false;
  }
}

function selectTab(tab: "search" | "post") {
  if (tab === "post" && !auth.isAuthenticated) {
    window.location.href = "/login?redirect=/jobs";
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
        <Briefcase class="h-5 w-5" />
      </div>
      <div>
        <h1 class="text-xl font-bold text-yulda-black">{{ t("jobs.pageTitle") }}</h1>
        <p class="text-sm text-yulda-gray-500">{{ t("jobs.pageSubtitle") }}</p>
      </div>
    </div>

    <div class="mt-6 flex gap-2 border-b border-yulda-gray-100">
      <button
        class="border-b-2 px-4 py-2.5 text-sm font-semibold transition-colors"
        :class="activeTab === 'search' ? 'border-yulda-black text-yulda-black' : 'border-transparent text-yulda-gray-400 hover:text-yulda-gray-600'"
        @click="selectTab('search')"
      >
        {{ t("jobs.searchTab") }}
      </button>
      <button
        class="border-b-2 px-4 py-2.5 text-sm font-semibold transition-colors"
        :class="activeTab === 'post' ? 'border-yulda-black text-yulda-black' : 'border-transparent text-yulda-gray-400 hover:text-yulda-gray-600'"
        @click="selectTab('post')"
      >
        {{ t("jobs.postTab") }}
      </button>
    </div>

    <!-- SEARCH TAB -->
    <div v-if="activeTab === 'search'" class="mt-6">
      <div class="card flex flex-col gap-3 p-5">
        <div class="flex flex-wrap gap-2">
          <button
            v-for="type in (['OFFER', 'REQUEST'] as JobPostType[])"
            :key="type"
            type="button"
            class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
            :class="searchForm.postType === type ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
            @click="searchForm.postType = searchForm.postType === type ? '' : type"
          >
            {{ t(`jobs.postType.${type}`) }}
          </button>
        </div>

        <div class="flex flex-wrap items-end gap-3">
          <div class="w-44">
            <label class="label">{{ t("jobs.category.label") }}</label>
            <select v-model="searchForm.category" class="input">
              <option value="">{{ t("jobs.category.all") }}</option>
              <option v-for="c in categories" :key="c" :value="c">{{ t(`jobs.category.${c}`) }}</option>
            </select>
          </div>
          <div class="w-40">
            <label class="label">{{ t("jobs.employmentType.label") }}</label>
            <select v-model="searchForm.employmentType" class="input">
              <option value="">{{ t("jobs.employmentType.all") }}</option>
              <option v-for="e in employmentTypes" :key="e" :value="e">{{ t(`jobs.employmentType.${e}`) }}</option>
            </select>
          </div>
          <div class="w-36">
            <label class="label">{{ t("jobs.city") }}</label>
            <input v-model="searchForm.city" type="text" class="input" />
          </div>
          <BaseButton :loading="store.isLoading" @click="runSearch">
            <Search class="h-4 w-4" />
            {{ t("jobs.searchTab") }}
          </BaseButton>
        </div>
      </div>

      <div v-if="store.isLoading" class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div v-for="i in 4" :key="i" class="card h-48 animate-pulse bg-yulda-gray-100" />
      </div>

      <template v-else-if="hasSearched">
        <div v-if="store.posts.length === 0" class="card mt-6 p-10 text-center text-sm text-yulda-gray-500">
          {{ t("jobs.noResults") }}
        </div>
        <div v-else class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <JobPostCard v-for="post in store.posts" :key="post.id" :post="post" :liked="likedIds.has(post.id)" />
        </div>
      </template>
    </div>

    <!-- POST TAB -->
    <div v-else class="mt-6">
      <form class="card flex flex-col gap-4 p-6" @submit.prevent="handleSubmit">
        <div>
          <label class="label">{{ t("jobs.postTypeLabel") }}</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="type in (['OFFER', 'REQUEST'] as JobPostType[])"
              :key="type"
              type="button"
              class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
              :class="postForm.post_type === type ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
              @click="postForm.post_type = type"
            >
              {{ t(`jobs.postType.${type}`) }}
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label class="label">{{ t("jobs.category.label") }}</label>
            <select v-model="postForm.category" class="input">
              <option v-for="c in categories" :key="c" :value="c">{{ t(`jobs.category.${c}`) }}</option>
            </select>
          </div>
          <div>
            <label class="label">{{ t("jobs.employmentType.label") }}</label>
            <select v-model="postForm.employment_type" class="input">
              <option v-for="e in employmentTypes" :key="e" :value="e">{{ t(`jobs.employmentType.${e}`) }}</option>
            </select>
          </div>
        </div>

        <BaseInput v-model="postForm.title" :label="t('jobs.titleLabel')" :placeholder="t('jobs.titlePlaceholder')" required />
        <BaseTextarea v-model="postForm.description" :label="t('jobs.descriptionLabel')" :placeholder="t('jobs.descriptionPlaceholder')" :rows="6" required />

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label class="label">{{ t("jobs.payType.label") }}</label>
            <select v-model="postForm.pay_type" class="input">
              <option value="">—</option>
              <option v-for="p in payTypes" :key="p" :value="p">{{ t(`jobs.payType.${p}`) }}</option>
            </select>
          </div>
          <BaseInput v-model="postForm.pay_amount" type="number" :label="t('jobs.payAmount')" :placeholder="t('jobs.payAmountPlaceholder')" />
        </div>

        <BaseInput v-model="postForm.city" :label="t('jobs.city')" />

        <label class="flex items-center gap-2 text-sm text-yulda-gray-700">
          <input v-model="postForm.requires_korean" type="checkbox" class="h-4 w-4 rounded border-yulda-gray-300" />
          {{ t("jobs.requiresKorean") }}
        </label>
        <label class="flex items-center gap-2 text-sm text-yulda-gray-700">
          <input v-model="postForm.visa_sponsorship" type="checkbox" class="h-4 w-4 rounded border-yulda-gray-300" />
          {{ t("jobs.visaSponsorship") }}
        </label>

        <div>
          <label class="label">{{ t("jobs.photosLabel") }}</label>
          <PhotoUploader v-model="postForm.photos" folder="community" />
        </div>

        <BaseInput v-model="postForm.contact_value" :label="t('jobs.contactValueLabel')" :placeholder="t('jobs.contactValuePlaceholder')" required />

        <p v-if="submitSuccess" class="rounded-xl bg-green-50 px-4 py-3 text-sm text-green-700">
          {{ t("jobs.publish") }} ✓
        </p>

        <BaseButton type="submit" full-width :disabled="!canSubmit" :loading="isSubmitting">
          {{ t("jobs.publish") }}
        </BaseButton>
      </form>
    </div>
  </div>
</template>
