<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { Plus, X } from "lucide-vue-next";

import PlaceAutocomplete from "@/components/common/PlaceAutocomplete.vue";
import type { PlaceCountry } from "@/types/place";
import type { RouteStop } from "@/types/route";

const props = withDefaults(
  defineProps<{
    modelValue: RouteStop[];
    /** Restrict autocomplete to a single country (e.g. Taxi = Korea only). Omit for international (Cargo). */
    fixedCountry?: PlaceCountry;
    /** Country list to offer per-stop when fixedCountry is not set. */
    countryOptions?: PlaceCountry[];
  }>(),
  {
    fixedCountry: undefined,
    countryOptions: () => ["KR", "UZ", "KZ", "KG", "TJ", "TM", "RU"],
  },
);

const emit = defineEmits<{ "update:modelValue": [value: RouteStop[]] }>();
const { t } = useI18n();

function updateStop(index: number, patch: Partial<RouteStop>) {
  const next = props.modelValue.map((stop, i) => (i === index ? { ...stop, ...patch } : stop));
  emit("update:modelValue", next);
}

function addStop() {
  const lastCountry = props.modelValue.at(-1)?.country ?? props.fixedCountry ?? "KR";
  emit("update:modelValue", [...props.modelValue, { name: "", country: lastCountry }]);
}

function removeStop(index: number) {
  if (props.modelValue.length <= 2) return;
  emit(
    "update:modelValue",
    props.modelValue.filter((_, i) => i !== index),
  );
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <div v-for="(stop, index) in modelValue" :key="index" class="flex items-center gap-2">
      <div class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full bg-yulda-gray-100 text-xs font-semibold text-yulda-gray-500">
        {{ index + 1 }}
      </div>

      <select
        v-if="!fixedCountry"
        :value="stop.country"
        class="input w-28 flex-shrink-0"
        @change="updateStop(index, { country: ($event.target as HTMLSelectElement).value as PlaceCountry, name: '' })"
      >
        <option v-for="code in countryOptions" :key="code" :value="code">{{ code }}</option>
      </select>

      <div class="flex-1">
        <PlaceAutocomplete
          :model-value="stop.name"
          :country="fixedCountry ?? stop.country as PlaceCountry"
          :placeholder="t('route.stopPlaceholder')"
          @update:model-value="(value) => updateStop(index, { name: value })"
          @select="(place) => place && updateStop(index, { name: place.name })"
        />
      </div>

      <button
        v-if="modelValue.length > 2"
        type="button"
        class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg text-yulda-gray-400 hover:bg-yulda-gray-100 hover:text-red-500"
        :aria-label="t('route.removeStop')"
        @click="removeStop(index)"
      >
        <X class="h-4 w-4" />
      </button>
    </div>

    <button type="button" class="btn-outline mt-1 self-start" @click="addStop">
      <Plus class="h-4 w-4" />
      {{ t("route.addStop") }}
    </button>
  </div>
</template>
