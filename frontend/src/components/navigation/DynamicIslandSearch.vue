<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { Search, X } from "lucide-vue-next";

const { t } = useI18n();
const router = useRouter();
const query = ref("");

function handleSubmit() {
  const trimmed = query.value.trim();
  if (!trimmed) return;
  router.push({ path: "/marketplace", query: { q: trimmed } });
}

function clearSearch() {
  query.value = "";
}
</script>

<template>
  <div class="flex w-full justify-center">
    <form
      class="flex h-11 w-full max-w-md items-center gap-2 rounded-2xl bg-white border border-yulda-gray-200 px-4 shadow focus-within:shadow-md focus-within:border-yulda-black focus-within:ring-1 focus-within:ring-yulda-black transition-all"
      @submit.prevent="handleSubmit"
    >
      <Search class="h-[18px] w-[18px] flex-shrink-0 text-yulda-gray-400" />
      <input
        v-model="query"
        type="text"
        :placeholder="t('nav.searchPlaceholder')"
        class="h-full min-w-0 flex-1 bg-transparent text-sm text-yulda-black placeholder:text-yulda-gray-400 focus:outline-none"
      />
      <button
        v-if="query"
        type="button"
        class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full text-yulda-gray-400 hover:bg-yulda-gray-100 hover:text-yulda-black transition-colors"
        :aria-label="t('nav.closeSearch')"
        @click="clearSearch"
      >
        <X class="h-4 w-4" />
      </button>
    </form>
  </div>
</template>
