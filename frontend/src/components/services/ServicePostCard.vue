<script setup lang="ts">
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import { Check, Copy, ImageOff, MapPin, Phone } from "lucide-vue-next";

import LikeButton from "@/components/common/LikeButton.vue";
import type { ServicePost } from "@/types/service";
import { formatPriceNote, formatRelativeTime } from "@/utils/format";

const props = withDefaults(defineProps<{ post: ServicePost; liked?: boolean }>(), { liked: false });
const { t, d } = useI18n();

const isRevealed = ref(false);
const isCopied = ref(false);

const isUnavailable = computed(() => props.post.status === "UNAVAILABLE");
const relativeTime = computed(() =>
  formatRelativeTime(props.post.created_at, (date) => String(d(date, { year: "numeric", month: "short", day: "numeric" } as never))),
);

async function handleContactClick() {
  const isMobile = typeof navigator !== "undefined" && /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

  if (!isRevealed.value) {
    isRevealed.value = true;
    if (navigator.clipboard) {
      try {
        await navigator.clipboard.writeText(props.post.contact_value);
        isCopied.value = true;
        setTimeout(() => { isCopied.value = false; }, 2500);
      } catch {
        // ignore
      }
    }
    if (isMobile) {
      window.location.href = `tel:${props.post.contact_value}`;
    }
  } else if (isMobile) {
    window.location.href = `tel:${props.post.contact_value}`;
  } else if (navigator.clipboard) {
    try {
      await navigator.clipboard.writeText(props.post.contact_value);
      isCopied.value = true;
      setTimeout(() => { isCopied.value = false; }, 2500);
    } catch {
      // ignore
    }
  }
}
</script>

<template>
  <RouterLink
    :to="`/services/${post.id}`"
    class="card flex flex-col overflow-hidden transition-all hover:shadow-card-hover group"
    :class="{ 'opacity-60': isUnavailable }"
  >
    <div class="relative flex aspect-video items-center justify-center bg-yulda-gray-100 overflow-hidden">
      <img
        v-if="post.photos[0]"
        :src="post.photos[0]"
        :alt="post.title"
        class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
      />
      <ImageOff v-else class="h-8 w-8 text-yulda-gray-300" />

      <div class="absolute right-2 top-2 rounded-full bg-white/90 shadow-md backdrop-blur">
        <LikeButton target-type="SERVICES" :target-id="post.id" :liked="liked" :like-count="post.like_count" size="sm" @click.stop />
      </div>
    </div>

    <div class="flex flex-1 flex-col gap-1.5 p-4">
      <div class="flex items-center gap-1.5 text-xs font-semibold text-yulda-gray-400">
        <span>{{ t(`services.category.${post.category}`) }}</span>
        <template v-if="relativeTime">
          <span>&middot;</span>
          <span>{{ relativeTime }}</span>
        </template>
      </div>
      <h3 class="line-clamp-2 text-sm font-bold text-yulda-black">{{ post.title }}</h3>
      <p v-if="post.price_note" class="mt-auto text-base font-extrabold text-yulda-black">
        {{ formatPriceNote(post.price_note) }}
      </p>

      <div class="flex items-center justify-between text-xs text-yulda-gray-400">
        <span v-if="post.city" class="flex items-center gap-1 font-medium text-yulda-gray-600 truncate">
          <MapPin class="h-3 w-3 flex-shrink-0" />
          {{ post.city }}
        </span>
        <button
          type="button"
          class="btn-primary !px-3 !py-1.5 text-xs font-bold shadow-md transition-all hover:scale-105 active:scale-95 flex items-center gap-1.5 ml-auto"
          :class="isCopied ? '!bg-emerald-400 !text-black ring-2 ring-emerald-300' : ''"
          @click.stop.prevent="handleContactClick"
        >
          <Phone class="h-3.5 w-3.5" />
          <template v-if="!isRevealed">
            <span>{{ t("services.call") }}</span>
          </template>
          <template v-else>
            <span class="font-black tracking-wide font-mono text-[11px]">{{ post.contact_value }}</span>
            <Check v-if="isCopied" class="h-3.5 w-3.5 text-emerald-950" />
            <Copy v-else class="h-3.5 w-3.5 opacity-70 hover:opacity-100" />
          </template>
        </button>
      </div>
    </div>
  </RouterLink>
</template>
