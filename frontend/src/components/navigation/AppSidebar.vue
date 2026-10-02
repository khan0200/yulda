<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import {
  Building2,
  Car,
  CarFront,
  Heart,
  Home,
  MessageSquare,
  Package,
  Settings,
  ShoppingBag,
  Store,
  User,
  Users,
  Wallet,
  Wrench,
} from "lucide-vue-next";

import AppLogo from "@/components/common/AppLogo.vue";
import LanguageSwitcher from "@/components/common/LanguageSwitcher.vue";

const { t } = useI18n();

const mainLinks = [
  { to: "/", labelKey: "nav.home", icon: Home },
  { to: "/taxi", labelKey: "nav.taxi", icon: Car },
  { to: "/delivery", labelKey: "nav.delivery", icon: Package },
  { to: "/jobs", labelKey: "nav.jobs", icon: ShoppingBag },
  { to: "/services", labelKey: "nav.services", icon: Wrench },
  { to: "/marketplace", labelKey: "nav.marketplace", icon: Store },
  { to: "/housing", labelKey: "nav.housing", icon: Building2 },
  { to: "/auto", labelKey: "nav.auto", icon: CarFront },
  { to: "/community", labelKey: "nav.community", icon: Users },
];

const secondaryLinks = [
  { to: "/orders", labelKey: "nav.orders", icon: ShoppingBag },
  { to: "/messages", labelKey: "nav.messages", icon: MessageSquare },
  { to: "/favorites", labelKey: "nav.favorites", icon: Heart },
];

const accountLinks = [
  { to: "/payments", labelKey: "nav.payments", icon: Wallet },
  { to: "/profile", labelKey: "nav.settings", icon: Settings },
];
</script>

<template>
  <aside class="flex h-full w-64 flex-col border-r border-yulda-gray-100 bg-white px-4 py-6">
    <div class="mb-8 flex items-center justify-between px-2">
      <RouterLink to="/"><AppLogo :size="28" /></RouterLink>
      <LanguageSwitcher />
    </div>

    <nav class="flex flex-1 flex-col gap-6">
      <div class="flex flex-col gap-1">
        <RouterLink
          v-for="link in mainLinks"
          :key="link.to"
          :to="link.to"
          class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black"
          active-class="bg-yulda-yellow/15 text-yulda-black font-semibold"
        >
          <component :is="link.icon" class="h-[18px] w-[18px]" />
          {{ t(link.labelKey) }}
        </RouterLink>
      </div>

      <div class="flex flex-col gap-1 border-t border-yulda-gray-100 pt-4">
        <RouterLink
          v-for="link in secondaryLinks"
          :key="link.to"
          :to="link.to"
          class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black"
          active-class="bg-yulda-yellow/15 text-yulda-black font-semibold"
        >
          <component :is="link.icon" class="h-[18px] w-[18px]" />
          {{ t(link.labelKey) }}
        </RouterLink>
      </div>

      <div class="flex flex-col gap-1 border-t border-yulda-gray-100 pt-4">
        <RouterLink
          v-for="link in accountLinks"
          :key="link.to"
          :to="link.to"
          class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black"
          active-class="bg-yulda-yellow/15 text-yulda-black font-semibold"
        >
          <component :is="link.icon" class="h-[18px] w-[18px]" />
          {{ t(link.labelKey) }}
        </RouterLink>
      </div>
    </nav>

    <RouterLink to="/profile" class="mt-4 flex items-center gap-3 rounded-xl border border-yulda-gray-100 px-3 py-2.5 hover:bg-yulda-gray-50">
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-yulda-black text-white">
        <User class="h-4 w-4" />
      </div>
      <span class="truncate text-sm font-medium">{{ t("nav.account") }}</span>
    </RouterLink>
  </aside>
</template>
