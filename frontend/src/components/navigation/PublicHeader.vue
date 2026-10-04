<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRouter } from "vue-router";
import { Menu, Search, X } from "lucide-vue-next";

import AppLogo from "@/components/common/AppLogo.vue";
import LanguageSwitcher from "@/components/common/LanguageSwitcher.vue";
import DynamicIslandSearch from "@/components/navigation/DynamicIslandSearch.vue";
import NotificationBell from "@/components/navigation/NotificationBell.vue";
import { useAuthStore } from "@/stores/authStore";

const { t } = useI18n();
const auth = useAuthStore();
const router = useRouter();
const mobileOpen = ref(false);
const mobileSearchOpen = ref(false);
const mobileQuery = ref("");

async function handleLogout() {
  await auth.logout();
  router.push("/");
}

function submitMobileSearch() {
  const trimmed = mobileQuery.value.trim();
  if (!trimmed) return;
  router.push({ path: "/search", query: { q: trimmed } });
  mobileSearchOpen.value = false;
  mobileQuery.value = "";
}
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-yulda-gray-100 bg-white/95 backdrop-blur">
    <div class="mx-auto flex h-16 max-w-7xl items-center gap-4 px-6">
      <RouterLink to="/" class="flex flex-shrink-0 items-center gap-2">
        <AppLogo :size="28" />
      </RouterLink>

      <div class="hidden flex-1 md:block">
        <DynamicIslandSearch />
      </div>

      <div class="hidden flex-shrink-0 items-center gap-2 md:flex">
        <LanguageSwitcher />
        <template v-if="auth.isAuthenticated">
          <RouterLink to="/messages" class="btn-ghost">{{ t("nav.messages") }}</RouterLink>
          <NotificationBell />
          <RouterLink to="/profile" class="btn-outline">{{ auth.user?.name }}</RouterLink>
          <button class="btn-ghost" @click="handleLogout">{{ t("nav.logout") }}</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn-ghost">{{ t("nav.login") }}</RouterLink>
          <RouterLink to="/signup" class="btn-primary">{{ t("nav.signup") }}</RouterLink>
        </template>
      </div>

      <div class="ml-auto flex items-center gap-1 md:hidden">
        <button class="p-2" :aria-label="t('nav.search')" @click="mobileSearchOpen = !mobileSearchOpen">
          <Search class="h-5 w-5" />
        </button>
        <NotificationBell v-if="auth.isAuthenticated" />
        <LanguageSwitcher />
        <button class="p-2" @click="mobileOpen = !mobileOpen">
          <Menu v-if="!mobileOpen" class="h-6 w-6" />
          <X v-else class="h-6 w-6" />
        </button>
      </div>
    </div>

    <div v-if="mobileSearchOpen" class="border-t border-yulda-gray-100 px-6 py-3 md:hidden">
      <form class="flex items-center gap-2 rounded-xl bg-yulda-gray-100 px-3 py-2.5" @submit.prevent="submitMobileSearch">
        <Search class="h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
        <input
          v-model="mobileQuery"
          type="text"
          :placeholder="t('nav.searchPlaceholder')"
          class="w-full bg-transparent text-sm text-yulda-black placeholder:text-yulda-gray-400 focus:outline-none"
        />
      </form>
    </div>

    <div v-if="mobileOpen" class="border-t border-yulda-gray-100 px-6 py-4 md:hidden">
      <nav class="flex flex-col gap-1">
        <RouterLink to="/taxi" class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.taxi") }}</RouterLink>
        <RouterLink to="/delivery" class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.delivery") }}</RouterLink>
        <RouterLink to="/marketplace" class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.marketplace") }}</RouterLink>
        <RouterLink to="/housing" class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.housing") }}</RouterLink>
        <RouterLink to="/auto" class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.auto") }}</RouterLink>
        <RouterLink to="/jobs" class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.jobs") }}</RouterLink>
        <RouterLink to="/services" class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.services") }}</RouterLink>
        <RouterLink to="/community" class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.community") }}</RouterLink>
        <div class="my-2 border-t border-yulda-gray-100" />
        <template v-if="auth.isAuthenticated">
          <RouterLink to="/my-listings" class="rounded-lg px-4 py-3 text-sm font-medium hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("profile.myListings") }}</RouterLink>
          <RouterLink to="/messages" class="rounded-lg px-4 py-3 text-sm font-medium hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.messages") }}</RouterLink>
          <RouterLink to="/profile" class="rounded-lg px-4 py-3 text-sm font-medium hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("profile.title") }}</RouterLink>
          <button class="rounded-lg px-4 py-3 text-left text-sm font-medium hover:bg-yulda-gray-100" @click="handleLogout">{{ t("nav.logout") }}</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="rounded-lg px-4 py-3 text-sm font-medium hover:bg-yulda-gray-100" @click="mobileOpen = false">{{ t("nav.login") }}</RouterLink>
          <RouterLink to="/signup" class="rounded-lg px-4 py-3 text-sm font-semibold text-yulda-black" @click="mobileOpen = false">{{ t("nav.signup") }}</RouterLink>
        </template>
      </nav>
    </div>
  </header>
</template>
