<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import { authApi } from "@/services/authApi";

const email = ref("");
const isSubmitting = ref(false);
const submitted = ref(false);

async function handleSubmit() {
  isSubmitting.value = true;
  try {
    await authApi.forgotPassword(email.value);
    submitted.value = true;
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-yulda-black">Reset your password</h1>
    <p class="mt-2 text-sm text-yulda-gray-500">We'll send a reset link to your email.</p>

    <div v-if="submitted" class="mt-8 rounded-xl bg-yulda-gray-50 px-4 py-4 text-sm text-yulda-gray-700">
      If an account exists for <strong>{{ email }}</strong>, you'll receive a password reset link shortly.
    </div>
    <form v-else class="mt-8 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <BaseInput v-model="email" type="email" label="Email" placeholder="you@example.com" autocomplete="email" required />
      <BaseButton type="submit" full-width :loading="isSubmitting">Send reset link</BaseButton>
    </form>

    <p class="mt-8 text-sm text-yulda-gray-500">
      <RouterLink to="/login" class="font-semibold text-yulda-black">Back to login</RouterLink>
    </p>
  </div>
</template>
