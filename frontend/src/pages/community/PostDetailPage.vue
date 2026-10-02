<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { ArrowLeft, Trash2 } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import { useAuthStore } from "@/stores/authStore";
import { useCommunityStore } from "@/stores/communityStore";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const store = useCommunityStore();

const postId = computed(() => route.params.id as string);
const commentBody = ref("");
const isSubmittingComment = ref(false);

const isAuthor = computed(() => {
  return Boolean(auth.user && store.currentPost && store.currentPost.author.id === auth.user.id);
});

async function handleAddComment() {
  if (!commentBody.value.trim()) return;
  isSubmittingComment.value = true;
  try {
    await store.addComment(postId.value, { body: commentBody.value.trim() });
    commentBody.value = "";
  } finally {
    isSubmittingComment.value = false;
  }
}

async function handleDelete() {
  if (!confirm(t("community.confirmDelete"))) return;
  await store.deletePost(postId.value);
  router.push("/community");
}

onMounted(() => store.fetchPost(postId.value));
</script>

<template>
  <div class="mx-auto max-w-3xl px-6 py-10">
    <RouterLink to="/community" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("community.backToFeed") }}
    </RouterLink>

    <div v-if="store.isLoading && !store.currentPost" class="card mt-6 h-48 animate-pulse bg-yulda-gray-100" />

    <template v-else-if="store.currentPost">
      <div class="card mt-6 p-6">
        <div class="flex items-center justify-between">
          <span class="inline-flex items-center rounded-full bg-yulda-yellow/15 px-2.5 py-1 text-xs font-semibold text-yulda-black">
            {{ t(`community.category.${store.currentPost.category}`) }}
          </span>
          <button v-if="isAuthor" class="flex items-center gap-1.5 text-sm text-red-500 hover:text-red-600" @click="handleDelete">
            <Trash2 class="h-4 w-4" />
            {{ t("community.deletePost") }}
          </button>
        </div>

        <h1 class="mt-4 text-xl font-bold text-yulda-black">{{ store.currentPost.title }}</h1>
        <p class="mt-3 whitespace-pre-wrap text-sm text-yulda-gray-700">{{ store.currentPost.body }}</p>

        <div class="mt-6 flex items-center gap-2 border-t border-yulda-gray-100 pt-4 text-sm text-yulda-gray-500">
          <div class="flex h-6 w-6 items-center justify-center rounded-full bg-yulda-black text-xs font-semibold text-white">
            {{ store.currentPost.author.name.charAt(0) }}
          </div>
          <span>{{ store.currentPost.author.name }}</span>
          <span v-if="store.currentPost.city">&middot; {{ store.currentPost.city }}</span>
        </div>
      </div>

      <div class="mt-8">
        <h2 class="text-sm font-semibold text-yulda-black">
          {{ t("community.comments") }} ({{ store.currentPost.comment_count }})
        </h2>

        <div v-if="store.comments.length === 0" class="mt-4 text-sm text-yulda-gray-500">
          {{ t("community.noComments") }}
        </div>

        <div v-else class="mt-4 flex flex-col gap-4">
          <div v-for="comment in store.comments" :key="comment.id" class="flex gap-3">
            <div class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full bg-yulda-black text-xs font-semibold text-white">
              {{ comment.author.name.charAt(0) }}
            </div>
            <div>
              <p class="text-sm font-medium text-yulda-black">{{ comment.author.name }}</p>
              <p class="mt-0.5 whitespace-pre-wrap text-sm text-yulda-gray-700">{{ comment.body }}</p>
            </div>
          </div>
        </div>

        <div v-if="auth.isAuthenticated" class="mt-6 flex flex-col gap-3">
          <BaseTextarea v-model="commentBody" :placeholder="t('community.commentPlaceholder')" :rows="3" />
          <BaseButton class="self-end" :loading="isSubmittingComment" @click="handleAddComment">
            {{ t("community.send") }}
          </BaseButton>
        </div>
      </div>
    </template>
  </div>
</template>
