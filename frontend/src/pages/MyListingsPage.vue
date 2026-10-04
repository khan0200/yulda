<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { ImageOff, Pencil, RotateCcw, Trash2 } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import BaseTextarea from "@/components/common/BaseTextarea.vue";
import { autoApi } from "@/services/autoApi";
import { housingApi } from "@/services/housingApi";
import { jobApi } from "@/services/jobApi";
import { marketplaceApi } from "@/services/marketplaceApi";
import { serviceApi } from "@/services/serviceApi";
import { useConfirmStore } from "@/stores/confirmStore";
import { useToastStore } from "@/stores/toastStore";
import { formatKrw, formatPriceNote } from "@/utils/format";

const { t } = useI18n();
const confirmStore = useConfirmStore();
const toast = useToastStore();

type ModuleKey = "marketplace" | "housing" | "auto" | "jobs" | "services";

interface ManagedItem {
  id: string;
  title: string;
  subtitle: string;
  photo: string | null;
  status: string;
  created_at: string;
  raw: Record<string, unknown>;
}

interface EditField {
  key: string;
  labelKey: string;
  type: "text" | "textarea" | "number";
}

interface ModuleConfig {
  key: ModuleKey;
  labelKey: string;
  activeStatus: string;
  pausedStatus: string;
  editFields: EditField[];
  api: {
    listMine: () => Promise<{ items: Record<string, unknown>[] }>;
    repost: (id: string) => Promise<Record<string, unknown>>;
    update: (id: string, payload: Record<string, unknown>) => Promise<Record<string, unknown>>;
    delete: (id: string) => Promise<void>;
  };
  toItem: (raw: Record<string, unknown>) => ManagedItem;
}

const modules: ModuleConfig[] = [
  {
    key: "marketplace",
    labelKey: "nav.marketplace",
    activeStatus: "ACTIVE",
    pausedStatus: "PAUSED",
    editFields: [
      { key: "title", labelKey: "myListings.editTitle", type: "text" },
      { key: "description", labelKey: "myListings.editDescription", type: "textarea" },
      { key: "price", labelKey: "myListings.editPrice", type: "number" },
    ],
    api: {
      listMine: () => marketplaceApi.listMine(),
      repost: (id: string) => marketplaceApi.repost(id),
      update: (id: string, payload: Record<string, unknown>) => marketplaceApi.updateListing(id, payload),
      delete: (id: string) => marketplaceApi.deleteListing(id),
    } as unknown as ModuleConfig["api"],
    toItem: (raw) => ({
      id: raw.id as string,
      title: raw.title as string,
      subtitle: formatKrw(raw.price as number),
      photo: (raw.photos as string[])?.[0] ?? null,
      status: raw.status as string,
      created_at: raw.created_at as string,
      raw,
    }),
  },
  {
    key: "housing",
    labelKey: "nav.housing",
    activeStatus: "ACTIVE",
    pausedStatus: "PAUSED",
    editFields: [
      { key: "title", labelKey: "myListings.editTitle", type: "text" },
      { key: "description", labelKey: "myListings.editDescription", type: "textarea" },
      { key: "deposit", labelKey: "housing.deposit", type: "number" },
      { key: "monthly_rent", labelKey: "housing.monthlyRent", type: "number" },
    ],
    api: {
      listMine: () => housingApi.listMine(),
      repost: (id: string) => housingApi.repost(id),
      update: (id: string, payload: Record<string, unknown>) => housingApi.updateListing(id, payload),
      delete: (id: string) => housingApi.deleteListing(id),
    } as unknown as ModuleConfig["api"],
    toItem: (raw) => ({
      id: raw.id as string,
      title: raw.title as string,
      subtitle: `${formatKrw(raw.deposit as number)} / ${formatKrw(raw.monthly_rent as number)}`,
      photo: (raw.photos as string[])?.[0] ?? null,
      status: raw.status as string,
      created_at: raw.created_at as string,
      raw,
    }),
  },
  {
    key: "auto",
    labelKey: "nav.auto",
    activeStatus: "ACTIVE",
    pausedStatus: "UNAVAILABLE",
    editFields: [
      { key: "description", labelKey: "myListings.editDescription", type: "textarea" },
      { key: "price", labelKey: "myListings.editPrice", type: "number" },
    ],
    api: {
      listMine: () => autoApi.listMine(),
      repost: (id: string) => autoApi.repost(id),
      update: (id: string, payload: Record<string, unknown>) => autoApi.updateListing(id, payload),
      delete: (id: string) => autoApi.deleteListing(id),
    } as unknown as ModuleConfig["api"],
    toItem: (raw) => ({
      id: raw.id as string,
      title: `${raw.make} ${raw.model} (${raw.year})`,
      subtitle: formatKrw(raw.price as number),
      photo: (raw.photos as string[])?.[0] ?? null,
      status: raw.status as string,
      created_at: raw.created_at as string,
      raw,
    }),
  },
  {
    key: "jobs",
    labelKey: "nav.jobs",
    activeStatus: "ACTIVE",
    pausedStatus: "CLOSED",
    editFields: [
      { key: "title", labelKey: "myListings.editTitle", type: "text" },
      { key: "description", labelKey: "myListings.editDescription", type: "textarea" },
      { key: "pay_amount", labelKey: "jobs.payAmount", type: "number" },
    ],
    api: {
      listMine: () => jobApi.listMine(),
      repost: (id: string) => jobApi.repost(id),
      update: (id: string, payload: Record<string, unknown>) => jobApi.updatePost(id, payload),
      delete: (id: string) => jobApi.deletePost(id),
    } as unknown as ModuleConfig["api"],
    toItem: (raw) => ({
      id: raw.id as string,
      title: raw.title as string,
      subtitle: raw.pay_amount ? formatKrw(raw.pay_amount as number) : "",
      photo: (raw.photos as string[])?.[0] ?? null,
      status: raw.status as string,
      created_at: raw.created_at as string,
      raw,
    }),
  },
  {
    key: "services",
    labelKey: "nav.services",
    activeStatus: "ACTIVE",
    pausedStatus: "UNAVAILABLE",
    editFields: [
      { key: "title", labelKey: "myListings.editTitle", type: "text" },
      { key: "description", labelKey: "myListings.editDescription", type: "textarea" },
      { key: "price_note", labelKey: "services.priceNote", type: "text" },
    ],
    api: {
      listMine: () => serviceApi.listMine(),
      repost: (id: string) => serviceApi.repost(id),
      update: (id: string, payload: Record<string, unknown>) => serviceApi.updatePost(id, payload),
      delete: (id: string) => serviceApi.deletePost(id),
    } as unknown as ModuleConfig["api"],
    toItem: (raw) => ({
      id: raw.id as string,
      title: raw.title as string,
      subtitle: raw.price_note ? formatPriceNote(raw.price_note as string) : "",
      photo: (raw.photos as string[])?.[0] ?? null,
      status: raw.status as string,
      created_at: raw.created_at as string,
      raw,
    }),
  },
];

const activeModuleKey = ref<ModuleKey>("marketplace");
const activeModule = computed(() => modules.find((m) => m.key === activeModuleKey.value)!);

const itemsByModule = reactive<Record<ModuleKey, ManagedItem[]>>({
  marketplace: [],
  housing: [],
  auto: [],
  jobs: [],
  services: [],
});
const loadedModules = reactive<Record<ModuleKey, boolean>>({
  marketplace: false,
  housing: false,
  auto: false,
  jobs: false,
  services: false,
});
const isLoading = ref(false);

async function loadModule(key: ModuleKey) {
  const config = modules.find((m) => m.key === key)!;
  isLoading.value = true;
  try {
    const result = await config.api.listMine();
    itemsByModule[key] = result.items.map((raw) => config.toItem(raw));
    loadedModules[key] = true;
  } finally {
    isLoading.value = false;
  }
}

async function selectModule(key: ModuleKey) {
  activeModuleKey.value = key;
  if (!loadedModules[key]) await loadModule(key);
}

const editingId = ref<string | null>(null);
const editForm = reactive<Record<string, string>>({});
const isSaving = ref(false);

function startEdit(item: ManagedItem) {
  editingId.value = item.id;
  for (const key of Object.keys(editForm)) delete editForm[key];
  for (const field of activeModule.value.editFields) {
    const value = item.raw[field.key];
    editForm[field.key] = value === null || value === undefined ? "" : String(value);
  }
}

function cancelEdit() {
  editingId.value = null;
}

async function saveEdit(item: ManagedItem) {
  isSaving.value = true;
  try {
    const payload: Record<string, unknown> = {};
    for (const field of activeModule.value.editFields) {
      const raw = editForm[field.key];
      payload[field.key] = field.type === "number" ? Number(raw) || 0 : raw;
    }
    const updated = await activeModule.value.api.update(item.id, payload);
    const index = itemsByModule[activeModuleKey.value].findIndex((i) => i.id === item.id);
    if (index !== -1) itemsByModule[activeModuleKey.value][index] = activeModule.value.toItem(updated);
    editingId.value = null;
    toast.success(t("myListings.updateSuccess"));
  } finally {
    isSaving.value = false;
  }
}

async function toggleStatus(item: ManagedItem) {
  const config = activeModule.value;
  const nextStatus = item.status === config.activeStatus ? config.pausedStatus : config.activeStatus;
  try {
    const updated = await config.api.update(item.id, { status: nextStatus });
    const index = itemsByModule[activeModuleKey.value].findIndex((i) => i.id === item.id);
    if (index !== -1) itemsByModule[activeModuleKey.value][index] = config.toItem(updated);
    toast.success(t("myListings.updateSuccess"));
  } catch {
    // Global http error toast already informed the user; nothing further to do.
  }
}

async function repostItem(item: ManagedItem) {
  const ok = await confirmStore.ask({ message: t("myListings.confirmRepost") });
  if (!ok) return;
  try {
    const updated = await activeModule.value.api.repost(item.id);
    const index = itemsByModule[activeModuleKey.value].findIndex((i) => i.id === item.id);
    if (index !== -1) itemsByModule[activeModuleKey.value][index] = activeModule.value.toItem(updated);
    toast.success(t("myListings.repostSuccess"));
  } catch {
    // Global http error toast already informed the user; nothing further to do.
  }
}

async function deleteItem(item: ManagedItem) {
  const ok = await confirmStore.ask({ message: t("myListings.confirmDelete"), danger: true });
  if (!ok) return;
  try {
    await activeModule.value.api.delete(item.id);
    itemsByModule[activeModuleKey.value] = itemsByModule[activeModuleKey.value].filter((i) => i.id !== item.id);
    toast.success(t("myListings.deleteSuccess"));
  } catch {
    // Global http error toast already informed the user; nothing further to do.
  }
}

onMounted(() => loadModule(activeModuleKey.value));
</script>

<template>
  <div class="mx-auto max-w-4xl px-6 py-10">
    <h1 class="text-xl font-bold text-yulda-black">{{ t("myListings.title") }}</h1>
    <p class="text-sm text-yulda-gray-500">{{ t("myListings.subtitle") }}</p>

    <div class="mt-6 flex flex-wrap gap-2 border-b border-yulda-gray-100 pb-1">
      <button
        v-for="mod in modules"
        :key="mod.key"
        type="button"
        class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
        :class="activeModuleKey === mod.key ? 'bg-yulda-black text-white' : 'bg-yulda-gray-100 text-yulda-gray-600 hover:bg-yulda-gray-200'"
        @click="selectModule(mod.key)"
      >
        {{ t(mod.labelKey) }}
      </button>
    </div>

    <div v-if="isLoading" class="mt-6 flex flex-col gap-3">
      <div v-for="i in 3" :key="i" class="card h-24 animate-pulse bg-yulda-gray-100" />
    </div>

    <div v-else-if="itemsByModule[activeModuleKey].length === 0" class="card mt-6 p-10 text-center text-sm text-yulda-gray-500">
      {{ t("myListings.empty") }}
    </div>

    <div v-else class="mt-6 flex flex-col gap-3">
      <div v-for="item in itemsByModule[activeModuleKey]" :key="item.id" class="card p-4">
        <div v-if="editingId !== item.id" class="flex items-center gap-3">
          <div class="flex h-14 w-14 flex-shrink-0 items-center justify-center overflow-hidden rounded-xl bg-yulda-gray-100">
            <img v-if="item.photo" :src="item.photo" :alt="item.title" class="h-full w-full object-cover" />
            <ImageOff v-else class="h-5 w-5 text-yulda-gray-300" />
          </div>
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2">
              <h3 class="truncate text-sm font-bold text-yulda-black">{{ item.title }}</h3>
              <span
                class="flex-shrink-0 rounded-full px-2 py-0.5 text-[11px] font-semibold"
                :class="item.status === activeModule.activeStatus ? 'bg-emerald-50 text-emerald-700' : 'bg-yulda-gray-100 text-yulda-gray-600'"
              >
                {{ t(`${activeModuleKey}.status.${item.status}`) }}
              </span>
            </div>
            <p v-if="item.subtitle" class="truncate text-xs font-semibold text-yulda-gray-600">{{ item.subtitle }}</p>
          </div>
          <div class="flex flex-shrink-0 items-center gap-1">
            <button
              type="button"
              class="rounded-lg px-2.5 py-1.5 text-xs font-semibold text-yulda-gray-600 hover:bg-yulda-gray-100"
              @click="toggleStatus(item)"
            >
              {{ item.status === activeModule.activeStatus ? t("myListings.deactivate") : t("myListings.activate") }}
            </button>
            <button
              type="button"
              class="flex items-center gap-1 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-yulda-gray-600 hover:bg-yulda-gray-100"
              :title="t('myListings.repost')"
              @click="repostItem(item)"
            >
              <RotateCcw class="h-3.5 w-3.5" />
            </button>
            <button
              type="button"
              class="flex items-center gap-1 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-yulda-gray-600 hover:bg-yulda-gray-100"
              :title="t('myListings.edit')"
              @click="startEdit(item)"
            >
              <Pencil class="h-3.5 w-3.5" />
            </button>
            <button
              type="button"
              class="flex items-center gap-1 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-red-500 hover:bg-red-50"
              :title="t('myListings.delete')"
              @click="deleteItem(item)"
            >
              <Trash2 class="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        <form v-else class="flex flex-col gap-3" @submit.prevent="saveEdit(item)">
          <template v-for="field in activeModule.editFields" :key="field.key">
            <BaseTextarea
              v-if="field.type === 'textarea'"
              v-model="editForm[field.key]"
              :label="t(field.labelKey)"
              :rows="3"
            />
            <BaseInput
              v-else
              v-model="editForm[field.key]"
              :type="field.type === 'number' ? 'number' : 'text'"
              :label="t(field.labelKey)"
            />
          </template>
          <div class="flex gap-2">
            <BaseButton type="submit" :loading="isSaving">{{ t("myListings.save") }}</BaseButton>
            <button type="button" class="btn-outline" @click="cancelEdit">{{ t("myListings.cancel") }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
