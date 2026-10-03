<script setup lang="ts">
import { ref, watch } from "vue";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    label?: string;
    placeholder?: string;
    currency?: string;
    prefixSymbol?: string;
    error?: string;
    required?: boolean;
    disabled?: boolean;
    quickAmounts?: number[];
  }>(),
  {
    label: undefined,
    placeholder: "masalan, 70,000",
    currency: "KRW",
    prefixSymbol: "₩",
    error: undefined,
    required: false,
    disabled: false,
    quickAmounts: () => [10000, 30000, 50000, 70000, 100000],
  },
);

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

const inputEl = ref<HTMLInputElement | null>(null);

// Extract numeric or text display from modelValue
function parseModelToDisplay(val: string): string {
  if (!val) return "";
  const clean = val.replace(/\s*(KRW|krw|won|₩|von)\s*/gi, "").trim();
  const digitsOnly = clean.replace(/,/g, "");
  if (/^\d+$/.test(digitsOnly)) {
    const num = parseInt(digitsOnly, 10);
    return num.toLocaleString("en-US");
  }
  return val;
}

const displayValue = ref(parseModelToDisplay(props.modelValue || ""));

watch(
  () => props.modelValue,
  (newVal) => {
    const expected = parseModelToDisplay(newVal || "");
    if (expected !== displayValue.value) {
      displayValue.value = expected;
    }
  },
);

function handleInput(e: Event) {
  const target = e.target as HTMLInputElement;
  const rawInput = target.value;
  const selectionStart = target.selectionStart || 0;

  if (!rawInput.trim()) {
    displayValue.value = "";
    emit("update:modelValue", "");
    return;
  }

  // Count digits before cursor for stable cursor positioning
  const digitsBeforeCursor = rawInput.slice(0, selectionStart).replace(/\D/g, "").length;
  const digitsOnly = rawInput.replace(/\D/g, "");

  if (digitsOnly) {
    const num = parseInt(digitsOnly, 10);
    const formatted = num.toLocaleString("en-US");
    displayValue.value = formatted;
    target.value = formatted;

    // Restore cursor position
    let newCursor = 0;
    let digitsSeen = 0;
    for (let i = 0; i < formatted.length; i++) {
      if (/\d/.test(formatted[i])) {
        digitsSeen++;
      }
      if (digitsSeen === digitsBeforeCursor) {
        newCursor = i + 1;
        break;
      }
    }
    if (digitsBeforeCursor === 0) newCursor = 0;
    if (digitsSeen < digitsBeforeCursor) newCursor = formatted.length;

    target.setSelectionRange(newCursor, newCursor);

    // Emit formatted with KRW
    emit("update:modelValue", `${formatted} ${props.currency}`.trim());
  } else {
    // Non-numeric text (e.g. "Kelishiladi")
    displayValue.value = rawInput;
    emit("update:modelValue", rawInput);
  }
}

function addQuickAmount(amount: number) {
  const currentDigits = displayValue.value.replace(/\D/g, "");
  const current = currentDigits ? parseInt(currentDigits, 10) : 0;
  const next = current + amount;
  const formatted = next.toLocaleString("en-US");
  displayValue.value = formatted;
  emit("update:modelValue", `${formatted} ${props.currency}`.trim());
}
</script>

<template>
  <div class="space-y-1.5">
    <div v-if="label" class="flex items-center justify-between">
      <label class="label !mb-0">
        {{ label }}<span v-if="required" class="text-yulda-gold"> *</span>
      </label>
      <span v-if="currency" class="text-[11px] font-semibold tracking-wider text-yulda-gray-400">
        {{ currency }}
      </span>
    </div>

    <div class="relative flex items-center">
      <!-- Prefix Symbol (₩) -->
      <div
        v-if="prefixSymbol"
        class="pointer-events-none absolute left-3 flex items-center text-sm font-bold text-yulda-gray-400 select-none"
      >
        {{ prefixSymbol }}
      </div>

      <input
        ref="inputEl"
        type="text"
        inputmode="numeric"
        :value="displayValue"
        :placeholder="placeholder"
        :disabled="disabled"
        class="input w-full font-medium transition-all"
        :class="[
          prefixSymbol ? '!pl-8' : '',
          currency ? '!pr-16' : '',
          error ? 'border-red-400 focus:border-red-400 focus:ring-red-200' : '',
        ]"
        @input="handleInput"
      />

      <!-- Suffix Badge (KRW) -->
      <div
        v-if="currency"
        class="pointer-events-none absolute right-2.5 flex items-center select-none"
      >
        <span class="rounded-lg border border-yulda-gray-200 bg-yulda-gray-100 px-2 py-0.5 text-xs font-bold text-yulda-gray-600 shadow-xs">
          {{ currency }}
        </span>
      </div>
    </div>

    <!-- Quick Preset Chips -->
    <div v-if="quickAmounts && quickAmounts.length > 0" class="flex flex-wrap items-center gap-1.5 pt-0.5">
      <button
        v-for="amt in quickAmounts"
        :key="amt"
        type="button"
        class="rounded-lg border border-yulda-gray-200 bg-white px-2 py-0.5 text-[11px] font-medium text-yulda-gray-600 transition-all hover:border-yulda-yellow hover:bg-yulda-yellow/20 hover:text-yulda-black active:scale-95"
        @click="addQuickAmount(amt)"
      >
        +{{ (amt / 1000).toLocaleString() }}k
      </button>
      <button
        v-if="displayValue"
        type="button"
        class="rounded-lg border border-red-100 bg-red-50/50 px-2 py-0.5 text-[11px] font-medium text-red-500 transition-all hover:bg-red-100 active:scale-95"
        @click="displayValue = ''; emit('update:modelValue', '')"
      >
        Tozalash
      </button>
    </div>

    <p v-if="error" class="text-xs text-red-500">{{ error }}</p>
  </div>
</template>
