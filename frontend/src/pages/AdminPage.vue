<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { ShieldAlert, ShieldCheck, Trash2 } from "lucide-vue-next";

import { adminApi } from "@/services/adminApi";
import { useConfirmStore } from "@/stores/confirmStore";
import { useToastStore } from "@/stores/toastStore";
import type { Report, ReportStatus } from "@/types/report";
import type { User } from "@/types/user";

const { t, d } = useI18n();
const confirmStore = useConfirmStore();
const toast = useToastStore();

const activeTab = ref<"reports" | "users">("reports");

const reports = ref<Report[]>([]);
const reportStatusFilter = ref<ReportStatus | "">("PENDING");
const isLoadingReports = ref(false);

async function loadReports() {
  isLoadingReports.value = true;
  try {
    const result = await adminApi.listReports(reportStatusFilter.value);
    reports.value = result.items;
  } finally {
    isLoadingReports.value = false;
  }
}

async function handleResolveReport(report: Report, status: "RESOLVED" | "DISMISSED") {
  await adminApi.resolveReport(report.id, status);
  toast.success(t("admin.reportUpdated"));
  await loadReports();
}

async function handleRemoveContent(report: Report) {
  const ok = await confirmStore.ask({ message: t("admin.confirmRemoveContent"), danger: true });
  if (!ok) return;
  try {
    await adminApi.removeContent(report.target_type, report.target_id);
    toast.success(t("admin.contentRemoved"));
  } finally {
    await handleResolveReport(report, "RESOLVED");
  }
}

const users = ref<User[]>([]);
const userSearch = ref("");
const isLoadingUsers = ref(false);

async function loadUsers() {
  isLoadingUsers.value = true;
  try {
    const result = await adminApi.listUsers(userSearch.value);
    users.value = result.items;
  } finally {
    isLoadingUsers.value = false;
  }
}

async function handleBan(user: User) {
  const ok = await confirmStore.ask({ message: t("admin.confirmBan"), danger: true });
  if (!ok) return;
  const updated = await adminApi.banUser(user.id);
  const index = users.value.findIndex((u) => u.id === user.id);
  if (index !== -1) users.value[index] = updated;
  toast.success(t("admin.userBanned"));
}

async function handleUnban(user: User) {
  const updated = await adminApi.unbanUser(user.id);
  const index = users.value.findIndex((u) => u.id === user.id);
  if (index !== -1) users.value[index] = updated;
  toast.success(t("admin.userUnbanned"));
}

function formatDate(iso: string): string {
  return d(new Date(iso), { dateStyle: "medium", timeStyle: "short" } as never) as unknown as string;
}

watch(reportStatusFilter, loadReports);
watch(activeTab, (tab) => {
  if (tab === "users" && users.value.length === 0) loadUsers();
});

onMounted(loadReports);
</script>

<template>
  <div class="mx-auto max-w-4xl px-6 py-10">
    <h1 class="text-2xl font-bold text-yulda-black">{{ t("admin.title") }}</h1>

    <div class="mt-6 flex gap-2 border-b border-yulda-gray-100">
      <button
        type="button"
        class="px-4 py-2.5 text-sm font-semibold"
        :class="activeTab === 'reports' ? 'border-b-2 border-yulda-black text-yulda-black' : 'text-yulda-gray-500'"
        @click="activeTab = 'reports'"
      >
        {{ t("admin.reportsTab") }}
      </button>
      <button
        type="button"
        class="px-4 py-2.5 text-sm font-semibold"
        :class="activeTab === 'users' ? 'border-b-2 border-yulda-black text-yulda-black' : 'text-yulda-gray-500'"
        @click="activeTab = 'users'"
      >
        {{ t("admin.usersTab") }}
      </button>
    </div>

    <div v-if="activeTab === 'reports'" class="mt-6">
      <select
        v-model="reportStatusFilter"
        class="rounded-xl border border-yulda-gray-200 bg-white px-3 py-2 text-sm focus:border-yulda-yellow focus:outline-none focus:ring-2 focus:ring-yulda-yellow"
      >
        <option value="PENDING">{{ t("admin.statusPending") }}</option>
        <option value="RESOLVED">{{ t("admin.statusResolved") }}</option>
        <option value="DISMISSED">{{ t("admin.statusDismissed") }}</option>
        <option value="">{{ t("admin.statusAll") }}</option>
      </select>

      <div v-if="isLoadingReports" class="mt-4 flex flex-col gap-2">
        <div v-for="i in 3" :key="i" class="h-20 animate-pulse rounded-xl bg-yulda-gray-100" />
      </div>
      <div v-else-if="reports.length === 0" class="mt-6 text-center text-sm text-yulda-gray-400">
        {{ t("admin.noReports") }}
      </div>
      <div v-else class="mt-4 flex flex-col gap-3">
        <div v-for="report in reports" :key="report.id" class="card p-4">
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="rounded-full bg-yulda-gray-100 px-2 py-0.5 text-xs font-semibold text-yulda-gray-600">
                  {{ report.target_type }}
                </span>
                <span class="text-xs font-semibold text-red-500">{{ t(`report.reasons.${report.reason}`) }}</span>
              </div>
              <p v-if="report.details" class="mt-2 text-sm text-yulda-gray-700">{{ report.details }}</p>
              <p class="mt-2 text-xs text-yulda-gray-400">
                {{ t("admin.reportedBy") }} {{ report.reporter.name }} &middot; {{ formatDate(report.created_at) }}
              </p>
            </div>
            <span
              class="flex-shrink-0 rounded-full px-2.5 py-1 text-xs font-semibold"
              :class="{
                'bg-yellow-50 text-yellow-700': report.status === 'PENDING',
                'bg-green-50 text-green-700': report.status === 'RESOLVED',
                'bg-yulda-gray-100 text-yulda-gray-500': report.status === 'DISMISSED',
              }"
            >
              {{ t(`admin.status${report.status}`) }}
            </span>
          </div>

          <div v-if="report.status === 'PENDING'" class="mt-3 flex gap-2 border-t border-yulda-gray-100 pt-3">
            <button
              v-if="report.target_type !== 'USER'"
              type="button"
              class="flex items-center gap-1.5 text-xs font-semibold text-red-500 hover:text-red-600"
              @click="handleRemoveContent(report)"
            >
              <Trash2 class="h-3.5 w-3.5" />
              {{ t("admin.removeContent") }}
            </button>
            <button
              type="button"
              class="ml-auto text-xs font-semibold text-yulda-gray-500 hover:text-yulda-black"
              @click="handleResolveReport(report, 'DISMISSED')"
            >
              {{ t("admin.dismiss") }}
            </button>
            <button
              type="button"
              class="text-xs font-semibold text-yulda-black hover:underline"
              @click="handleResolveReport(report, 'RESOLVED')"
            >
              {{ t("admin.markResolved") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="mt-6">
      <input
        v-model="userSearch"
        type="text"
        :placeholder="t('admin.searchUsers')"
        class="w-full max-w-sm rounded-xl border border-yulda-gray-200 bg-white px-3 py-2.5 text-sm focus:border-yulda-yellow focus:outline-none focus:ring-2 focus:ring-yulda-yellow"
        @keyup.enter="loadUsers"
      />
      <button type="button" class="btn-outline ml-2 !px-4 !py-2 text-sm" @click="loadUsers">
        {{ t("admin.search") }}
      </button>

      <div v-if="isLoadingUsers" class="mt-4 flex flex-col gap-2">
        <div v-for="i in 3" :key="i" class="h-14 animate-pulse rounded-xl bg-yulda-gray-100" />
      </div>
      <div v-else class="mt-4 flex flex-col gap-2">
        <div
          v-for="user in users"
          :key="user.id"
          class="flex items-center justify-between rounded-xl bg-yulda-gray-50 px-4 py-3"
        >
          <div class="min-w-0">
            <p class="truncate text-sm font-bold text-yulda-black">
              {{ user.name }}
              <span v-if="user.is_banned" class="ml-1.5 rounded-full bg-red-50 px-2 py-0.5 text-xs font-semibold text-red-600">
                {{ t("admin.banned") }}
              </span>
            </p>
            <p class="truncate text-xs text-yulda-gray-500">{{ user.email }} &middot; {{ user.roles.join(", ") }}</p>
          </div>
          <button
            v-if="!user.is_banned"
            type="button"
            class="flex flex-shrink-0 items-center gap-1.5 text-sm font-medium text-red-500 hover:text-red-600"
            @click="handleBan(user)"
          >
            <ShieldAlert class="h-4 w-4" />
            {{ t("admin.ban") }}
          </button>
          <button
            v-else
            type="button"
            class="flex flex-shrink-0 items-center gap-1.5 text-sm font-medium text-yulda-gray-500 hover:text-yulda-black"
            @click="handleUnban(user)"
          >
            <ShieldCheck class="h-4 w-4" />
            {{ t("admin.unban") }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
