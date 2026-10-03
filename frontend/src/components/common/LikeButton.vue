<script setup lang="ts">
import { ref } from "vue";
import { Heart } from "lucide-vue-next";

import { favoriteApi, type FavoriteTargetType } from "@/services/favoriteApi";
import { useAuthStore } from "@/stores/authStore";

const props = withDefaults(
  defineProps<{
    targetType: FavoriteTargetType;
    targetId: string;
    liked?: boolean;
    likeCount: number;
    size?: "sm" | "md";
  }>(),
  { liked: false, size: "md" },
);
const emit = defineEmits<{ change: [liked: boolean, likeCount: number] }>();

const auth = useAuthStore();
const isLiked = ref(props.liked);
const count = ref(props.likeCount);
const isSubmitting = ref(false);

async function handleClick(e: MouseEvent) {
  e.preventDefault();
  e.stopPropagation();

  if (!auth.isAuthenticated) {
    window.location.href = "/login";
    return;
  }
  if (isSubmitting.value) return;

  isSubmitting.value = true;
  const prevLiked = isLiked.value;
  const prevCount = count.value;
  isLiked.value = !prevLiked;
  count.value = prevLiked ? Math.max(prevCount - 1, 0) : prevCount + 1;

  try {
    const result = await favoriteApi.toggle(props.targetType, props.targetId);
    isLiked.value = result.is_favorited;
    count.value = result.like_count;
    emit("change", result.is_favorited, result.like_count);
  } catch {
    isLiked.value = prevLiked;
    count.value = prevCount;
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <button
    type="button"
    class="flex items-center gap-1 rounded-full transition-colors"
    :class="size === 'sm' ? 'px-1.5 py-1 text-xs' : 'px-2.5 py-1.5 text-sm'"
    :disabled="isSubmitting"
    @click="handleClick"
  >
    <Heart
      :class="[size === 'sm' ? 'h-3.5 w-3.5' : 'h-4 w-4', isLiked ? 'fill-red-500 text-red-500' : 'text-yulda-gray-400']"
    />
    <span :class="isLiked ? 'font-semibold text-red-500' : 'text-yulda-gray-500'">{{ count }}</span>
  </button>
</template>
