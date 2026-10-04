<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRouter } from "vue-router";
import { AlertTriangle, KeyRound, ListChecks, ShieldOff, User, UserX } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import { blockApi } from "@/services/blockApi";
import { usersApi } from "@/services/usersApi";
import { useAuthStore } from "@/stores/authStore";
import { useConfirmStore } from "@/stores/confirmStore";
import { useToastStore } from "@/stores/toastStore";
import type { BlockedUser } from "@/types/block";

const { t } = useI18n();
const router = useRouter();
const auth = useAuthStore();
const confirmStore = useConfirmStore();
const toast = useToastStore();

const blockedUsers = ref<BlockedUser[]>([]);
const isLoadingBlocks = ref(false);

async function loadBlockedUsers() {
  isLoadingBlocks.value = true;
  try {
    blockedUsers.value = await blockApi.list();
  } finally {
    isLoadingBlocks.value = false;
  }
}

async function handleUnblock(userId: string) {
  const ok = await confirmStore.ask({ message: t("block.confirmUnblock") });
  if (!ok) return;
  await blockApi.unblock(userId);
  blockedUsers.value = blockedUsers.value.filter((b) => b.blocked_user.id !== userId);
  toast.success(t("block.unblockSuccess"));
}

onMounted(loadBlockedUsers);

const deleteAccountPassword = ref("");
const isDeletingAccount = ref(false);
const deleteAccountError = ref("");

async function handleDeleteAccount() {
  deleteAccountError.value = "";
  if (!deleteAccountPassword.value) return;

  const ok = await confirmStore.ask({
    title: t("profile.deleteAccountConfirmTitle"),
    message: t("profile.deleteAccountConfirmMessage"),
    danger: true,
  });
  if (!ok) return;

  isDeletingAccount.value = true;
  try {
    await usersApi.deleteAccount(deleteAccountPassword.value);
    auth.clearSession();
    toast.success(t("profile.deleteAccountSuccess"));
    router.push("/");
  } catch {
    deleteAccountError.value = t("profile.deleteAccountWrongPassword");
  } finally {
    isDeletingAccount.value = false;
  }
}

const profileForm = reactive({
  name: auth.user?.name ?? "",
  phone: auth.user?.phone ?? "",
});
const isSavingProfile = ref(false);
const profileSuccess = ref(false);
const profileError = ref("");

async function handleProfileSave() {
  if (!profileForm.name.trim()) return;
  isSavingProfile.value = true;
  profileSuccess.value = false;
  profileError.value = "";
  try {
    const updated = await usersApi.updateProfile({
      name: profileForm.name.trim(),
      phone: profileForm.phone.trim() || undefined,
    });
    auth.setUser(updated);
    profileSuccess.value = true;
  } catch {
    profileError.value = t("profile.updateFailed");
  } finally {
    isSavingProfile.value = false;
  }
}

const passwordForm = reactive({
  currentPassword: "",
  newPassword: "",
  confirmPassword: "",
});
const isSavingPassword = ref(false);
const passwordSuccess = ref(false);
const passwordError = ref("");

async function handlePasswordSave() {
  passwordError.value = "";
  passwordSuccess.value = false;

  if (passwordForm.newPassword.length < 8) {
    passwordError.value = t("profile.passwordTooShort");
    return;
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordError.value = t("profile.passwordMismatch");
    return;
  }

  isSavingPassword.value = true;
  try {
    await usersApi.changePassword({
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword,
    });
    passwordSuccess.value = true;
    passwordForm.currentPassword = "";
    passwordForm.newPassword = "";
    passwordForm.confirmPassword = "";
  } catch {
    passwordError.value = t("profile.currentPasswordWrong");
  } finally {
    isSavingPassword.value = false;
  }
}
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-10">
    <h1 class="text-2xl font-bold text-yulda-black">{{ t("profile.title") }}</h1>

    <RouterLink
      to="/my-listings"
      class="card mt-6 flex items-center justify-between p-5 transition-colors hover:border-yulda-yellow/70"
    >
      <div class="flex items-center gap-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-yulda-yellow/15 text-yulda-black">
          <ListChecks class="h-5 w-5" />
        </div>
        <div>
          <p class="text-sm font-bold text-yulda-black">{{ t("profile.myListings") }}</p>
          <p class="text-xs text-yulda-gray-500">{{ t("profile.myListingsDesc") }}</p>
        </div>
      </div>
    </RouterLink>

    <div class="card mt-4 p-6">
      <div class="flex items-center gap-2">
        <User class="h-4 w-4 text-yulda-gray-400" />
        <h2 class="text-sm font-bold uppercase tracking-wide text-yulda-gray-500">{{ t("profile.accountInfo") }}</h2>
      </div>

      <div class="mt-4 flex items-center gap-4">
        <div class="flex h-16 w-16 items-center justify-center rounded-full bg-yulda-black text-xl font-bold text-white">
          {{ auth.user?.name?.charAt(0) }}
        </div>
        <div>
          <p class="text-lg font-semibold">{{ auth.user?.name }}</p>
          <p class="text-sm text-yulda-gray-500">{{ auth.user?.email }}</p>
        </div>
      </div>

      <form class="mt-6 flex flex-col gap-4 border-t border-yulda-gray-100 pt-6" @submit.prevent="handleProfileSave">
        <BaseInput v-model="profileForm.name" :label="t('profile.name')" required />
        <BaseInput v-model="profileForm.phone" :label="t('profile.phone')" :placeholder="t('profile.phonePlaceholder')" />

        <dl class="grid grid-cols-2 gap-4">
          <div>
            <dt class="text-xs font-medium uppercase text-yulda-gray-400">{{ t("profile.roles") }}</dt>
            <dd class="mt-1 text-sm font-medium">{{ auth.user?.roles.join(", ") }}</dd>
          </div>
          <div>
            <dt class="text-xs font-medium uppercase text-yulda-gray-400">{{ t("profile.verification") }}</dt>
            <dd class="mt-1 text-sm font-medium">{{ auth.user?.verification_status }}</dd>
          </div>
        </dl>

        <p v-if="profileSuccess" class="rounded-xl bg-green-50 px-4 py-3 text-sm text-green-700">
          {{ t("profile.updateSuccess") }}
        </p>
        <p v-if="profileError" class="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
          {{ profileError }}
        </p>

        <BaseButton type="submit" :loading="isSavingProfile">{{ t("profile.saveChanges") }}</BaseButton>
      </form>
    </div>

    <div class="card mt-4 p-6">
      <div class="flex items-center gap-2">
        <KeyRound class="h-4 w-4 text-yulda-gray-400" />
        <h2 class="text-sm font-bold uppercase tracking-wide text-yulda-gray-500">{{ t("profile.changePassword") }}</h2>
      </div>

      <form class="mt-4 flex flex-col gap-4" @submit.prevent="handlePasswordSave">
        <BaseInput
          v-model="passwordForm.currentPassword"
          type="password"
          autocomplete="current-password"
          :label="t('profile.currentPassword')"
          required
        />
        <BaseInput
          v-model="passwordForm.newPassword"
          type="password"
          autocomplete="new-password"
          :label="t('profile.newPassword')"
          required
        />
        <BaseInput
          v-model="passwordForm.confirmPassword"
          type="password"
          autocomplete="new-password"
          :label="t('profile.confirmNewPassword')"
          required
        />

        <p v-if="passwordSuccess" class="rounded-xl bg-green-50 px-4 py-3 text-sm text-green-700">
          {{ t("profile.passwordChangeSuccess") }}
        </p>
        <p v-if="passwordError" class="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
          {{ passwordError }}
        </p>

        <BaseButton
          type="submit"
          :disabled="!passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword"
          :loading="isSavingPassword"
        >
          {{ t("profile.changePassword") }}
        </BaseButton>
      </form>
    </div>

    <div v-if="blockedUsers.length > 0" class="card mt-4 p-6">
      <div class="flex items-center gap-2">
        <ShieldOff class="h-4 w-4 text-yulda-gray-400" />
        <h2 class="text-sm font-bold uppercase tracking-wide text-yulda-gray-500">{{ t("profile.blockedUsers") }}</h2>
      </div>

      <div class="mt-4 flex flex-col gap-2">
        <div
          v-for="block in blockedUsers"
          :key="block.id"
          class="flex items-center justify-between rounded-xl bg-yulda-gray-50 px-4 py-3"
        >
          <div class="flex items-center gap-3">
            <div class="flex h-9 w-9 items-center justify-center rounded-full bg-yulda-black text-sm font-semibold text-white">
              {{ block.blocked_user.name.charAt(0) }}
            </div>
            <span class="text-sm font-medium text-yulda-black">{{ block.blocked_user.name }}</span>
          </div>
          <button
            type="button"
            class="flex items-center gap-1.5 text-sm font-medium text-yulda-gray-500 hover:text-yulda-black"
            @click="handleUnblock(block.blocked_user.id)"
          >
            <UserX class="h-4 w-4" />
            {{ t("block.unblockUser") }}
          </button>
        </div>
      </div>
    </div>

    <div class="card mt-4 border-red-200 p-6">
      <div class="flex items-center gap-2">
        <AlertTriangle class="h-4 w-4 text-red-500" />
        <h2 class="text-sm font-bold uppercase tracking-wide text-red-500">{{ t("profile.dangerZone") }}</h2>
      </div>
      <p class="mt-2 text-sm text-yulda-gray-600">{{ t("profile.deleteAccountWarning") }}</p>

      <form class="mt-4 flex flex-col gap-3" @submit.prevent="handleDeleteAccount">
        <BaseInput
          v-model="deleteAccountPassword"
          type="password"
          autocomplete="current-password"
          :label="t('profile.deleteAccountPasswordLabel')"
        />
        <p v-if="deleteAccountError" class="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
          {{ deleteAccountError }}
        </p>
        <button
          type="submit"
          :disabled="!deleteAccountPassword || isDeletingAccount"
          class="rounded-xl bg-red-500 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-red-600 disabled:opacity-50"
        >
          {{ t("profile.deleteAccountButton") }}
        </button>
      </form>
    </div>
  </div>
</template>
