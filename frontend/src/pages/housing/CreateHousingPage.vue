<script setup lang="ts">
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRouter } from "vue-router";
import { ArrowLeft } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import PhotoUploader from "@/components/common/PhotoUploader.vue";
import { useHousingStore } from "@/stores/housingStore";
import type { HousingAmenity, HousingType } from "@/types/housing";

const { t } = useI18n();
const router = useRouter();
const store = useHousingStore();

const types: HousingType[] = ["ONE_ROOM", "TWO_ROOM", "ROOMMATE", "APARTMENT", "COMMERCIAL"];
const amenitiesList: HousingAmenity[] = ["FRIDGE", "WASHER", "AC", "PARKING"];

const form = reactive({
  housing_type: "ONE_ROOM" as HousingType,
  title: "",
  description: "",
  deposit: "",
  monthly_rent: "",
  maintenance_fee: "",
  amenities: [] as HousingAmenity[],
  move_in_date: "",
  city: "",
  metro_station: "",
  contact_value: "",
  photos: [] as string[],
});
const isSubmitting = ref(false);

function toggleAmenity(amenity: HousingAmenity) {
  const index = form.amenities.indexOf(amenity);
  if (index === -1) {
    form.amenities.push(amenity);
  } else {
    form.amenities.splice(index, 1);
  }
}

async function handleSubmit() {
  if (!form.title.trim() || !form.description.trim() || !form.contact_value.trim()) return;
  isSubmitting.value = true;
  try {
    const listing = await store.createListing({
      ...form,
      deposit: Number(form.deposit) || 0,
      monthly_rent: Number(form.monthly_rent) || 0,
      maintenance_fee: Number(form.maintenance_fee) || 0,
      move_in_date: form.move_in_date || undefined,
      city: form.city || undefined,
      metro_station: form.metro_station || undefined,
    });
    router.push(`/housing/${listing.id}`);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-10">
    <RouterLink to="/housing" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("housing.backToFeed") }}
    </RouterLink>

    <h1 class="mt-4 text-2xl font-bold text-yulda-black">{{ t("housing.newListing") }}</h1>

    <form class="mt-6 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <div>
        <label class="label">{{ t("housing.allTypes") }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="type in types"
            :key="type"
            type="button"
            class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
            :class="form.housing_type === type ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
            @click="form.housing_type = type"
          >
            {{ t(`housing.type.${type}`) }}
          </button>
        </div>
      </div>

      <div>
        <label class="label">{{ t("housing.photosLabel") }}</label>
        <PhotoUploader v-model="form.photos" folder="housing" />
      </div>

      <BaseInput v-model="form.title" :label="t('housing.titleLabel')" :placeholder="t('housing.titlePlaceholder')" required />
      <BaseTextarea v-model="form.description" :label="t('housing.descriptionLabel')" :placeholder="t('housing.descriptionPlaceholder')" :rows="6" required />

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <BaseInput v-model="form.deposit" type="number" :label="t('housing.deposit')" required />
        <BaseInput v-model="form.monthly_rent" type="number" :label="t('housing.monthlyRent')" required />
        <BaseInput v-model="form.maintenance_fee" type="number" :label="t('housing.maintenanceFee')" />
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <BaseInput v-model="form.city" :label="t('housing.city')" />
        <BaseInput v-model="form.metro_station" :label="t('housing.metroStation')" />
        <BaseInput v-model="form.move_in_date" type="date" :label="t('housing.moveInDate')" />
      </div>

      <div>
        <label class="label">{{ t("housing.amenitiesLabel") }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="amenity in amenitiesList"
            :key="amenity"
            type="button"
            class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
            :class="form.amenities.includes(amenity) ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
            @click="toggleAmenity(amenity)"
          >
            {{ t(`housing.amenity.${amenity}`) }}
          </button>
        </div>
      </div>

      <BaseInput v-model="form.contact_value" :label="t('housing.contactValueLabel')" :placeholder="t('housing.contactValuePlaceholder')" required />

      <BaseButton type="submit" full-width :loading="isSubmitting">{{ t("housing.publish") }}</BaseButton>
    </form>
  </div>
</template>
