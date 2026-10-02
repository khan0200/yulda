<script setup lang="ts">
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRouter } from "vue-router";
import { AxiosError } from "axios";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import { useAuthStore } from "@/stores/authStore";
import type { ApiErrorBody } from "@/types/api";

const { t } = useI18n();
const auth = useAuthStore();
const router = useRouter();

const form = reactive({ name: "", email: "", password: "" });
const errorMessage = ref("");
const isSubmitting = ref(false);

async function handleSubmit() {
  errorMessage.value = "";
  isSubmitting.value = true;
  try {
    await auth.signup(form);
    router.push("/");
  } catch (error) {
    if (error instanceof AxiosError) {
      const data = error.response?.data as ApiErrorBody | undefined;
      errorMessage.value = data?.message ?? t("auth.signupError");
    } else {
      errorMessage.value = t("auth.signupError");
    }
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-yulda-black">{{ t("auth.signupTitle") }}</h1>
    <p class="mt-2 text-sm text-yulda-gray-500">{{ t("auth.signupSubtitle") }}</p>

    <form class="mt-8 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <BaseInput v-model="form.name" :label="t('auth.fullName')" placeholder="Jane Doe" autocomplete="name" required />
      <BaseInput v-model="form.email" type="email" :label="t('auth.email')" placeholder="you@example.com" autocomplete="email" required />
      <BaseInput v-model="form.password" type="password" :label="t('auth.password')" :placeholder="t('auth.passwordPlaceholder')" autocomplete="new-password" required />

      <p v-if="errorMessage" class="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">{{ errorMessage }}</p>

      <BaseButton type="submit" full-width :loading="isSubmitting">{{ t("auth.createAccount") }}</BaseButton>
    </form>

    <p class="mt-8 text-sm text-yulda-gray-500">
      {{ t("auth.haveAccount") }}
      <RouterLink to="/login" class="font-semibold text-yulda-black">{{ t("auth.loginLink") }}</RouterLink>
    </p>
  </div>
</template>
