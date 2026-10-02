<script setup lang="ts">
import { useI18n } from "vue-i18n";

import type { CargoCategory } from "@/types/cargo";

const props = defineProps<{ modelValue: CargoCategory[]; label: string }>();
const emit = defineEmits<{ "update:modelValue": [value: CargoCategory[]] }>();
const { t } = useI18n();

const allCategories: CargoCategory[] = [
  "DOCUMENTS",
  "MEDICINE",
  "PERSONAL_ITEMS",
  "FOOD",
  "CLOTHING",
  "ELECTRONICS",
  "PHONE",
  "LAPTOP",
  "GAME_CONSOLE",
  "PERFUME",
  "OTHER",
];

function toggle(category: CargoCategory) {
  const index = props.modelValue.indexOf(category);
  if (index === -1) {
    emit("update:modelValue", [...props.modelValue, category]);
  } else {
    emit(
      "update:modelValue",
      props.modelValue.filter((c) => c !== category),
    );
  }
}
</script>

<template>
  <div>
    <label class="label">{{ label }}</label>
    <div class="flex flex-wrap gap-2">
      <button
        v-for="category in allCategories"
        :key="category"
        type="button"
        class="rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors"
        :class="modelValue.includes(category) ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="toggle(category)"
      >
        {{ t(`cargo.category.${category}`) }}
      </button>
    </div>
  </div>
</template>
