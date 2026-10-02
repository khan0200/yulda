<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string;
    label?: string;
    placeholder?: string;
    error?: string;
    required?: boolean;
    rows?: number;
  }>(),
  {
    label: undefined,
    placeholder: undefined,
    error: undefined,
    required: false,
    rows: 5,
  },
);

defineEmits<{ "update:modelValue": [value: string] }>();
</script>

<template>
  <div>
    <label v-if="label" class="label">{{ label }}<span v-if="required" class="text-yulda-gold"> *</span></label>
    <textarea
      :value="modelValue"
      :placeholder="placeholder"
      :rows="rows"
      class="input resize-none"
      :class="{ 'border-red-400 focus:border-red-400 focus:ring-red-200': error }"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    />
    <p v-if="error" class="mt-1.5 text-sm text-red-500">{{ error }}</p>
  </div>
</template>
