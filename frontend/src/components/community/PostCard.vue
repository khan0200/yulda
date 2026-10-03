<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { MessageCircle } from "lucide-vue-next";

import LikeButton from "@/components/common/LikeButton.vue";
import type { CommunityPost } from "@/types/community";

const props = withDefaults(defineProps<{ post: CommunityPost; liked?: boolean }>(), { liked: false });
const { t, d } = useI18n();

const relativeTime = computed(() => {
  const date = new Date(props.post.created_at);
  const diffMs = Date.now() - date.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "";
  if (diffMin < 60) return `${diffMin}m`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h`;
  const diffDay = Math.floor(diffHr / 24);
  if (diffDay < 7) return `${diffDay}d`;
  return d(date, { year: "numeric", month: "short", day: "numeric" } as never);
});
</script>

<template>
  <RouterLink :to="`/community/${post.id}`" class="card flex flex-col gap-3 p-5 transition-shadow hover:shadow-card-hover">
    <div class="flex items-center justify-between">
      <span class="inline-flex items-center rounded-full bg-yulda-yellow/15 px-2.5 py-1 text-xs font-semibold text-yulda-black">
        {{ t(`community.category.${post.category}`) }}
      </span>
      <span v-if="post.city" class="text-xs text-yulda-gray-400">{{ post.city }}</span>
    </div>

    <div class="flex gap-3">
      <div class="min-w-0 flex-1">
        <h3 class="text-base font-bold text-yulda-black">{{ post.title }}</h3>
        <p class="mt-1 line-clamp-2 text-sm text-yulda-gray-600">{{ post.body }}</p>
      </div>
      <div v-if="post.photos[0]" class="h-16 w-16 flex-shrink-0 overflow-hidden rounded-xl bg-yulda-gray-100">
        <img :src="post.photos[0]" :alt="post.title" class="h-full w-full object-cover" />
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-yulda-gray-400">
      <div class="flex items-center gap-2">
        <div class="flex h-5 w-5 items-center justify-center rounded-full bg-yulda-black text-[10px] font-semibold text-white">
          {{ post.author.name.charAt(0) }}
        </div>
        <span>{{ post.author.name }}</span>
        <span v-if="relativeTime">&middot; {{ relativeTime }}</span>
      </div>
      <div class="flex items-center gap-3">
        <LikeButton target-type="COMMUNITY" :target-id="post.id" :liked="liked" :like-count="post.like_count" size="sm" @click.stop />
        <div class="flex items-center gap-1">
          <MessageCircle class="h-3.5 w-3.5" />
          {{ post.comment_count }}
        </div>
      </div>
    </div>
  </RouterLink>
</template>
