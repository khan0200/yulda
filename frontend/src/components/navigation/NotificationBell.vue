<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { Bell, Check, Heart, MessageCircle } from "lucide-vue-next";

import { useNotificationStore } from "@/stores/notificationStore";
import type { AppNotification } from "@/types/notification";

const { t } = useI18n();
const router = useRouter();
const store = useNotificationStore();

const isOpen = ref(false);
const rootEl = ref<HTMLElement | null>(null);

function formatTime(iso: string): string {
  const diffMs = Date.now() - new Date(iso).getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return t("notifications.justNow");
  if (diffMin < 60) return `${diffMin}${t("notifications.minutesShort")}`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}${t("notifications.hoursShort")}`;
  return `${Math.floor(diffHr / 24)}${t("notifications.daysShort")}`;
}

async function toggleOpen() {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    await store.fetchNotifications();
  }
}

async function handleClickNotification(notification: AppNotification) {
  if (!notification.is_read) await store.markRead(notification.id);
  isOpen.value = false;
  if (notification.link) router.push(notification.link);
}

async function handleMarkAllRead() {
  await store.markAllRead();
}

function onClickOutside(e: MouseEvent) {
  if (rootEl.value && !rootEl.value.contains(e.target as Node)) {
    isOpen.value = false;
  }
}

onMounted(() => {
  store.fetchUnreadCount();
  document.addEventListener("mousedown", onClickOutside);
});
onUnmounted(() => document.removeEventListener("mousedown", onClickOutside));
</script>

<template>
  <div ref="rootEl" class="relative">
    <button
      type="button"
      class="relative flex h-9 w-9 items-center justify-center rounded-xl text-yulda-gray-600 transition-colors hover:bg-yulda-gray-100 hover:text-yulda-black"
      :aria-label="t('notifications.title')"
      @click="toggleOpen"
    >
      <Bell class="h-5 w-5" />
      <span
        v-if="store.unreadCount > 0"
        class="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white"
      >
        {{ store.unreadCount > 9 ? "9+" : store.unreadCount }}
      </span>
    </button>

    <Transition
      enter-active-class="transition-all duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition-all duration-100 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 z-50 mt-2 w-80 overflow-hidden rounded-2xl border border-yulda-gray-100 bg-white shadow-card-hover"
      >
        <div class="flex items-center justify-between border-b border-yulda-gray-100 px-4 py-3">
          <h3 class="text-sm font-bold text-yulda-black">{{ t("notifications.title") }}</h3>
          <button
            v-if="store.unreadCount > 0"
            type="button"
            class="flex items-center gap-1 text-xs font-medium text-yulda-gray-500 hover:text-yulda-black"
            @click="handleMarkAllRead"
          >
            <Check class="h-3.5 w-3.5" />
            {{ t("notifications.markAllRead") }}
          </button>
        </div>

        <div class="max-h-96 overflow-y-auto">
          <div v-if="store.isLoading" class="p-6 text-center text-sm text-yulda-gray-400">
            {{ t("notifications.loading") }}
          </div>
          <div v-else-if="store.items.length === 0" class="p-6 text-center text-sm text-yulda-gray-400">
            {{ t("notifications.empty") }}
          </div>
          <button
            v-for="notification in store.items"
            :key="notification.id"
            type="button"
            class="flex w-full items-start gap-3 border-b border-yulda-gray-50 px-4 py-3 text-left transition-colors hover:bg-yulda-gray-50"
            :class="{ 'bg-yulda-yellow/5': !notification.is_read }"
            @click="handleClickNotification(notification)"
          >
            <div
              class="mt-0.5 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full"
              :class="notification.type === 'NEW_MESSAGE' ? 'bg-blue-50 text-blue-600' : 'bg-red-50 text-red-500'"
            >
              <MessageCircle v-if="notification.type === 'NEW_MESSAGE'" class="h-4 w-4" />
              <Heart v-else class="h-4 w-4" />
            </div>
            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-bold text-yulda-black">{{ notification.title }}</p>
              <p class="line-clamp-2 text-xs text-yulda-gray-500">{{ notification.body }}</p>
              <p class="mt-0.5 text-[11px] text-yulda-gray-400">{{ formatTime(notification.created_at) }}</p>
            </div>
            <span v-if="!notification.is_read" class="mt-1.5 h-2 w-2 flex-shrink-0 rounded-full bg-yulda-yellow" />
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>
