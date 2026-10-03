<script setup lang="ts">
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRouter } from "vue-router";
import { ArrowLeft } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import PhotoUploader from "@/components/common/PhotoUploader.vue";
import { useMarketplaceStore } from "@/stores/marketplaceStore";
import type { ContactMethod, ListingCategory, ListingCondition } from "@/types/marketplace";

const { t } = useI18n();
const router = useRouter();
const store = useMarketplaceStore();

const categories: ListingCategory[] = ["ELECTRONICS", "FURNITURE", "BIKES", "CLOTHING", "FOOD", "FREE", "OTHER"];
const conditions: ListingCondition[] = ["NEW", "USED"];
const contactMethods: ContactMethod[] = ["PHONE", "CHAT", "KAKAOTALK"];

const form = reactive({
  category: "ELECTRONICS" as ListingCategory,
  title: "",
  description: "",
  price: "",
  condition: "USED" as ListingCondition,
  city: "",
  contact_method: "CHAT" as ContactMethod,
  contact_value: "",
  photos: [] as string[],
});
const isSubmitting = ref(false);

async function handleSubmit() {
  if (!form.title.trim() || !form.description.trim() || !form.contact_value.trim()) return;
  isSubmitting.value = true;
  try {
    const listing = await store.createListing({
      ...form,
      price: Number(form.price) || 0,
      city: form.city || undefined,
    });
    router.push(`/marketplace/${listing.id}`);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-10">
    <RouterLink to="/marketplace" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("marketplace.backToFeed") }}
    </RouterLink>

    <h1 class="mt-4 text-2xl font-bold text-yulda-black">{{ t("marketplace.newListing") }}</h1>

    <form class="mt-6 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <div>
        <label class="label">{{ t("marketplace.categoryLabel") }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="category in categories"
            :key="category"
            type="button"
            class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
            :class="form.category === category ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
            @click="form.category = category"
          >
            {{ t(`marketplace.category.${category}`) }}
          </button>
        </div>
      </div>

      <div>
        <label class="label">{{ t("marketplace.photosLabel") }}</label>
        <PhotoUploader v-model="form.photos" folder="marketplace" />
      </div>

      <BaseInput v-model="form.title" :label="t('marketplace.titleLabel')" :placeholder="t('marketplace.titlePlaceholder')" required />
      <BaseTextarea v-model="form.description" :label="t('marketplace.descriptionLabel')" :placeholder="t('marketplace.descriptionPlaceholder')" :rows="6" required />

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <BaseInput v-model="form.price" type="number" :label="t('marketplace.priceLabel')" :placeholder="t('marketplace.pricePlaceholder')" required />
        <div>
          <label class="label">{{ t("marketplace.conditionLabel") }}</label>
          <select v-model="form.condition" class="input">
            <option v-for="condition in conditions" :key="condition" :value="condition">
              {{ t(`marketplace.condition.${condition}`) }}
            </option>
          </select>
        </div>
      </div>

      <BaseInput v-model="form.city" :label="t('marketplace.city')" />

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label class="label">{{ t("marketplace.contactMethodLabel") }}</label>
          <select v-model="form.contact_method" class="input">
            <option v-for="method in contactMethods" :key="method" :value="method">
              {{ t(`marketplace.contactMethod.${method}`) }}
            </option>
          </select>
        </div>
        <BaseInput v-model="form.contact_value" :label="t('marketplace.contactValueLabel')" :placeholder="t('marketplace.contactValuePlaceholder')" required />
      </div>

      <BaseButton type="submit" full-width :loading="isSubmitting">{{ t("marketplace.publish") }}</BaseButton>
    </form>
  </div>
</template>
