<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { Minus, Plus } from "lucide-vue-next";

import PlaceAutocomplete from "@/components/common/PlaceAutocomplete.vue";
import type { PlaceCountry } from "@/types/place";
import type { RouteStop } from "@/types/route";

const props = withDefaults(
  defineProps<{
    modelValue: RouteStop[];
    fixedCountry?: PlaceCountry;
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
  const last = props.modelValue[props.modelValue.length - 1];
  const newStops = [...props.modelValue];
  newStops.splice(newStops.length - 1, 0, { name: "", country: last?.country ?? props.fixedCountry ?? "KR" });
  emit("update:modelValue", newStops);
}

function removeStop(index: number) {
  if (props.modelValue.length <= 2) return;
  emit("update:modelValue", props.modelValue.filter((_, i) => i !== index));
}

function dotType(index: number) {
  if (index === 0) return "origin";
  if (index === props.modelValue.length - 1) return "dest";
  return "via";
}
</script>

<template>
  <div class="flex flex-col">
    <div v-for="(stop, index) in modelValue" :key="index" class="flex items-stretch">

      <!-- Left column: dot + dashed connector -->
      <div class="flex w-7 flex-shrink-0 flex-col items-center">
        <div class="relative z-10 mt-[14px] flex-shrink-0">
          <div v-if="dotType(index) === 'origin'" class="h-3 w-3 rounded-full bg-blue-500 ring-2 ring-blue-200" />
          <div v-else-if="dotType(index) === 'dest'" class="h-3 w-3 rounded-full bg-red-500 ring-2 ring-red-200" />
          <div v-else class="h-3 w-3 rounded-full border-2 border-yulda-gray-400 bg-white" />
        </div>
        <div v-if="index < modelValue.length - 1" class="my-0.5 flex-1 border-l-2 border-dashed border-yulda-gray-300" />
      </div>

      <!-- Input + action buttons -->
      <div class="mb-2 ml-2.5 flex flex-1 items-center gap-2">
        <div class="flex-1">
          <select
            v-if="!fixedCountry"
            :value="stop.country"
            class="input mb-1 w-24 text-xs"
            @change="updateStop(index, { country: ($event.target as HTMLSelectElement).value as PlaceCountry, name: '' })"
          >
            <option v-for="code in countryOptions" :key="code" :value="code">{{ code }}</option>
          </select>
          <PlaceAutocomplete
            :model-value="stop.name"
            :country="fixedCountry ?? stop.country as PlaceCountry"
            :placeholder="
              index === 0 ? t('route.fromCity')
              : index === modelValue.length - 1 ? t('route.toCity')
              : t('route.stopPlaceholder')
            "
            @update:model-value="(v) => updateStop(index, { name: v })"
            @select="(place) => place && updateStop(index, { name: place.name })"
          />
        </div>

        <!-- Minus: remove waypoint (only middle stops) -->
        <button
          v-if="index > 0 && index < modelValue.length - 1"
          type="button"
          class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border border-yulda-gray-200 bg-white text-yulda-gray-400 shadow-sm transition hover:border-red-300 hover:text-red-500"
          :title="t('route.removeStop')"
          @click="removeStop(index)"
        >
          <Minus class="h-3.5 w-3.5" />
        </button>

        <!-- Plus: add waypoint before destination (only on last row) -->
        <button
          v-if="index === modelValue.length - 1"
          type="button"
          class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border border-yulda-gray-200 bg-white text-yulda-gray-500 shadow-sm transition hover:border-yulda-black hover:text-yulda-black"
          :title="t('route.addStop')"
          @click="addStop"
        >
          <Plus class="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  </div>
</template>

