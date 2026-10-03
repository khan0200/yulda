<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { ArrowLeft, Briefcase, CheckCircle2, MapPin, Trash2 } from "lucide-vue-next";

import LikeButton from "@/components/common/LikeButton.vue";
import { useAuthStore } from "@/stores/authStore";
import { useJobStore } from "@/stores/jobStore";
import { formatKrw } from "@/utils/format";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const store = useJobStore();

const jobId = computed(() => route.params.id as string);
const isOwner = computed(() => {
  return Boolean(auth.user && store.currentPost && store.currentPost.owner.id === auth.user.id);
});
const payLabel = computed(() => {
  if (!store.currentPost?.pay_amount || !store.currentPost?.pay_type) return "";
  return `${formatKrw(store.currentPost.pay_amount)} / ${t(`jobs.payType.${store.currentPost.pay_type}`)}`;
});

async function handleDelete() {
  if (!confirm(t("jobs.confirmDelete"))) return;
  await store.deletePost(jobId.value);
  router.push("/jobs");
}

async function handleMarkClosed() {
  await store.markClosed(jobId.value);
}

onMounted(() => store.fetchPost(jobId.value));
</script>

<template>
  <div class="mx-auto max-w-3xl px-6 py-10">
    <RouterLink to="/jobs" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("jobs.backToFeed") }}
    </RouterLink>

    <div v-if="store.isLoading && !store.currentPost" class="card mt-6 h-96 animate-pulse bg-yulda-gray-100" />

    <template v-else-if="store.currentPost">
      <div class="card mt-6 overflow-hidden">
        <div v-if="store.currentPost.photos.length" class="flex aspect-video items-center justify-center bg-yulda-gray-100">
          <img :src="store.currentPost.photos[0]" :alt="store.currentPost.title" class="h-full w-full object-cover" />
        </div>

        <div class="p-6">
          <div class="flex items-center justify-between">
            <span
              class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold"
              :class="store.currentPost.post_type === 'OFFER' ? 'bg-amber-50 text-amber-900' : 'bg-blue-50 text-blue-900'"
            >
              <Briefcase class="h-3.5 w-3.5" />
              {{ t(`jobs.postType.${store.currentPost.post_type}`) }}
            </span>
            <div class="flex items-center gap-3">
              <LikeButton target-type="JOBS" :target-id="store.currentPost.id" :like-count="store.currentPost.like_count" />
              <div v-if="isOwner" class="flex items-center gap-4">
                <button
                  v-if="store.currentPost.status === 'ACTIVE'"
                  class="flex items-center gap-1.5 text-sm text-yulda-gray-600 hover:text-yulda-black"
                  @click="handleMarkClosed"
                >
                  <CheckCircle2 class="h-4 w-4" />
                  {{ t("jobs.markClosed") }}
                </button>
                <button class="flex items-center gap-1.5 text-sm text-red-500 hover:text-red-600" @click="handleDelete">
                  <Trash2 class="h-4 w-4" />
                  {{ t("jobs.deletePost") }}
                </button>
              </div>
            </div>
          </div>

          <h1 class="mt-4 text-xl font-bold text-yulda-black">{{ store.currentPost.title }}</h1>
          <div class="mt-1.5 flex flex-wrap items-center gap-1.5 text-sm text-yulda-gray-500">
            <span>{{ t(`jobs.category.${store.currentPost.category}`) }}</span>
            <span>&middot;</span>
            <span>{{ t(`jobs.employmentType.${store.currentPost.employment_type}`) }}</span>
          </div>

          <p v-if="payLabel" class="mt-3 text-2xl font-extrabold text-yulda-black">{{ payLabel }}</p>

          <span
            v-if="store.currentPost.status !== 'ACTIVE'"
            class="mt-2 inline-block rounded-full bg-yulda-gray-100 px-3 py-1 text-xs font-semibold text-yulda-gray-600"
          >
            {{ t(`jobs.status.${store.currentPost.status}`) }}
          </span>

          <div class="mt-4 flex flex-wrap items-center gap-1.5">
            <span v-if="store.currentPost.city" class="inline-flex items-center gap-1 rounded-xl border border-yulda-gray-200 bg-yulda-gray-50/80 px-2.5 py-1 text-xs font-semibold text-yulda-gray-800">
              <MapPin class="h-3 w-3 text-yulda-gray-500" />
              {{ store.currentPost.city }}
            </span>
            <span v-if="store.currentPost.requires_korean" class="rounded-lg bg-yulda-gray-100 px-2 py-0.5 text-[11px] font-semibold text-yulda-gray-600">
              {{ t("jobs.requiresKorean") }}
            </span>
            <span v-if="store.currentPost.visa_sponsorship" class="rounded-lg bg-emerald-50 px-2 py-0.5 text-[11px] font-semibold text-emerald-700 ring-1 ring-emerald-200">
              {{ t("jobs.visaSponsorship") }}
            </span>
          </div>

          <p class="mt-4 whitespace-pre-wrap text-sm text-yulda-gray-700">{{ store.currentPost.description }}</p>

          <div class="mt-6 flex items-center gap-2 border-t border-yulda-gray-100 pt-4 text-sm text-yulda-gray-500">
            <div class="flex h-6 w-6 items-center justify-center rounded-full bg-yulda-black text-xs font-semibold text-white">
              {{ store.currentPost.owner.name.charAt(0) }}
            </div>
            <span>{{ store.currentPost.owner.name }}</span>
          </div>

          <div class="mt-4 rounded-xl bg-yulda-gray-50 p-4">
            <p class="text-xs font-semibold uppercase text-yulda-gray-400">{{ t("jobs.contactValueLabel") }}</p>
            <p class="mt-1 text-sm font-medium text-yulda-black">{{ store.currentPost.contact_value }}</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
