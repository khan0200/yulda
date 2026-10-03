<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import TurnstileWidget from "@/components/common/TurnstileWidget.vue";
import { authApi } from "@/services/authApi";

const { t } = useI18n();
const email = ref("");
const turnstileToken = ref("");
const isSubmitting = ref(false);
const submitted = ref(false);

async function handleSubmit() {
  isSubmitting.value = true;
  try {
    await authApi.forgotPassword(email.value, turnstileToken.value);
    submitted.value = true;
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-yulda-black">{{ t("auth.forgotTitle") }}</h1>
    <p class="mt-2 text-sm text-yulda-gray-500">{{ t("auth.forgotSubtitle") }}</p>

    <div v-if="submitted" class="mt-8 rounded-xl bg-yulda-gray-50 px-4 py-4 text-sm text-yulda-gray-700">
      {{ t("auth.resetSent", { email }) }}
    </div>
    <form v-else class="mt-8 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <BaseInput v-model="email" type="email" :label="t('auth.email')" placeholder="you@example.com" autocomplete="email" required />
      <TurnstileWidget @verified="(token) => (turnstileToken = token)" @expired="turnstileToken = ''" />
      <BaseButton type="submit" full-width :loading="isSubmitting">{{ t("auth.sendResetLink") }}</BaseButton>
    </form>

    <p class="mt-8 text-sm text-yulda-gray-500">
      <RouterLink to="/login" class="font-semibold text-yulda-black">{{ t("auth.backToLogin") }}</RouterLink>
    </p>
  </div>
</template>
