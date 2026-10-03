<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string | number;
    label?: string;
    type?: string;
    placeholder?: string;
    error?: string;
    required?: boolean;
    autocomplete?: string;
    prefix?: string;
    suffix?: string;
  }>(),
  {
    type: "text",
    label: undefined,
    placeholder: undefined,
    error: undefined,
    required: false,
    autocomplete: undefined,
    prefix: undefined,
    suffix: undefined,
  },
);

defineEmits<{ "update:modelValue": [value: string] }>();
defineOptions({ inheritAttrs: false });
</script>

<template>
  <div>
    <label v-if="label" class="label">{{ label }}<span v-if="required" class="text-yulda-gold"> *</span></label>
    <div class="relative flex items-center">
      <div v-if="prefix || $slots.prefix" class="pointer-events-none absolute left-3 flex items-center text-sm font-semibold text-yulda-gray-400 select-none">
        <slot name="prefix">{{ prefix }}</slot>
      </div>
      <input
        v-bind="$attrs"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        class="input w-full"
        :class="[
          { 'border-red-400 focus:border-red-400 focus:ring-red-200': error },
          prefix || $slots.prefix ? '!pl-8' : '',
          suffix || $slots.suffix ? '!pr-16' : '',
        ]"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <div v-if="suffix || $slots.suffix" class="pointer-events-none absolute right-2.5 flex items-center select-none">
        <slot name="suffix">
          <span class="rounded-lg border border-yulda-gray-200 bg-yulda-gray-100 px-2 py-0.5 text-xs font-bold text-yulda-gray-600 shadow-xs">
            {{ suffix }}
          </span>
        </slot>
      </div>
    </div>
    <p v-if="error" class="mt-1.5 text-sm text-red-500">{{ error }}</p>
  </div>
</template>
