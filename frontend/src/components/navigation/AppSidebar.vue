<script setup lang="ts">
import { RouterLink } from "vue-router";
import {
  Car,
  Heart,
  Home,
  MessageSquare,
  Package,
  Settings,
  ShoppingBag,
  User,
  Wallet,
  Wrench,
} from "lucide-vue-next";

const mainLinks = [
  { to: "/", label: "Home", icon: Home },
  { to: "/taxi", label: "Taxi", icon: Car },
  { to: "/delivery", label: "Delivery", icon: Package },
  { to: "/jobs", label: "Jobs", icon: ShoppingBag },
  { to: "/services", label: "Services", icon: Wrench },
];

const secondaryLinks = [
  { to: "/orders", label: "Orders", icon: ShoppingBag },
  { to: "/messages", label: "Messages", icon: MessageSquare },
  { to: "/favorites", label: "Favorites", icon: Heart },
];

const accountLinks = [
  { to: "/payments", label: "Payments", icon: Wallet },
  { to: "/profile", label: "Settings", icon: Settings },
];
</script>

<template>
  <aside class="flex h-full w-64 flex-col border-r border-yulda-gray-100 bg-white px-4 py-6">
    <RouterLink to="/" class="mb-8 px-2 text-xl font-extrabold tracking-tight">YULDA</RouterLink>

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
          {{ link.label }}
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
          {{ link.label }}
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
          {{ link.label }}
        </RouterLink>
      </div>
    </nav>

    <RouterLink to="/profile" class="mt-4 flex items-center gap-3 rounded-xl border border-yulda-gray-100 px-3 py-2.5 hover:bg-yulda-gray-50">
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-yulda-black text-white">
        <User class="h-4 w-4" />
      </div>
      <span class="truncate text-sm font-medium">Account</span>
    </RouterLink>
  </aside>
</template>
