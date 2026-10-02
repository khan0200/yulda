<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string;
    label?: string;
    type?: string;
    placeholder?: string;
    error?: string;
    required?: boolean;
    autocomplete?: string;
  }>(),
  {
    type: "text",
    label: undefined,
    placeholder: undefined,
    error: undefined,
    required: false,
    autocomplete: undefined,
  },
);

defineEmits<{ "update:modelValue": [value: string] }>();
</script>

<template>
  <div>
    <label v-if="label" class="label">{{ label }}<span v-if="required" class="text-yulda-gold"> *</span></label>
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :autocomplete="autocomplete"
      class="input"
      :class="{ 'border-red-400 focus:border-red-400 focus:ring-red-200': error }"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="mt-1.5 text-sm text-red-500">{{ error }}</p>
  </div>
</template>
