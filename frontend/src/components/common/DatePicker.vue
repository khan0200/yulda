<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { Calendar, ChevronLeft, ChevronRight, X } from "lucide-vue-next";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    label?: string;
    placeholder?: string;
    min?: string;
    max?: string;
    required?: boolean;
    error?: string;
    disabled?: boolean;
    clearable?: boolean;
  }>(),
  {
    label: undefined,
    placeholder: "YYYY-MM-DD",
    min: undefined,
    max: undefined,
    required: false,
    error: undefined,
    disabled: false,
    clearable: true,
  },
);

const emit = defineEmits<{
  "update:modelValue": [v: string];
}>();

const { locale } = useI18n();

const MONTHS_MAP: Record<string, string[]> = {
  uz: ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"],
  ru: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
  ko: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
  en: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
};

const DAYS_MAP: Record<string, string[]> = {
  uz: ["Du", "Se", "Ch", "Pa", "Ju", "Sh", "Ya"],
  ru: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
  ko: ["월", "화", "수", "목", "금", "토", "일"],
  en: ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
};

const currentMonths = computed(() => MONTHS_MAP[locale.value] || MONTHS_MAP.uz);
const currentDays = computed(() => DAYS_MAP[locale.value] || DAYS_MAP.uz);

function pad(n: number) {
  return String(n).padStart(2, "0");
}

function parseDate(val: string) {
  if (!val) {
    const now = new Date();
    return { y: now.getFullYear(), m: now.getMonth(), d: now.getDate(), hasValue: false };
  }
  const parts = val.split("-");
  if (parts.length === 3) {
    const y = parseInt(parts[0], 10);
    const m = parseInt(parts[1], 10) - 1;
    const d = parseInt(parts[2], 10);
    if (!isNaN(y) && !isNaN(m) && !isNaN(d)) {
      return { y, m, d, hasValue: true };
    }
  }
  const dt = new Date(val);
  if (!isNaN(dt.getTime())) {
    return { y: dt.getFullYear(), m: dt.getMonth(), d: dt.getDate(), hasValue: true };
  }
  const now = new Date();
  return { y: now.getFullYear(), m: now.getMonth(), d: now.getDate(), hasValue: false };
}

const parsed = parseDate(props.modelValue);
const selYear = ref(parsed.hasValue ? parsed.y : null);
const selMonth = ref(parsed.hasValue ? parsed.m : null);
const selDay = ref(parsed.hasValue ? parsed.d : null);

const calYear = ref(parsed.y);
const calMonth = ref(parsed.m);

const showCal = ref(false);
const rootEl = ref<HTMLElement | null>(null);

function onClickOutside(e: MouseEvent) {
  if (rootEl.value && !rootEl.value.contains(e.target as Node)) {
    showCal.value = false;
  }
}

onMounted(() => document.addEventListener("mousedown", onClickOutside));
onUnmounted(() => document.removeEventListener("mousedown", onClickOutside));

watch(
  () => props.modelValue,
  (val) => {
    const p = parseDate(val);
    if (p.hasValue) {
      selYear.value = p.y;
      selMonth.value = p.m;
      selDay.value = p.d;
      calYear.value = p.y;
      calMonth.value = p.m;
    } else {
      selYear.value = null;
      selMonth.value = null;
      selDay.value = null;
    }
  },
);

const minDate = computed(() => (props.min ? parseDate(props.min) : null));
const maxDate = computed(() => (props.max ? parseDate(props.max) : null));

function isDayDisabled(y: number, m: number, d: number) {
  const current = y * 10000 + (m + 1) * 100 + d;
  if (minDate.value && minDate.value.hasValue) {
    const minVal = minDate.value.y * 10000 + (minDate.value.m + 1) * 100 + minDate.value.d;
    if (current < minVal) return true;
  }
  if (maxDate.value && maxDate.value.hasValue) {
    const maxVal = maxDate.value.y * 10000 + (maxDate.value.m + 1) * 100 + maxDate.value.d;
    if (current > maxVal) return true;
  }
  return false;
}

const calDays = computed(() => {
  const first = new Date(calYear.value, calMonth.value, 1);
  const last = new Date(calYear.value, calMonth.value + 1, 0);
  const startDow = (first.getDay() + 6) % 7; // Monday=0
  const cells: Array<{ d: number; isSelected: boolean; isToday: boolean; isDisabled: boolean } | null> = [];

  const now = new Date();
  const todayY = now.getFullYear();
  const todayM = now.getMonth();
  const todayD = now.getDate();

  for (let i = 0; i < startDow; i++) cells.push(null);

  for (let d = 1; d <= last.getDate(); d++) {
    const isSelected =
      selYear.value === calYear.value &&
      selMonth.value === calMonth.value &&
      selDay.value === d;
    const isToday = todayY === calYear.value && todayM === calMonth.value && todayD === d;
    const isDisabled = isDayDisabled(calYear.value, calMonth.value, d);

    cells.push({ d, isSelected, isToday, isDisabled });
  }

  while (cells.length % 7 !== 0) cells.push(null);
  return cells;
});

function prevMonth() {
  if (calMonth.value === 0) {
    calMonth.value = 11;
    calYear.value--;
  } else {
    calMonth.value--;
  }
}

function nextMonth() {
  if (calMonth.value === 11) {
    calMonth.value = 0;
    calYear.value++;
  } else {
    calMonth.value++;
  }
}

function pickDay(d: number, disabled: boolean) {
  if (disabled) return;
  selDay.value = d;
  selMonth.value = calMonth.value;
  selYear.value = calYear.value;
  showCal.value = false;
  emit("update:modelValue", `${selYear.value}-${pad(selMonth.value + 1)}-${pad(selDay.value)}`);
}

function selectToday() {
  const now = new Date();
  const y = now.getFullYear();
  const m = now.getMonth();
  const d = now.getDate();
  if (isDayDisabled(y, m, d)) return;

  selYear.value = y;
  selMonth.value = m;
  selDay.value = d;
  calYear.value = y;
  calMonth.value = m;
  showCal.value = false;
  emit("update:modelValue", `${y}-${pad(m + 1)}-${pad(d)}`);
}

function clearDate() {
  selYear.value = null;
  selMonth.value = null;
  selDay.value = null;
  showCal.value = false;
  emit("update:modelValue", "");
}

const formattedDate = computed(() => {
  if (selYear.value !== null && selMonth.value !== null && selDay.value !== null) {
    return `${selYear.value}-${pad(selMonth.value + 1)}-${pad(selDay.value)}`;
  }
  return "";
});
</script>

<template>
  <div ref="rootEl" class="relative">
    <label v-if="label" class="label">
      {{ label }}<span v-if="required" class="text-yulda-gold"> *</span>
    </label>

    <!-- Display Button/Input -->
    <div class="relative flex items-center">
      <button
        type="button"
        :disabled="disabled"
        class="input flex w-full items-center justify-between gap-2 text-left font-medium transition-all"
        :class="[
          error ? 'border-red-400 focus:border-red-400 focus:ring-red-200' : '',
          disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer hover:border-yulda-gray-400',
        ]"
        @click="showCal = !showCal"
      >
        <div class="flex items-center gap-2 truncate">
          <Calendar class="h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
          <span v-if="formattedDate" class="text-yulda-black font-semibold">{{ formattedDate }}</span>
          <span v-else class="text-yulda-gray-400 font-normal">{{ placeholder }}</span>
        </div>

        <div class="flex items-center gap-1">
          <span
            v-if="clearable && formattedDate && !disabled"
            class="rounded-md p-1 text-yulda-gray-400 hover:bg-yulda-gray-100 hover:text-yulda-black"
            @click.stop="clearDate"
          >
            <X class="h-3.5 w-3.5" />
          </span>
        </div>
      </button>
    </div>

    <!-- Calendar Dropdown Popover -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="showCal"
        class="absolute left-0 top-[calc(100%+6px)] z-50 w-72 rounded-2xl border border-yulda-gray-200 bg-white p-4 shadow-2xl backdrop-blur"
      >
        <!-- Month and Year Navigation -->
        <div class="mb-3 flex items-center justify-between">
          <button
            type="button"
            class="flex h-8 w-8 items-center justify-center rounded-xl text-yulda-gray-600 transition-colors hover:bg-yulda-gray-100 active:scale-95"
            @click="prevMonth"
          >
            <ChevronLeft class="h-4 w-4" />
          </button>
          <span class="text-sm font-bold text-yulda-black">
            {{ currentMonths[calMonth] }} {{ calYear }}
          </span>
          <button
            type="button"
            class="flex h-8 w-8 items-center justify-center rounded-xl text-yulda-gray-600 transition-colors hover:bg-yulda-gray-100 active:scale-95"
            @click="nextMonth"
          >
            <ChevronRight class="h-4 w-4" />
          </button>
        </div>

        <!-- Week Day Headers -->
        <div class="mb-1.5 grid grid-cols-7 text-center">
          <span
            v-for="d in currentDays"
            :key="d"
            class="py-1 text-xs font-bold text-yulda-gray-400"
          >
            {{ d }}
          </span>
        </div>

        <!-- Calendar Days Grid -->
        <div class="grid grid-cols-7 gap-y-1 text-center text-sm">
          <div v-for="(cell, i) in calDays" :key="i" class="flex items-center justify-center">
            <button
              v-if="cell"
              type="button"
              class="flex h-8 w-8 items-center justify-center rounded-full text-xs font-semibold transition-all"
              :class="[
                cell.isDisabled ? 'cursor-not-allowed text-yulda-gray-300' :
                cell.isSelected ? 'bg-yulda-black text-white shadow-md' :
                cell.isToday    ? 'border border-yulda-yellow text-yulda-black font-bold hover:bg-yulda-yellow/20' :
                                  'text-yulda-black hover:bg-yulda-yellow/30 active:scale-95'
              ]"
              :disabled="cell.isDisabled"
              @click="pickDay(cell.d, cell.isDisabled)"
            >
              {{ cell.d }}
            </button>
          </div>
        </div>

        <!-- Action Footer (Bugun / Tozalash) -->
        <div class="mt-3 flex items-center justify-between border-t border-yulda-gray-100 pt-2 text-xs">
          <button
            type="button"
            class="font-semibold text-yulda-gray-500 hover:text-yulda-black transition-colors"
            @click="clearDate"
          >
            Tozalash
          </button>
          <button
            type="button"
            class="font-bold text-yulda-black hover:underline"
            @click="selectToday"
          >
            Bugun
          </button>
        </div>
      </div>
    </Transition>

    <p v-if="error" class="mt-1 text-xs text-red-500">{{ error }}</p>
  </div>
</template>
