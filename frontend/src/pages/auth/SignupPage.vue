<script setup lang="ts">
import { reactive, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { AxiosError } from "axios";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import { useAuthStore } from "@/stores/authStore";
import type { ApiErrorBody } from "@/types/api";

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
      errorMessage.value = data?.message ?? "Unable to create your account.";
    } else {
      errorMessage.value = "Unable to create your account.";
    }
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-yulda-black">Create your account</h1>
    <p class="mt-2 text-sm text-yulda-gray-500">Join Yulda to ride, deliver, work and more.</p>

    <form class="mt-8 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <BaseInput v-model="form.name" label="Full name" placeholder="Jane Doe" autocomplete="name" required />
      <BaseInput v-model="form.email" type="email" label="Email" placeholder="you@example.com" autocomplete="email" required />
      <BaseInput v-model="form.password" type="password" label="Password" placeholder="At least 8 characters" autocomplete="new-password" required />

      <p v-if="errorMessage" class="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">{{ errorMessage }}</p>

      <BaseButton type="submit" full-width :loading="isSubmitting">Create account</BaseButton>
    </form>

    <p class="mt-8 text-sm text-yulda-gray-500">
      Already have an account?
      <RouterLink to="/login" class="font-semibold text-yulda-black">Log in</RouterLink>
    </p>
  </div>
</template>
