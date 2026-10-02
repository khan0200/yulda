<script setup lang="ts">
import { ref } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { Menu, X } from "lucide-vue-next";

import { useAuthStore } from "@/stores/authStore";

const auth = useAuthStore();
const router = useRouter();
const mobileOpen = ref(false);

const navLinks = [
  { to: "/taxi", label: "Taxi" },
  { to: "/delivery", label: "Delivery" },
  { to: "/jobs", label: "Jobs" },
  { to: "/services", label: "Services" },
];

async function handleLogout() {
  await auth.logout();
  router.push("/");
}
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-yulda-gray-100 bg-white/95 backdrop-blur">
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
      <div class="flex items-center gap-10">
        <RouterLink to="/" class="flex items-center gap-2">
          <span class="text-xl font-extrabold tracking-tight text-yulda-black">YULDA</span>
        </RouterLink>
        <nav class="hidden items-center gap-1 md:flex">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="rounded-lg px-4 py-2 text-sm font-medium text-yulda-gray-700 transition-colors hover:bg-yulda-gray-100 hover:text-yulda-black"
            active-class="text-yulda-black bg-yulda-gray-100"
          >
            {{ link.label }}
          </RouterLink>
        </nav>
      </div>

      <div class="hidden items-center gap-3 md:flex">
        <template v-if="auth.isAuthenticated">
          <RouterLink to="/orders" class="btn-ghost">Orders</RouterLink>
          <RouterLink to="/profile" class="btn-outline">{{ auth.user?.name }}</RouterLink>
          <button class="btn-ghost" @click="handleLogout">Log out</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn-ghost">Log in</RouterLink>
          <RouterLink to="/signup" class="btn-primary">Sign up</RouterLink>
        </template>
      </div>

      <button class="p-2 md:hidden" @click="mobileOpen = !mobileOpen">
        <Menu v-if="!mobileOpen" class="h-6 w-6" />
        <X v-else class="h-6 w-6" />
      </button>
    </div>

    <div v-if="mobileOpen" class="border-t border-yulda-gray-100 px-6 py-4 md:hidden">
      <nav class="flex flex-col gap-1">
        <RouterLink
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="rounded-lg px-4 py-3 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </RouterLink>
        <div class="my-2 border-t border-yulda-gray-100" />
        <template v-if="auth.isAuthenticated">
          <RouterLink to="/orders" class="rounded-lg px-4 py-3 text-sm font-medium hover:bg-yulda-gray-100" @click="mobileOpen = false">Orders</RouterLink>
          <RouterLink to="/profile" class="rounded-lg px-4 py-3 text-sm font-medium hover:bg-yulda-gray-100" @click="mobileOpen = false">Profile</RouterLink>
          <button class="rounded-lg px-4 py-3 text-left text-sm font-medium hover:bg-yulda-gray-100" @click="handleLogout">Log out</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="rounded-lg px-4 py-3 text-sm font-medium hover:bg-yulda-gray-100" @click="mobileOpen = false">Log in</RouterLink>
          <RouterLink to="/signup" class="rounded-lg px-4 py-3 text-sm font-semibold text-yulda-black" @click="mobileOpen = false">Sign up</RouterLink>
        </template>
      </nav>
    </div>
  </header>
</template>
