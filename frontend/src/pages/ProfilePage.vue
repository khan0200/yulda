<script setup lang="ts">
import { useI18n } from "vue-i18n";

import { useAuthStore } from "@/stores/authStore";

const { t } = useI18n();
const auth = useAuthStore();
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-10">
    <h1 class="text-2xl font-bold text-yulda-black">{{ t("profile.title") }}</h1>

    <div class="card mt-6 p-6">
      <div class="flex items-center gap-4">
        <div class="flex h-16 w-16 items-center justify-center rounded-full bg-yulda-black text-xl font-bold text-white">
          {{ auth.user?.name?.charAt(0) }}
        </div>
        <div>
          <p class="text-lg font-semibold">{{ auth.user?.name }}</p>
          <p class="text-sm text-yulda-gray-500">{{ auth.user?.email }}</p>
        </div>
      </div>

      <dl class="mt-6 grid grid-cols-2 gap-4 border-t border-yulda-gray-100 pt-6">
        <div>
          <dt class="text-xs font-medium uppercase text-yulda-gray-400">{{ t("profile.roles") }}</dt>
          <dd class="mt-1 text-sm font-medium">{{ auth.user?.roles.join(", ") }}</dd>
        </div>
        <div>
          <dt class="text-xs font-medium uppercase text-yulda-gray-400">{{ t("profile.verification") }}</dt>
          <dd class="mt-1 text-sm font-medium">{{ auth.user?.verification_status }}</dd>
        </div>
        <div>
          <dt class="text-xs font-medium uppercase text-yulda-gray-400">{{ t("profile.phone") }}</dt>
          <dd class="mt-1 text-sm font-medium">{{ auth.user?.phone ?? t("profile.notSet") }}</dd>
        </div>
      </dl>
    </div>
  </div>
</template>
