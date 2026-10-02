<script setup lang="ts">
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRouter } from "vue-router";
import { ArrowLeft } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import { useCommunityStore } from "@/stores/communityStore";
import type { PostCategory } from "@/types/community";

const { t } = useI18n();
const router = useRouter();
const store = useCommunityStore();

const categories: PostCategory[] = [
  "QUESTION",
  "ANNOUNCEMENT",
  "LOST_AND_FOUND",
  "MEETUP",
  "TRAVELER_REQUEST",
  "NEWS",
  "OTHER",
];

const form = reactive({
  category: "QUESTION" as PostCategory,
  title: "",
  body: "",
});
const isSubmitting = ref(false);

async function handleSubmit() {
  if (!form.title.trim() || !form.body.trim()) return;
  isSubmitting.value = true;
  try {
    const post = await store.createPost(form);
    router.push(`/community/${post.id}`);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-10">
    <RouterLink to="/community" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("community.backToFeed") }}
    </RouterLink>

    <h1 class="mt-4 text-2xl font-bold text-yulda-black">{{ t("community.newPost") }}</h1>

    <form class="mt-6 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <div>
        <label class="label">{{ t("community.categoryLabel") }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="category in categories"
            :key="category"
            type="button"
            class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
            :class="form.category === category ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
            @click="form.category = category"
          >
            {{ t(`community.category.${category}`) }}
          </button>
        </div>
      </div>

      <BaseInput v-model="form.title" :label="t('community.titleLabel')" :placeholder="t('community.titlePlaceholder')" required />
      <BaseTextarea v-model="form.body" :label="t('community.bodyLabel')" :placeholder="t('community.bodyPlaceholder')" :rows="8" required />

      <BaseButton type="submit" full-width :loading="isSubmitting">{{ t("community.publish") }}</BaseButton>
    </form>
  </div>
</template>
