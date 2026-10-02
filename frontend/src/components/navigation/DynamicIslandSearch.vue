<script setup lang="ts">
import { nextTick, ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { Search, X } from "lucide-vue-next";

const { t } = useI18n();
const router = useRouter();

const isExpanded = ref(false);
const query = ref("");
const rootEl = ref<HTMLElement | null>(null);
const inputEl = ref<HTMLInputElement | null>(null);

async function expand() {
  isExpanded.value = true;
  await nextTick();
  inputEl.value?.focus();
}

function collapse() {
  isExpanded.value = false;
  query.value = "";
}

function handleSubmit() {
  const trimmed = query.value.trim();
  if (!trimmed) return;
  router.push({ path: "/marketplace", query: { q: trimmed } });
  collapse();
}

onClickOutside(rootEl, () => {
  if (isExpanded.value && !query.value) collapse();
});
</script>

<template>
  <div ref="rootEl" class="flex justify-center">
    <div
      class="flex items-center overflow-hidden bg-yulda-black transition-all ease-[cubic-bezier(0.34,1.56,0.64,1)]"
      :class="isExpanded ? 'w-full max-w-xl rounded-2xl duration-500' : 'w-11 rounded-full duration-300'"
      style="height: 44px"
    >
      <button
        v-if="!isExpanded"
        type="button"
        class="flex h-11 w-11 flex-shrink-0 items-center justify-center text-white"
        :aria-label="t('nav.search')"
        @click="expand"
      >
        <Search class="h-[18px] w-[18px]" />
      </button>

      <form v-else class="flex w-full items-center gap-2 px-3" @submit.prevent="handleSubmit">
        <Search class="h-[18px] w-[18px] flex-shrink-0 text-yulda-gray-400" />
        <input
          ref="inputEl"
          v-model="query"
          type="text"
          :placeholder="t('nav.searchPlaceholder')"
          class="h-full min-w-0 flex-1 bg-transparent text-sm text-white placeholder:text-yulda-gray-500 focus:outline-none"
          @keydown.escape="collapse"
        />
        <button
          type="button"
          class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full text-yulda-gray-400 hover:bg-white/10 hover:text-white"
          :aria-label="t('nav.closeSearch')"
          @click="collapse"
        >
          <X class="h-4 w-4" />
        </button>
      </form>
    </div>
  </div>
</template>
