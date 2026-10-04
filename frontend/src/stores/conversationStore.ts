import { ref } from "vue";
import { defineStore } from "pinia";

import { conversationApi, type StartConversationPayload } from "@/services/conversationApi";
import type { Conversation, Message } from "@/types/conversation";

export const useConversationStore = defineStore("conversation", () => {
  const conversations = ref<Conversation[]>([]);
  const isLoadingConversations = ref(false);
  const messagesByConversation = ref<Record<string, Message[]>>({});
  const isLoadingMessages = ref(false);

  async function fetchConversations(): Promise<void> {
    isLoadingConversations.value = true;
    try {
      const result = await conversationApi.list();
      conversations.value = result.items;
    } finally {
      isLoadingConversations.value = false;
    }
  }

  async function startConversation(payload: StartConversationPayload): Promise<Conversation> {
    const convo = await conversationApi.start(payload);
    if (!conversations.value.some((c) => c.id === convo.id)) {
      conversations.value = [convo, ...conversations.value];
    }
    return convo;
  }

  async function fetchMessages(conversationId: string): Promise<void> {
    isLoadingMessages.value = true;
    try {
      const result = await conversationApi.listMessages(conversationId);
      messagesByConversation.value = { ...messagesByConversation.value, [conversationId]: result.items };
    } finally {
      isLoadingMessages.value = false;
    }
  }

  async function sendMessage(conversationId: string, body: string): Promise<void> {
    const message = await conversationApi.sendMessage(conversationId, body);
    const existing = messagesByConversation.value[conversationId] ?? [];
    messagesByConversation.value = {
      ...messagesByConversation.value,
      [conversationId]: [...existing, message],
    };
    const convo = conversations.value.find((c) => c.id === conversationId);
    if (convo) {
      convo.last_message_preview = body.length > 140 ? `${body.slice(0, 137)}...` : body;
      convo.last_message_at = message.created_at;
    }
  }

  async function markRead(conversationId: string): Promise<void> {
    const convo = conversations.value.find((c) => c.id === conversationId);
    if (convo) convo.unread_count = 0;
    await conversationApi.markRead(conversationId);
  }

  function handleIncomingMessage(conversationId: string, message: Message, isActiveThread: boolean): void {
    const existing = messagesByConversation.value[conversationId];
    if (existing) {
      messagesByConversation.value = {
        ...messagesByConversation.value,
        [conversationId]: [...existing, message],
      };
    }

    const convo = conversations.value.find((c) => c.id === conversationId);
    if (convo) {
      convo.last_message_preview = message.body.length > 140 ? `${message.body.slice(0, 137)}...` : message.body;
      convo.last_message_at = message.created_at;
      if (!isActiveThread) convo.unread_count += 1;
    }
  }

  function reset(): void {
    conversations.value = [];
    messagesByConversation.value = {};
  }

  return {
    conversations,
    isLoadingConversations,
    messagesByConversation,
    isLoadingMessages,
    fetchConversations,
    startConversation,
    fetchMessages,
    sendMessage,
    markRead,
    handleIncomingMessage,
    reset,
  };
});
