<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { Car } from "lucide-vue-next";

const props = defineProps<{ modelValue: string; placeholder?: string }>();
const emit = defineEmits<{ "update:modelValue": [v: string] }>();

const LS_KEY = "yulda_custom_vehicles";

const BUILTIN: string[] = [
  "Hyundai Sonata",
  "Hyundai Grandeur",
  "Hyundai Avante",
  "Hyundai Ioniq 6",
  "Hyundai Staria",
  "Kia K5",
  "Kia K8",
  "Kia Carnival",
  "Kia EV6",
  "Kia Morning",
  "Genesis G80",
  "Genesis G90",
  "Ssangyong Rexton",
  "Chevrolet Malibu",
  "Renault Samsung SM6",
  "Toyota Camry",
  "Mercedes-Benz E-Class",
  "BMW 5 Series",
];

const customVehicles = ref<string[]>([]);

onMounted(() => {
  try {
    const stored = localStorage.getItem(LS_KEY);
    if (stored) customVehicles.value = JSON.parse(stored);
  } catch {}
});

const allVehicles = computed(() => {
  const all = [...BUILTIN, ...customVehicles.value.filter((v) => !BUILTIN.includes(v))];
  return [...new Set(all)];
});

const isOpen = ref(false);
const inputEl = ref<HTMLInputElement | null>(null);

const filtered = computed(() => {
  const q = props.modelValue.trim().toLowerCase();
  if (!q) return allVehicles.value.slice(0, 10);
  return allVehicles.value.filter((v) => v.toLowerCase().includes(q)).slice(0, 10);
});

function select(v: string) {
  emit("update:modelValue", v);
  isOpen.value = false;
}

function onBlur() {
  setTimeout(() => {
    isOpen.value = false;
    saveCustomIfNew();
  }, 150);
}

function saveCustomIfNew() {
  const v = props.modelValue.trim();
  if (!v) return;
  if (BUILTIN.some((b) => b.toLowerCase() === v.toLowerCase())) return;
  if (customVehicles.value.some((c) => c.toLowerCase() === v.toLowerCase())) return;
  customVehicles.value = [v, ...customVehicles.value].slice(0, 30);
  try { localStorage.setItem(LS_KEY, JSON.stringify(customVehicles.value)); } catch {}
}

function onClickOutside(e: MouseEvent) {
  if (inputEl.value && !inputEl.value.closest(".vehicle-autocomplete")?.contains(e.target as Node)) {
    isOpen.value = false;
  }
}

onMounted(() => document.addEventListener("mousedown", onClickOutside));
onUnmounted(() => document.removeEventListener("mousedown", onClickOutside));

function highlightMatch(text: string): string {
  const q = props.modelValue.trim();
  if (!q) return text;
  const idx = text.toLowerCase().indexOf(q.toLowerCase());
  if (idx === -1) return text;
  return (
    text.slice(0, idx) +
    `<mark class="bg-yulda-yellow/60 text-yulda-black rounded px-0.5">${text.slice(idx, idx + q.length)}</mark>` +
    text.slice(idx + q.length)
  );
}
</script>

<template>
  <div class="vehicle-autocomplete relative">
    <div class="relative">
      <Car class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-yulda-gray-400" />
      <input
        ref="inputEl"
        :value="modelValue"
        type="text"
        :placeholder="placeholder ?? 'Masalan: Hyundai Sonata'"
        class="input pl-9"
        autocomplete="off"
        @input="emit('update:modelValue', ($event.target as HTMLInputElement).value); isOpen = true"
        @focus="isOpen = true"
        @blur="onBlur"
        @keydown.escape="isOpen = false"
        @keydown.enter.prevent="filtered[0] && select(filtered[0])"
      />
    </div>
    <Transition
      enter-active-class="transition-all duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition-all duration-100 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <ul
        v-if="isOpen && filtered.length"
        class="absolute z-50 mt-1 max-h-56 w-full overflow-y-auto rounded-xl border border-yulda-gray-100 bg-white shadow-lg"
      >
        <li
          v-for="vehicle in filtered"
          :key="vehicle"
          class="flex cursor-pointer items-center gap-2.5 px-3 py-2.5 text-sm transition-colors hover:bg-yulda-yellow/10"
          @mousedown.prevent="select(vehicle)"
        >
          <Car class="h-3.5 w-3.5 flex-shrink-0 text-yulda-gray-400" />
          <span v-html="highlightMatch(vehicle)" />
          <span
            v-if="!BUILTIN.includes(vehicle)"
            class="ml-auto rounded-full bg-yulda-gray-100 px-2 py-0.5 text-xs text-yulda-gray-400"
          >
            Saqlangan
          </span>
        </li>
      </ul>
    </Transition>
  </div>
</template>
