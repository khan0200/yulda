<script setup lang="ts">
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRouter } from "vue-router";
import { Briefcase, Check, Copy, Home, MapPin, MessageCircle, Phone, User } from "lucide-vue-next";

import LikeButton from "@/components/common/LikeButton.vue";
import { useAuthStore } from "@/stores/authStore";
import { useConversationStore } from "@/stores/conversationStore";
import type { JobPost } from "@/types/job";
import { formatKrw, formatRelativeTime } from "@/utils/format";

const props = withDefaults(defineProps<{ post: JobPost; liked?: boolean }>(), { liked: false });
const { t, d } = useI18n();
const router = useRouter();
const auth = useAuthStore();
const conversationStore = useConversationStore();

const isRevealed = ref(false);
const isCopied = ref(false);
const isMessaging = ref(false);

const isClosed = computed(() => props.post.status === "CLOSED");
const relativeTime = computed(() =>
  formatRelativeTime(props.post.created_at, (date) => String(d(date, { year: "numeric", month: "short", day: "numeric" } as never))),
);
const payLabel = computed(() => {
  if (!props.post.pay_amount || !props.post.pay_type) return "";
  return `${formatKrw(props.post.pay_amount)} / ${t(`jobs.payType.${props.post.pay_type}`)}`;
});
const overtimeLabel = computed(() => {
  if (!props.post.overtime_pay_amount) return "";
  return `${t("jobs.overtimeShort")}: ${formatKrw(props.post.overtime_pay_amount)}`;
});
const visibleVisas = computed(() => props.post.accepted_visas.slice(0, 3));
const extraVisaCount = computed(() => Math.max(0, props.post.accepted_visas.length - 3));

async function handlePhoneClick() {
  const contactValue = props.post.contact_value;
  if (!contactValue) return;
  const isMobile = typeof navigator !== "undefined" && /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

  if (!isRevealed.value) {
    isRevealed.value = true;
    if (navigator.clipboard) {
      try {
        await navigator.clipboard.writeText(contactValue);
        isCopied.value = true;
        setTimeout(() => { isCopied.value = false; }, 2500);
      } catch {
        // ignore
      }
    }
    if (isMobile) {
      window.location.href = `tel:${contactValue}`;
    }
  } else if (isMobile) {
    window.location.href = `tel:${contactValue}`;
  } else if (navigator.clipboard) {
    try {
      await navigator.clipboard.writeText(contactValue);
      isCopied.value = true;
      setTimeout(() => { isCopied.value = false; }, 2500);
    } catch {
      // ignore
    }
  }
}

async function handleMessageClick() {
  if (!auth.isAuthenticated) {
    router.push({ path: "/login", query: { redirect: `/jobs/${props.post.id}` } });
    return;
  }
  if (isMessaging.value) return;
  isMessaging.value = true;
  try {
    const convo = await conversationStore.startConversation({
      target_user_id: props.post.owner.id,
      listing_type: "JOBS",
      listing_id: props.post.id,
      listing_title: props.post.title,
    });
    router.push(`/messages/${convo.id}`);
  } finally {
    isMessaging.value = false;
  }
}
</script>

<template>
  <RouterLink
    :to="`/jobs/${post.id}`"
    class="card relative flex flex-col justify-between overflow-hidden rounded-2xl border border-yulda-gray-200/90 bg-white p-5 shadow-card transition-all duration-300 hover:-translate-y-1 hover:border-yulda-yellow/70 hover:shadow-card-hover"
    :class="{ 'opacity-60': isClosed }"
  >
    <div class="space-y-3">
      <div class="flex items-center justify-between gap-2">
        <span
          class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold shadow-2xs"
          :class="post.post_type === 'OFFER' ? 'bg-amber-50 text-amber-900 ring-1 ring-amber-300/70' : 'bg-blue-50 text-blue-900 ring-1 ring-blue-300/70'"
        >
          <Briefcase class="h-3.5 w-3.5" />
          <span>{{ t(`jobs.postType.${post.post_type}`) }}</span>
        </span>
        <LikeButton target-type="JOBS" :target-id="post.id" :liked="liked" :like-count="post.like_count" size="sm" @click.stop />
      </div>

      <div>
        <h3 class="line-clamp-2 text-sm font-extrabold text-yulda-black">{{ post.title }}</h3>
        <div class="mt-1.5 flex flex-wrap items-center gap-1.5 text-xs text-yulda-gray-500">
          <span>{{ t(`jobs.category.${post.category}`) }}</span>
          <span>&middot;</span>
          <span>{{ t(`jobs.employmentType.${post.employment_type}`) }}</span>
          <template v-if="relativeTime">
            <span>&middot;</span>
            <span>{{ relativeTime }}</span>
          </template>
        </div>
      </div>

      <div class="flex flex-wrap items-baseline gap-x-2">
        <p v-if="payLabel" class="text-base font-extrabold text-yulda-black">{{ payLabel }}</p>
        <p v-if="overtimeLabel" class="text-xs font-semibold text-yulda-gray-500">{{ overtimeLabel }}</p>
      </div>

      <div class="flex flex-wrap items-center gap-1.5">
        <span v-if="post.city" class="inline-flex items-center gap-1 rounded-xl border border-yulda-gray-200 bg-yulda-gray-50/80 px-2.5 py-1 text-xs font-semibold text-yulda-gray-800">
          <MapPin class="h-3 w-3 text-yulda-gray-500" />
          {{ post.city }}
        </span>
        <span v-if="post.housing_option !== 'NOT_PROVIDED'" class="inline-flex items-center gap-1 rounded-lg bg-blue-50 px-2 py-0.5 text-[11px] font-semibold text-blue-700 ring-1 ring-blue-200">
          <Home class="h-3 w-3" />
          {{ t(`jobs.housingOption.${post.housing_option}`) }}
        </span>
        <span v-if="post.requires_korean" class="rounded-lg bg-yulda-gray-100 px-2 py-0.5 text-[11px] font-semibold text-yulda-gray-600">
          {{ t("jobs.requiresKorean") }}
        </span>
        <span v-if="post.visa_sponsorship" class="rounded-lg bg-emerald-50 px-2 py-0.5 text-[11px] font-semibold text-emerald-700 ring-1 ring-emerald-200">
          {{ t("jobs.visaSponsorship") }}
        </span>
        <span v-for="visa in visibleVisas" :key="visa" class="rounded-lg bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-800 ring-1 ring-amber-200">
          {{ visa }}
        </span>
        <span v-if="extraVisaCount > 0" class="rounded-lg bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-800 ring-1 ring-amber-200">
          +{{ extraVisaCount }}
        </span>
      </div>
    </div>

    <div class="mt-4 flex items-center justify-between border-t border-yulda-gray-100 pt-3">
      <div class="flex items-center gap-2">
        <div class="flex h-7 w-7 items-center justify-center rounded-full bg-yulda-gray-100 text-yulda-gray-700 border border-yulda-gray-200">
          <User class="h-3.5 w-3.5 text-yulda-gray-500" />
        </div>
        <span class="text-xs font-bold text-yulda-black truncate">{{ post.owner.name }}</span>
      </div>

      <button
        v-if="post.contact_method === 'PHONE'"
        type="button"
        class="btn-primary !px-3.5 !py-2 text-xs font-bold shadow-md transition-all hover:scale-105 active:scale-95 flex items-center gap-1.5"
        :class="isCopied ? '!bg-emerald-400 !text-black ring-2 ring-emerald-300' : ''"
        @click.stop.prevent="handlePhoneClick"
      >
        <Phone class="h-3.5 w-3.5" />
        <template v-if="!isRevealed">
          <span>{{ t("jobs.call") }}</span>
        </template>
        <template v-else>
          <span class="font-black tracking-wide font-mono text-[11px]">{{ post.contact_value }}</span>
          <Check v-if="isCopied" class="h-3.5 w-3.5 text-emerald-950" />
          <Copy v-else class="h-3.5 w-3.5 opacity-70 hover:opacity-100" />
        </template>
      </button>
      <button
        v-else
        type="button"
        class="btn-primary !px-3.5 !py-2 text-xs font-bold shadow-md transition-all hover:scale-105 active:scale-95 flex items-center gap-1.5"
        :disabled="isMessaging"
        @click.stop.prevent="handleMessageClick"
      >
        <MessageCircle class="h-3.5 w-3.5" />
        <span>{{ t("jobs.sendMessage") }}</span>
      </button>
    </div>
  </RouterLink>
</template>
