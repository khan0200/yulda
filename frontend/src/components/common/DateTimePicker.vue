<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { ChevronLeft, ChevronRight, Calendar, Clock } from "lucide-vue-next";

const props = defineProps<{ modelValue: string; min?: string }>();
const emit = defineEmits<{ "update:modelValue": [v: string] }>();

// ── Parse incoming value ────────────────────────────────────────────────────
function parseValue(val: string) {
  if (!val) {
    const n = new Date();
    return { y: n.getFullYear(), m: n.getMonth(), d: n.getDate(), h: n.getHours(), min: n.getMinutes() };
  }
  const dt = new Date(val);
  return { y: dt.getFullYear(), m: dt.getMonth(), d: dt.getDate(), h: dt.getHours(), min: dt.getMinutes() };
}

const initial = parseValue(props.modelValue);
const selYear  = ref(initial.y);
const selMonth = ref(initial.m);
const selDay   = ref(initial.d);
const selHour  = ref(initial.h);
const selMin   = ref(initial.min);

const calYear  = ref(initial.y);
const calMonth = ref(initial.m);

const showCal  = ref(false);
const rootEl   = ref<HTMLElement | null>(null);

function onClickOutside(e: MouseEvent) {
  if (rootEl.value && !rootEl.value.contains(e.target as Node)) {
    showCal.value = false;
  }
}
onMounted(() => document.addEventListener("mousedown", onClickOutside));
onUnmounted(() => document.removeEventListener("mousedown", onClickOutside));

// ── Min date ────────────────────────────────────────────────────────────────
const minDate = computed(() => props.min ? new Date(props.min) : null);

function isPast(y: number, m: number, d: number) {
  if (!minDate.value) return false;
  const mn = minDate.value;
  const a = y * 10000 + m * 100 + d;
  const b = mn.getFullYear() * 10000 + mn.getMonth() * 100 + mn.getDate();
  return a < b;
}

// ── Calendar grid ───────────────────────────────────────────────────────────
const MONTHS = ["Yanvar","Fevral","Mart","Aprel","May","Iyun","Iyul","Avgust","Sentyabr","Oktyabr","Noyabr","Dekabr"];
const DAYS   = ["Du","Se","Ch","Pa","Ju","Sh","Ya"];

const calDays = computed(() => {
  const first = new Date(calYear.value, calMonth.value, 1);
  const last  = new Date(calYear.value, calMonth.value + 1, 0);
  const startDow = (first.getDay() + 6) % 7; // Monday=0
  const cells: Array<{ d: number; cur: boolean; past: boolean } | null> = [];
  for (let i = 0; i < startDow; i++) cells.push(null);
  for (let d = 1; d <= last.getDate(); d++) {
    cells.push({ d, cur: calMonth.value === selMonth.value && calYear.value === selYear.value && d === selDay.value, past: isPast(calYear.value, calMonth.value, d) });
  }
  while (cells.length % 7 !== 0) cells.push(null);
  return cells;
});

function prevMonth() { if (calMonth.value === 0) { calMonth.value = 11; calYear.value--; } else calMonth.value--; }
function nextMonth() { if (calMonth.value === 11) { calMonth.value = 0; calYear.value++; } else calMonth.value++; }

function pickDay(d: number, past: boolean) {
  if (past) return;
  selDay.value = d; selMonth.value = calMonth.value; selYear.value = calYear.value;
  showCal.value = false;
  emitValue();
}

// ── Hours / Minutes ─────────────────────────────────────────────────────────
const hours   = Array.from({ length: 24 }, (_, i) => i);
const minutes = Array.from({ length: 12 }, (_, i) => i * 5);

function setHour(h: number) { selHour.value = h; emitValue(); }
function setMin(m: number)  { selMin.value = m; emitValue(); }

// ── Emit ────────────────────────────────────────────────────────────────────
function pad(n: number) { return String(n).padStart(2, "0"); }
function emitValue() {
  const v = `${selYear.value}-${pad(selMonth.value + 1)}-${pad(selDay.value)}T${pad(selHour.value)}:${pad(selMin.value)}`;
  emit("update:modelValue", v);
}

// Sync if parent changes value externally
watch(() => props.modelValue, (val) => {
  const p = parseValue(val);
  selYear.value = p.y; selMonth.value = p.m; selDay.value = p.d;
  selHour.value = p.h; selMin.value = p.min;
  calYear.value = p.y; calMonth.value = p.m;
});

const dateLabel = computed(() =>
  `${selYear.value}-${pad(selMonth.value + 1)}-${pad(selDay.value)}`
);
</script>

<template>
  <div ref="rootEl" class="flex gap-3">
    <!-- ── DATE picker ─────────────────────────────────────────── -->
    <div class="relative flex-1">
      <button
        type="button"
        class="input flex w-full items-center gap-2 text-left"
        @click="showCal = !showCal"
      >
        <Calendar class="h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
        <span class="font-medium text-yulda-black">{{ dateLabel }}</span>
      </button>

      <!-- Calendar dropdown -->
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
          class="absolute left-0 top-[calc(100%+6px)] z-50 w-72 rounded-2xl border border-yulda-gray-100 bg-white p-4 shadow-xl"
        >
          <!-- Month nav -->
          <div class="mb-3 flex items-center justify-between">
            <button type="button" class="flex h-8 w-8 items-center justify-center rounded-lg hover:bg-yulda-gray-100" @click="prevMonth">
              <ChevronLeft class="h-4 w-4" />
            </button>
            <span class="text-sm font-bold text-yulda-black">{{ MONTHS[calMonth] }} {{ calYear }}</span>
            <button type="button" class="flex h-8 w-8 items-center justify-center rounded-lg hover:bg-yulda-gray-100" @click="nextMonth">
              <ChevronRight class="h-4 w-4" />
            </button>
          </div>

          <!-- Day headers -->
          <div class="mb-1 grid grid-cols-7 text-center">
            <span v-for="d in DAYS" :key="d" class="py-1 text-xs font-semibold text-yulda-gray-400">{{ d }}</span>
          </div>

          <!-- Day cells -->
          <div class="grid grid-cols-7 gap-y-1 text-center text-sm">
            <div v-for="(cell, i) in calDays" :key="i">
              <button
                v-if="cell"
                type="button"
                class="mx-auto flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium transition-colors"
                :class="[
                  cell.past ? 'cursor-not-allowed text-yulda-gray-200' :
                  cell.cur  ? 'bg-yulda-black text-white shadow-md' :
                              'text-yulda-black hover:bg-yulda-yellow/30'
                ]"
                :disabled="cell.past"
                @click="pickDay(cell.d, cell.past)"
              >
                {{ cell.d }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ── TIME picker ─────────────────────────────────────────── -->
    <div class="relative w-44">
      <div class="input flex items-center gap-2">
        <Clock class="h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
        <!-- Hour -->
        <select
          :value="selHour"
          class="flex-1 bg-transparent text-sm font-medium text-yulda-black outline-none"
          @change="setHour(+($event.target as HTMLSelectElement).value)"
        >
          <option v-for="h in hours" :key="h" :value="h">{{ pad(h) }}</option>
        </select>
        <span class="font-bold text-yulda-gray-400">:</span>
        <!-- Minute -->
        <select
          :value="selMin"
          class="flex-1 bg-transparent text-sm font-medium text-yulda-black outline-none"
          @change="setMin(+($event.target as HTMLSelectElement).value)"
        >
          <option v-for="m in minutes" :key="m" :value="m">{{ pad(m) }}</option>
        </select>
      </div>
    </div>
  </div>
</template>
