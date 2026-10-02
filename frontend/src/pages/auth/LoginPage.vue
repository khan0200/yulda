<script setup lang="ts">
import { reactive, ref } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { AxiosError } from "axios";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import { useAuthStore } from "@/stores/authStore";
import type { ApiErrorBody } from "@/types/api";

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const form = reactive({ email: "", password: "" });
const errorMessage = ref("");
const isSubmitting = ref(false);

async function handleSubmit() {
  errorMessage.value = "";
  isSubmitting.value = true;
  try {
    await auth.login(form);
    const redirect = typeof route.query.redirect === "string" ? route.query.redirect : "/";
    router.push(redirect);
  } catch (error) {
    if (error instanceof AxiosError) {
      const data = error.response?.data as ApiErrorBody | undefined;
      errorMessage.value = data?.message ?? "Unable to log in. Please try again.";
    } else {
      errorMessage.value = "Unable to log in. Please try again.";
    }
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-yulda-black">Welcome back</h1>
    <p class="mt-2 text-sm text-yulda-gray-500">Log in to continue to Yulda.</p>

    <form class="mt-8 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <BaseInput v-model="form.email" type="email" label="Email" placeholder="you@example.com" autocomplete="email" required />
      <BaseInput v-model="form.password" type="password" label="Password" placeholder="••••••••" autocomplete="current-password" required />

      <div class="flex justify-end">
        <RouterLink to="/forgot-password" class="text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
          Forgot password?
        </RouterLink>
      </div>

      <p v-if="errorMessage" class="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">{{ errorMessage }}</p>

      <BaseButton type="submit" full-width :loading="isSubmitting">Log in</BaseButton>
    </form>

    <p class="mt-8 text-sm text-yulda-gray-500">
      Don't have an account?
      <RouterLink to="/signup" class="font-semibold text-yulda-black">Sign up</RouterLink>
    </p>
  </div>
</template>
