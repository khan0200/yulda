<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";
import { Flag, MessageSquare, Send, UserX } from "lucide-vue-next";

import ReportModal from "@/components/common/ReportModal.vue";
import { blockApi } from "@/services/blockApi";
import { useAuthStore } from "@/stores/authStore";
import { useConfirmStore } from "@/stores/confirmStore";
import { useConversationStore } from "@/stores/conversationStore";
import { useToastStore } from "@/stores/toastStore";
import type { Conversation } from "@/types/conversation";

const { t, d } = useI18n();
const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const store = useConversationStore();
const confirmStore = useConfirmStore();
const toast = useToastStore();

const draft = ref("");
const isSending = ref(false);
const messagesEnd = ref<HTMLElement | null>(null);
const showReport = ref(false);

const activeConversationId = computed(() => (route.params.id as string | undefined) ?? null);
const activeConversation = computed(() =>
  store.conversations.find((c) => c.id === activeConversationId.value) ?? null,
);
const activeMessages = computed(() =>
  activeConversationId.value ? store.messagesByConversation[activeConversationId.value] ?? [] : [],
);

function otherParticipant(convo: Conversation) {
  return convo.participants.find((p) => p.id !== auth.user?.id) ?? convo.participants[0];
}

function formatTime(iso: string): string {
  return d(new Date(iso), { hour: "2-digit", minute: "2-digit" } as never) as unknown as string;
}

async function scrollToBottom() {
  await nextTick();
  messagesEnd.value?.scrollIntoView({ behavior: "smooth" });
}

async function selectConversation(id: string) {
  router.push(`/messages/${id}`);
}

async function loadThread(id: string) {
  await store.fetchMessages(id);
  await store.markRead(id);
  scrollToBottom();
}

async function handleSend() {
  const body = draft.value.trim();
  if (!body || !activeConversationId.value) return;
  isSending.value = true;
  draft.value = "";
  try {
    await store.sendMessage(activeConversationId.value, body);
    scrollToBottom();
  } finally {
    isSending.value = false;
  }
}

async function handleBlock() {
  if (!activeConversation.value) return;
  const ok = await confirmStore.ask({ message: t("block.confirmBlock"), danger: true });
  if (!ok) return;
  await blockApi.block(otherParticipant(activeConversation.value).id);
  toast.success(t("block.blockSuccess"));
}

watch(activeConversationId, (id) => {
  if (id) loadThread(id);
});

watch(activeMessages, () => scrollToBottom());

onMounted(async () => {
  await store.fetchConversations();
  if (activeConversationId.value) await loadThread(activeConversationId.value);
});
</script>

<template>
  <div class="mx-auto flex h-[calc(100vh-4rem)] max-w-6xl">
    <!-- Conversation list -->
    <div class="w-full flex-shrink-0 border-r border-yulda-gray-100 sm:w-80" :class="{ 'hidden sm:block': activeConversationId }">
      <div class="border-b border-yulda-gray-100 px-5 py-4">
        <h1 class="text-lg font-bold text-yulda-black">{{ t("messages.title") }}</h1>
        <p class="text-xs text-yulda-gray-500">{{ t("messages.subtitle") }}</p>
      </div>

      <div v-if="store.isLoadingConversations" class="flex flex-col gap-2 p-4">
        <div v-for="i in 4" :key="i" class="h-16 animate-pulse rounded-xl bg-yulda-gray-100" />
      </div>

      <div v-else-if="store.conversations.length === 0" class="p-6 text-center text-sm text-yulda-gray-400">
        {{ t("messages.noConversations") }}
      </div>

      <div v-else class="flex flex-col overflow-y-auto">
        <button
          v-for="convo in store.conversations"
          :key="convo.id"
          type="button"
          class="flex items-start gap-3 border-b border-yulda-gray-50 px-5 py-3.5 text-left transition-colors hover:bg-yulda-gray-50"
          :class="{ 'bg-yulda-yellow/10': convo.id === activeConversationId }"
          @click="selectConversation(convo.id)"
        >
          <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-yulda-black text-sm font-bold text-white">
            {{ otherParticipant(convo).name.charAt(0) }}
          </div>
          <div class="min-w-0 flex-1">
            <div class="flex items-center justify-between gap-2">
              <p class="truncate text-sm font-bold text-yulda-black">{{ otherParticipant(convo).name }}</p>
              <span v-if="convo.unread_count > 0" class="flex h-5 min-w-5 items-center justify-center rounded-full bg-yulda-yellow px-1.5 text-[11px] font-bold text-yulda-black">
                {{ convo.unread_count }}
              </span>
            </div>
            <p v-if="convo.listing_title" class="truncate text-xs font-medium text-yulda-gray-500">
              {{ t("messages.about") }}: {{ convo.listing_title }}
            </p>
            <p class="truncate text-xs text-yulda-gray-400">{{ convo.last_message_preview ?? "" }}</p>
          </div>
        </button>
      </div>
    </div>

    <!-- Active thread -->
    <div class="flex flex-1 flex-col" :class="{ 'hidden sm:flex': !activeConversationId }">
      <template v-if="activeConversation">
        <div class="flex items-center gap-3 border-b border-yulda-gray-100 px-5 py-4">
          <div class="flex h-9 w-9 items-center justify-center rounded-full bg-yulda-black text-xs font-bold text-white">
            {{ otherParticipant(activeConversation).name.charAt(0) }}
          </div>
          <div class="min-w-0 flex-1">
            <p class="truncate text-sm font-bold text-yulda-black">{{ otherParticipant(activeConversation).name }}</p>
            <p v-if="activeConversation.listing_title" class="truncate text-xs text-yulda-gray-500">
              {{ activeConversation.listing_title }}
            </p>
          </div>
          <button
            type="button"
            class="flex items-center gap-1 text-xs font-medium text-yulda-gray-400 hover:text-red-500"
            @click="showReport = true"
          >
            <Flag class="h-3.5 w-3.5" />
            {{ t("report.reportButton") }}
          </button>
          <button
            type="button"
            class="flex items-center gap-1 text-xs font-medium text-yulda-gray-400 hover:text-red-500"
            @click="handleBlock"
          >
            <UserX class="h-3.5 w-3.5" />
            {{ t("block.blockUser") }}
          </button>
        </div>

        <div class="flex-1 overflow-y-auto px-5 py-4">
          <div v-if="store.isLoadingMessages" class="text-center text-sm text-yulda-gray-400">
            {{ t("messages.loadingMessages") }}
          </div>
          <div v-else class="flex flex-col gap-3">
            <div
              v-for="message in activeMessages"
              :key="message.id"
              class="flex flex-col"
              :class="message.sender_id === auth.user?.id ? 'items-end' : 'items-start'"
            >
              <div
                class="max-w-[75%] rounded-2xl px-4 py-2.5 text-sm"
                :class="message.sender_id === auth.user?.id ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-black'"
              >
                {{ message.body }}
              </div>
              <span class="mt-1 text-[11px] text-yulda-gray-400">{{ formatTime(message.created_at) }}</span>
            </div>
            <div ref="messagesEnd" />
          </div>
        </div>

        <form class="flex items-center gap-2 border-t border-yulda-gray-100 px-4 py-3" @submit.prevent="handleSend">
          <input
            v-model="draft"
            type="text"
            :placeholder="t('messages.typePlaceholder')"
            class="flex-1 rounded-xl border border-yulda-gray-200 bg-white px-4 py-2.5 text-sm focus:border-yulda-yellow focus:outline-none focus:ring-2 focus:ring-yulda-yellow"
          />
          <button
            type="submit"
            class="btn-primary !px-4 !py-2.5"
            :disabled="!draft.trim() || isSending"
          >
            <Send class="h-4 w-4" />
          </button>
        </form>
      </template>

      <div v-else class="flex flex-1 flex-col items-center justify-center gap-2 text-yulda-gray-400">
        <MessageSquare class="h-10 w-10" />
        <p class="text-sm">{{ t("messages.selectConversation") }}</p>
      </div>
    </div>

    <ReportModal
      v-if="activeConversation"
      v-model:show="showReport"
      target-type="USER"
      :target-id="otherParticipant(activeConversation).id"
    />
  </div>
</template>
