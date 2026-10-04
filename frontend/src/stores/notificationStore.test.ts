import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { notificationApi } from "@/services/notificationApi";
import { useNotificationStore } from "@/stores/notificationStore";
import type { AppNotification } from "@/types/notification";

vi.mock("@/services/notificationApi", () => ({
  notificationApi: {
    list: vi.fn(),
    unreadCount: vi.fn(),
    markRead: vi.fn(),
    markAllRead: vi.fn(),
  },
}));

function makeNotification(overrides: Partial<AppNotification> = {}): AppNotification {
  return {
    id: "n1",
    type: "NEW_MESSAGE",
    title: "Alice",
    body: "Hello!",
    link: "/messages/c1",
    is_read: false,
    created_at: new Date().toISOString(),
    ...overrides,
  };
}

describe("notificationStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("fetchNotifications replaces items on first page, appends on subsequent pages", async () => {
    const store = useNotificationStore();
    vi.mocked(notificationApi.list).mockResolvedValueOnce({
      items: [makeNotification({ id: "n1" })],
      total: 2,
      page: 1,
      page_size: 20,
      has_more: true,
    });
    await store.fetchNotifications(1);
    expect(store.items.map((n) => n.id)).toEqual(["n1"]);

    vi.mocked(notificationApi.list).mockResolvedValueOnce({
      items: [makeNotification({ id: "n2" })],
      total: 2,
      page: 2,
      page_size: 20,
      has_more: false,
    });
    await store.fetchNotifications(2, true);
    expect(store.items.map((n) => n.id)).toEqual(["n1", "n2"]);
  });

  it("fetchUnreadCount stores the count from the API", async () => {
    const store = useNotificationStore();
    vi.mocked(notificationApi.unreadCount).mockResolvedValueOnce(3);
    await store.fetchUnreadCount();
    expect(store.unreadCount).toBe(3);
  });

  it("markRead optimistically marks the item read and decrements the count", async () => {
    const store = useNotificationStore();
    store.items = [makeNotification({ id: "n1", is_read: false })];
    store.unreadCount = 1;
    vi.mocked(notificationApi.markRead).mockResolvedValueOnce(makeNotification({ id: "n1", is_read: true }));

    await store.markRead("n1");

    expect(store.items[0].is_read).toBe(true);
    expect(store.unreadCount).toBe(0);
    expect(notificationApi.markRead).toHaveBeenCalledWith("n1");
  });

  it("markRead does not go below zero unread count for an already-read item", async () => {
    const store = useNotificationStore();
    store.items = [makeNotification({ id: "n1", is_read: true })];
    store.unreadCount = 0;
    vi.mocked(notificationApi.markRead).mockResolvedValueOnce(makeNotification({ id: "n1", is_read: true }));

    await store.markRead("n1");

    expect(store.unreadCount).toBe(0);
  });

  it("markAllRead marks every item read and zeroes the count", async () => {
    const store = useNotificationStore();
    store.items = [
      makeNotification({ id: "n1", is_read: false }),
      makeNotification({ id: "n2", is_read: false }),
    ];
    store.unreadCount = 2;
    vi.mocked(notificationApi.markAllRead).mockResolvedValueOnce(undefined);

    await store.markAllRead();

    expect(store.items.every((n) => n.is_read)).toBe(true);
    expect(store.unreadCount).toBe(0);
  });

  it("handleIncoming prepends the new notification and increments unread count", () => {
    const store = useNotificationStore();
    store.items = [makeNotification({ id: "old" })];
    store.unreadCount = 1;

    store.handleIncoming(makeNotification({ id: "new" }));

    expect(store.items.map((n) => n.id)).toEqual(["new", "old"]);
    expect(store.unreadCount).toBe(2);
  });

  it("reset clears items and unread count", () => {
    const store = useNotificationStore();
    store.items = [makeNotification()];
    store.unreadCount = 5;

    store.reset();

    expect(store.items).toEqual([]);
    expect(store.unreadCount).toBe(0);
  });
});
