<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink, useRouter } from "vue-router";
import { ArrowLeft } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import InteractiveMap from "@/components/common/InteractiveMap.vue";
import PhotoUploader from "@/components/common/PhotoUploader.vue";
import SimpleAutocomplete from "@/components/common/SimpleAutocomplete.vue";
import { getModelsForMake, VEHICLE_MAKES } from "@/data/vehicleCatalog";
import { useAutoStore } from "@/stores/autoStore";
import type { AccidentHistory, AutoListingType, BodyType, FuelType, TransmissionType } from "@/types/auto";
import type { GeocodedLocation } from "@/utils/geo";

const { t } = useI18n();
const router = useRouter();
const store = useAutoStore();

const listingTypes: AutoListingType[] = ["SALE", "RENTAL"];
const fuelTypes: FuelType[] = ["GASOLINE", "DIESEL", "LPG", "HYBRID", "ELECTRIC"];
const transmissions: TransmissionType[] = ["AUTOMATIC", "MANUAL"];
const bodyTypes: BodyType[] = ["SEDAN", "SUV", "HATCHBACK", "WAGON", "MINIVAN", "PICKUP", "COUPE", "CONVERTIBLE", "VAN"];
const accidentHistories: AccidentHistory[] = ["NONE", "MINOR", "MAJOR"];

const selectedCoords = ref<[number, number] | null>(null);

function handleMapLocation(loc: GeocodedLocation) {
  if (loc.city) form.city = loc.city;
  else if (loc.name) form.city = loc.name;
  if (typeof loc.lat === "number" && typeof loc.lon === "number") {
    selectedCoords.value = [loc.lon, loc.lat];
  }
}

const form = reactive({
  listing_type: "SALE" as AutoListingType,
  make: "",
  model: "",
  year: "",
  mileage_km: "",
  fuel_type: "GASOLINE" as FuelType,
  transmission: "AUTOMATIC" as TransmissionType,
  price: "",
  rental_price_per_day: "",
  description: "",
  city: "",
  contact_value: "",
  photos: [] as string[],
  body_type: "" as BodyType | "",
  color: "",
  accident_history: "" as AccidentHistory | "",
  owner_count: "",
  credit_available: false,
});
const isSubmitting = ref(false);

const modelOptions = computed(() => getModelsForMake(form.make));

watch(() => form.make, (newMake, oldMake) => {
  if (newMake !== oldMake) form.model = "";
});

async function handleSubmit() {
  if (!form.make.trim() || !form.model.trim() || !form.description.trim() || !form.contact_value.trim()) return;
  isSubmitting.value = true;
  try {
    const listing = await store.createListing({
      ...form,
      year: Number(form.year) || new Date().getFullYear(),
      mileage_km: Number(form.mileage_km) || 0,
      price: Number(form.price) || 0,
      rental_price_per_day: form.rental_price_per_day ? Number(form.rental_price_per_day) : undefined,
      city: form.city || undefined,
      location: selectedCoords.value ? { type: "Point", coordinates: selectedCoords.value } : undefined,
      body_type: form.body_type || undefined,
      color: form.color || undefined,
      accident_history: form.accident_history || undefined,
      owner_count: form.owner_count ? Number(form.owner_count) : undefined,
      credit_available: form.credit_available,
    });
    router.push(`/auto/${listing.id}`);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-10">
    <RouterLink to="/auto" class="inline-flex items-center gap-1.5 text-sm font-medium text-yulda-gray-600 hover:text-yulda-black">
      <ArrowLeft class="h-4 w-4" />
      {{ t("auto.backToFeed") }}
    </RouterLink>

    <h1 class="mt-4 text-2xl font-bold text-yulda-black">{{ t("auto.newListing") }}</h1>

    <form class="mt-6 flex flex-col gap-4" @submit.prevent="handleSubmit">
      <div>
        <label class="label">{{ t("auto.listingType.SALE") }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="type in listingTypes"
            :key="type"
            type="button"
            class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
            :class="form.listing_type === type ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
            @click="form.listing_type = type"
          >
            {{ t(`auto.listingType.${type}`) }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label class="label">{{ t("auto.make") }}</label>
          <SimpleAutocomplete v-model="form.make" :options="VEHICLE_MAKES" placeholder="Hyundai" />
        </div>
        <div>
          <label class="label">{{ t("auto.model") }}</label>
          <SimpleAutocomplete
            v-model="form.model"
            :options="modelOptions"
            :disabled="!form.make.trim()"
            :placeholder="form.make.trim() ? t('auto.modelPlaceholder') : t('auto.make')"
          />
        </div>
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <BaseInput v-model="form.year" type="number" :label="t('auto.year')" :placeholder="t('auto.yearPlaceholder')" required />
        <BaseInput v-model="form.mileage_km" type="number" :label="t('auto.mileage')" :placeholder="t('auto.mileagePlaceholder')" required />
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label class="label">{{ t("auto.fuelType.GASOLINE") }}</label>
          <select v-model="form.fuel_type" class="input">
            <option v-for="fuel in fuelTypes" :key="fuel" :value="fuel">{{ t(`auto.fuelType.${fuel}`) }}</option>
          </select>
        </div>
        <div>
          <label class="label">{{ t("auto.transmission.AUTOMATIC") }}</label>
          <select v-model="form.transmission" class="input">
            <option v-for="tr in transmissions" :key="tr" :value="tr">{{ t(`auto.transmission.${tr}`) }}</option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <BaseInput v-model="form.price" type="number" prefix="₩" suffix="KRW" :label="t('auto.price')" required />
        <BaseInput
          v-if="form.listing_type === 'RENTAL'"
          v-model="form.rental_price_per_day"
          type="number"
          prefix="₩"
          suffix="KRW"
          :label="t('auto.rentalPricePerDay')"
        />
      </div>

      <BaseInput v-model="form.city" :label="t('auto.city')" />

      <!-- Interactive Map for pinpointing car location -->
      <div class="mt-1">
        <InteractiveMap mode="picker" label="Xaritada avtomobil turgan joyni belgilang (GPS yoki xaritaga bosib)" height="300px" @select="handleMapLocation" />
      </div>

      <!-- Optional details: body type, color, accident history, ownership -->
      <div class="rounded-xl border border-yulda-gray-100 p-4">
        <p class="text-sm font-semibold text-yulda-black">{{ t("housing.detailsLabel") }}</p>
        <p class="mt-0.5 text-xs text-yulda-gray-400">{{ t("housing.optionalHint") }}</p>

        <div class="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label class="label">{{ t("auto.bodyType.label") }}</label>
            <select v-model="form.body_type" class="input">
              <option value="">{{ t("auto.bodyType.all") }}</option>
              <option v-for="bt in bodyTypes" :key="bt" :value="bt">{{ t(`auto.bodyType.${bt}`) }}</option>
            </select>
          </div>
          <BaseInput v-model="form.color" :label="t('auto.color')" :placeholder="t('auto.colorPlaceholder')" />
        </div>

        <div class="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label class="label">{{ t("auto.accidentHistory.label") }}</label>
            <select v-model="form.accident_history" class="input">
              <option value="">{{ t("auto.accidentHistory.all") }}</option>
              <option v-for="ah in accidentHistories" :key="ah" :value="ah">{{ t(`auto.accidentHistory.${ah}`) }}</option>
            </select>
          </div>
          <BaseInput v-model="form.owner_count" type="number" :label="t('auto.ownerCount')" />
        </div>

        <label class="mt-4 flex items-center gap-2 text-sm text-yulda-gray-700">
          <input v-model="form.credit_available" type="checkbox" class="h-4 w-4 rounded border-yulda-gray-300" />
          {{ t("auto.creditAvailable") }}
        </label>
      </div>

      <div>
        <label class="label">{{ t("auto.photosLabel") }}</label>
        <PhotoUploader v-model="form.photos" folder="auto" />
      </div>

      <BaseTextarea v-model="form.description" :label="t('auto.descriptionLabel')" :placeholder="t('auto.descriptionPlaceholder')" :rows="6" required />
      <BaseInput v-model="form.contact_value" :label="t('auto.contactValueLabel')" :placeholder="t('auto.contactValuePlaceholder')" required />

      <BaseButton type="submit" full-width :loading="isSubmitting">{{ t("auto.publish") }}</BaseButton>
    </form>
  </div>
</template>
