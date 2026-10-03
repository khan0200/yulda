<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { Car } from "lucide-vue-next";

const props = defineProps<{ modelValue: string; placeholder?: string }>();
const emit = defineEmits<{ "update:modelValue": [v: string] }>();

const LS_KEY = "yulda_custom_vehicles";

const BUILTIN: string[] = [
  // Hyundai
  "Hyundai Avante", "Hyundai Sonata", "Hyundai Grandeur", "Hyundai Casper",
  "Hyundai Kona", "Hyundai Venue", "Hyundai Tucson", "Hyundai Santa Fe",
  "Hyundai Palisade", "Hyundai Staria", "Hyundai Porter",
  "Hyundai Ioniq 5", "Hyundai Ioniq 6",
  // KIA
  "Kia Morning", "Kia Ray", "Kia K3", "Kia K4", "Kia K5", "Kia K8", "Kia K9",
  "Kia Seltos", "Kia Sportage", "Kia Sorento", "Kia Telluride",
  "Kia Carnival", "Kia Bongo", "Kia EV3", "Kia EV6", "Kia EV9",
  // Genesis
  "Genesis G70", "Genesis G80", "Genesis G90",
  "Genesis GV60", "Genesis GV70", "Genesis GV80", "Genesis GV80 Coupe",
  // Chevrolet
  "Chevrolet Spark", "Chevrolet Malibu", "Chevrolet Trax",
  "Chevrolet Trailblazer", "Chevrolet Equinox", "Chevrolet Traverse",
  "Chevrolet Tahoe", "Chevrolet Colorado",
  // KGM (SsangYong)
  "KGM Tivoli", "KGM Korando", "KGM Torres", "KGM Rexton",
  "KGM Rexton Sports", "KGM Musso", "KGM Torres EVX",
  // Renault Korea
  "Renault SM3", "Renault SM5", "Renault SM6", "Renault XM3",
  "Renault Arkana", "Renault QM6", "Renault Grand Koleos",
  // BMW
  "BMW 1 Series", "BMW 2 Series", "BMW 3 Series", "BMW 4 Series",
  "BMW 5 Series", "BMW 6 Series", "BMW 7 Series",
  "BMW X1", "BMW X3", "BMW X5", "BMW X6", "BMW X7",
  "BMW i4", "BMW i5", "BMW i7", "BMW iX",
  // Mercedes-Benz
  "Mercedes-Benz A-Class", "Mercedes-Benz C-Class", "Mercedes-Benz E-Class",
  "Mercedes-Benz S-Class", "Mercedes-Benz CLA", "Mercedes-Benz CLS",
  "Mercedes-Benz GLA", "Mercedes-Benz GLB", "Mercedes-Benz GLC",
  "Mercedes-Benz GLE", "Mercedes-Benz GLS", "Mercedes-Benz G-Class",
  "Mercedes-Benz EQE", "Mercedes-Benz EQS",
  // Tesla
  "Tesla Model 3", "Tesla Model Y", "Tesla Model S", "Tesla Model X",
  // Audi
  "Audi A3", "Audi A4", "Audi A5", "Audi A6", "Audi A7", "Audi A8",
  "Audi Q3", "Audi Q5", "Audi Q7", "Audi Q8",
  "Audi e-tron", "Audi Q4 e-tron",
  // Volkswagen
  "Volkswagen Golf", "Volkswagen Jetta", "Volkswagen Passat",
  "Volkswagen Arteon", "Volkswagen Tiguan", "Volkswagen Touareg",
  "Volkswagen ID.4",
  // Volvo
  "Volvo S60", "Volvo S90", "Volvo XC40", "Volvo XC60", "Volvo XC90",
  "Volvo EX30", "Volvo EX40", "Volvo EX90",
  // Lexus
  "Lexus ES", "Lexus LS", "Lexus UX", "Lexus NX", "Lexus RX", "Lexus GX", "Lexus LM",
  // Toyota
  "Toyota Camry", "Toyota Corolla", "Toyota Prius", "Toyota RAV4",
  "Toyota Highlander", "Toyota Sienna", "Toyota Crown", "Toyota Alphard",
  // MINI
  "MINI Cooper", "MINI Clubman", "MINI Countryman", "MINI Aceman",
  // Porsche
  "Porsche 718", "Porsche 911", "Porsche Panamera",
  "Porsche Macan", "Porsche Cayenne", "Porsche Taycan",
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
