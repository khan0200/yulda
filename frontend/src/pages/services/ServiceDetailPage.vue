<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { ArrowLeft, CheckCircle2, Flag, ImageOff, MapPin, Trash2 } from "lucide-vue-next";

import LikeButton from "@/components/common/LikeButton.vue";
import ReportModal from "@/components/common/ReportModal.vue";
import { useAuthStore } from "@/stores/authStore";
import { useConfirmStore } from "@/stores/confirmStore";
import { useServiceStore } from "@/stores/serviceStore";
import { useToastStore } from "@/stores/toastStore";
import { formatPriceNote } from "@/utils/format";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const store = useServiceStore();
const confirmStore = useConfirmStore();
const toast = useToastStore();

const serviceId = computed(() => route.params.id as string);
const isOwner = computed(() => {
  return Boolean(auth.user && store.currentPost && store.currentPost.owner.id === auth.user.id);
});
const showReport = ref(false);

async function handleDelete() {
  const ok = await confirmStore.ask({ message: t("services.confirmDelete"), danger: true });
  if (!ok) return;
  await store.deletePost(serviceId.value);
  toast.success(t("services.deleteSuccess"));
  router.push("/services");
}

async function handleMarkUnavailable() {
  await store.markUnavailable(serviceId.value);
}

onMounted(() => store.fetchPost(serviceId.value));
</script>

<template>
  <div class="mx-auto max-w-3xl px-6 py-10">
    <RouterLink to="/services" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("services.backToFeed") }}
    </RouterLink>

    <div v-if="store.isLoading && !store.currentPost" class="card mt-6 h-96 animate-pulse bg-yulda-gray-100" />

    <template v-else-if="store.currentPost">
      <div class="card mt-6 overflow-hidden">
        <div class="flex aspect-video items-center justify-center bg-yulda-gray-100">
          <img
            v-if="store.currentPost.photos[0]"
            :src="store.currentPost.photos[0]"
            :alt="store.currentPost.title"
            class="h-full w-full object-cover"
          />
          <ImageOff v-else class="h-10 w-10 text-yulda-gray-300" />
        </div>

        <div class="p-6">
          <div class="flex items-center justify-between">
            <span class="inline-flex items-center rounded-full bg-yulda-yellow/15 px-2.5 py-1 text-xs font-semibold text-yulda-black">
              {{ t(`services.category.${store.currentPost.category}`) }}
            </span>
            <div class="flex items-center gap-3">
              <LikeButton target-type="SERVICES" :target-id="store.currentPost.id" :like-count="store.currentPost.like_count" />
              <div v-if="isOwner" class="flex items-center gap-4">
                <button
                  v-if="store.currentPost.status === 'ACTIVE'"
                  class="flex items-center gap-1.5 text-sm text-yulda-gray-600 hover:text-yulda-black"
                  @click="handleMarkUnavailable"
                >
                  <CheckCircle2 class="h-4 w-4" />
                  {{ t("services.markUnavailable") }}
                </button>
                <button class="flex items-center gap-1.5 text-sm text-red-500 hover:text-red-600" @click="handleDelete">
                  <Trash2 class="h-4 w-4" />
                  {{ t("services.deletePost") }}
                </button>
              </div>
            </div>
          </div>

          <h1 class="mt-4 text-xl font-bold text-yulda-black">{{ store.currentPost.title }}</h1>
          <p v-if="store.currentPost.price_note" class="mt-2 text-2xl font-extrabold text-yulda-black">
            {{ formatPriceNote(store.currentPost.price_note) }}
          </p>

          <span
            v-if="store.currentPost.status !== 'ACTIVE'"
            class="mt-2 inline-block rounded-full bg-yulda-gray-100 px-3 py-1 text-xs font-semibold text-yulda-gray-600"
          >
            {{ t(`services.status.${store.currentPost.status}`) }}
          </span>

          <p class="mt-4 whitespace-pre-wrap text-sm text-yulda-gray-700">{{ store.currentPost.description }}</p>

          <div class="mt-6 flex items-center gap-2 border-t border-yulda-gray-100 pt-4 text-sm text-yulda-gray-500">
            <div class="flex h-6 w-6 items-center justify-center rounded-full bg-yulda-black text-xs font-semibold text-white">
              {{ store.currentPost.owner.name.charAt(0) }}
            </div>
            <span>{{ store.currentPost.owner.name }}</span>
            <span v-if="store.currentPost.city" class="flex items-center gap-1">
              &middot; <MapPin class="h-3 w-3" /> {{ store.currentPost.city }}
            </span>
            <button
              v-if="auth.isAuthenticated && !isOwner"
              class="ml-auto flex items-center gap-1 text-xs font-medium text-yulda-gray-400 hover:text-red-500"
              @click="showReport = true"
            >
              <Flag class="h-3.5 w-3.5" />
              {{ t("report.reportButton") }}
            </button>
          </div>

          <div class="mt-4 rounded-xl bg-yulda-gray-50 p-4">
            <p class="text-xs font-semibold uppercase text-yulda-gray-400">{{ t("services.contactValueLabel") }}</p>
            <p class="mt-1 text-sm font-medium text-yulda-black">{{ store.currentPost.contact_value }}</p>
          </div>
        </div>
      </div>
    </template>

    <ReportModal v-model:show="showReport" target-type="SERVICES" :target-id="serviceId" />
  </div>
</template>
