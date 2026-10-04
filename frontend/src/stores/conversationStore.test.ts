import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { conversationApi } from "@/services/conversationApi";
import { useConversationStore } from "@/stores/conversationStore";
import type { Conversation, Message } from "@/types/conversation";

vi.mock("@/services/conversationApi", () => ({
  conversationApi: {
    list: vi.fn(),
    start: vi.fn(),
    listMessages: vi.fn(),
    sendMessage: vi.fn(),
    markRead: vi.fn(),
  },
}));

function makeConversation(overrides: Partial<Conversation> = {}): Conversation {
  return {
    id: "c1",
    participants: [
      { id: "me", name: "Me", avatar: null },
      { id: "them", name: "Them", avatar: null },
    ],
    listing_type: "MARKETPLACE",
    listing_id: "l1",
    listing_title: "iPhone 13",
    last_message_preview: null,
    last_message_at: null,
    unread_count: 0,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    ...overrides,
  };
}

function makeMessage(overrides: Partial<Message> = {}): Message {
  return {
    id: "m1",
    conversation_id: "c1",
    sender_id: "them",
    body: "Hello",
    created_at: new Date().toISOString(),
    read_at: null,
    ...overrides,
  };
}

describe("conversationStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("fetchConversations populates the conversation list", async () => {
    const store = useConversationStore();
    vi.mocked(conversationApi.list).mockResolvedValueOnce({
      items: [makeConversation()],
      total: 1,
      page: 1,
      page_size: 20,
      has_more: false,
    });

    await store.fetchConversations();

    expect(store.conversations).toHaveLength(1);
    expect(store.conversations[0].id).toBe("c1");
  });

  it("startConversation adds a new conversation to the front of the list", async () => {
    const store = useConversationStore();
    store.conversations = [makeConversation({ id: "existing" })];
    vi.mocked(conversationApi.start).mockResolvedValueOnce(makeConversation({ id: "new" }));

    const result = await store.startConversation({ target_user_id: "them" });

    expect(result.id).toBe("new");
    expect(store.conversations.map((c) => c.id)).toEqual(["new", "existing"]);
  });

  it("startConversation does not duplicate an already-known conversation", async () => {
    const store = useConversationStore();
    store.conversations = [makeConversation({ id: "c1" })];
    vi.mocked(conversationApi.start).mockResolvedValueOnce(makeConversation({ id: "c1" }));

    await store.startConversation({ target_user_id: "them" });

    expect(store.conversations).toHaveLength(1);
  });

  it("fetchMessages stores messages keyed by conversation id", async () => {
    const store = useConversationStore();
    vi.mocked(conversationApi.listMessages).mockResolvedValueOnce({
      items: [makeMessage()],
      total: 1,
      page: 1,
      page_size: 50,
      has_more: false,
    });

    await store.fetchMessages("c1");

    expect(store.messagesByConversation["c1"]).toHaveLength(1);
  });

  it("sendMessage appends the sent message and updates the conversation preview", async () => {
    const store = useConversationStore();
    store.conversations = [makeConversation({ id: "c1", last_message_preview: null })];
    store.messagesByConversation = { c1: [] };
    vi.mocked(conversationApi.sendMessage).mockResolvedValueOnce(
      makeMessage({ id: "m2", sender_id: "me", body: "Hi there" }),
    );

    await store.sendMessage("c1", "Hi there");

    expect(store.messagesByConversation["c1"]).toHaveLength(1);
    expect(store.conversations[0].last_message_preview).toBe("Hi there");
  });

  it("sendMessage truncates a long preview to 140 characters with ellipsis", async () => {
    const store = useConversationStore();
    const longBody = "x".repeat(200);
    store.conversations = [makeConversation({ id: "c1" })];
    store.messagesByConversation = { c1: [] };
    vi.mocked(conversationApi.sendMessage).mockResolvedValueOnce(
      makeMessage({ id: "m2", sender_id: "me", body: longBody }),
    );

    await store.sendMessage("c1", longBody);

    expect(store.conversations[0].last_message_preview).toHaveLength(140);
    expect(store.conversations[0].last_message_preview?.endsWith("...")).toBe(true);
  });

  it("markRead zeroes the conversation's unread count", async () => {
    const store = useConversationStore();
    store.conversations = [makeConversation({ id: "c1", unread_count: 4 })];
    vi.mocked(conversationApi.markRead).mockResolvedValueOnce(undefined);

    await store.markRead("c1");

    expect(store.conversations[0].unread_count).toBe(0);
  });

  it("handleIncomingMessage increments unread count only when the thread is not active", () => {
    const store = useConversationStore();
    store.conversations = [makeConversation({ id: "c1", unread_count: 0 })];
    store.messagesByConversation = { c1: [] };

    store.handleIncomingMessage("c1", makeMessage({ id: "m3" }), false);
    expect(store.conversations[0].unread_count).toBe(1);
    expect(store.messagesByConversation["c1"]).toHaveLength(1);

    store.handleIncomingMessage("c1", makeMessage({ id: "m4" }), true);
    expect(store.conversations[0].unread_count).toBe(1);
    expect(store.messagesByConversation["c1"]).toHaveLength(2);
  });

  it("handleIncomingMessage does not create a message list for an unopened thread", () => {
    const store = useConversationStore();
    store.conversations = [makeConversation({ id: "c1" })];

    store.handleIncomingMessage("c1", makeMessage(), false);

    expect(store.messagesByConversation["c1"]).toBeUndefined();
  });

  it("reset clears conversations and messages", () => {
    const store = useConversationStore();
    store.conversations = [makeConversation()];
    store.messagesByConversation = { c1: [makeMessage()] };

    store.reset();

    expect(store.conversations).toEqual([]);
    expect(store.messagesByConversation).toEqual({});
  });
});
