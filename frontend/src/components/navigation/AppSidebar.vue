<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";
import {
  Building2,
  Car,
  CarFront,
  Home,
  ListChecks,
  MessageSquare,
  Package,
  Settings,
  ShieldCheck,
  ShoppingBag,
  Store,
  Users,
  Wrench,
} from "lucide-vue-next";

import { useAuthStore } from "@/stores/authStore";

const { t } = useI18n();
const auth = useAuthStore();

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

const accountLinks = [
  { to: "/my-listings", labelKey: "profile.myListings", icon: ListChecks },
  { to: "/messages", labelKey: "nav.messages", icon: MessageSquare },
  { to: "/profile", labelKey: "nav.settings", icon: Settings },
];
</script>

<template>
  <aside class="hidden h-full w-64 flex-col border-r border-yulda-gray-100 bg-white px-4 py-6 md:flex">
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
          v-for="link in accountLinks"
          :key="link.to"
          :to="link.to"
          class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black"
          active-class="bg-yulda-yellow/15 text-yulda-black font-semibold"
        >
          <component :is="link.icon" class="h-[18px] w-[18px]" />
          {{ t(link.labelKey) }}
        </RouterLink>

        <RouterLink
          v-if="auth.hasRole('ADMIN')"
          to="/admin"
          class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black"
          active-class="bg-yulda-yellow/15 text-yulda-black font-semibold"
        >
          <ShieldCheck class="h-[18px] w-[18px]" />
          {{ t("admin.title") }}
        </RouterLink>
      </div>
    </nav>
  </aside>
</template>
