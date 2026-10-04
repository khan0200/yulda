import { ref } from "vue";
import { defineStore } from "pinia";

import { notificationApi } from "@/services/notificationApi";
import type { AppNotification } from "@/types/notification";

export const useNotificationStore = defineStore("notification", () => {
  const items = ref<AppNotification[]>([]);
  const unreadCount = ref(0);
  const isLoading = ref(false);

  async function fetchNotifications(page = 1, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const result = await notificationApi.list(page, 20);
      items.value = append ? [...items.value, ...result.items] : result.items;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchUnreadCount(): Promise<void> {
    unreadCount.value = await notificationApi.unreadCount();
  }

  async function markRead(id: string): Promise<void> {
    const notification = items.value.find((n) => n.id === id);
    if (notification && !notification.is_read) {
      notification.is_read = true;
      unreadCount.value = Math.max(unreadCount.value - 1, 0);
    }
    await notificationApi.markRead(id);
  }

  async function markAllRead(): Promise<void> {
    items.value.forEach((n) => { n.is_read = true; });
    unreadCount.value = 0;
    await notificationApi.markAllRead();
  }

  function handleIncoming(notification: AppNotification): void {
    items.value = [notification, ...items.value];
    unreadCount.value += 1;
  }

  function reset(): void {
    items.value = [];
    unreadCount.value = 0;
  }

  return {
    items,
    unreadCount,
    isLoading,
    fetchNotifications,
    fetchUnreadCount,
    markRead,
    markAllRead,
    handleIncoming,
    reset,
  };
});
