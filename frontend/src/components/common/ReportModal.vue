<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { Flag } from "lucide-vue-next";

import { reportApi } from "@/services/reportApi";
import { useToastStore } from "@/stores/toastStore";
import type { ReportReason, ReportTargetType } from "@/types/report";

const props = defineProps<{
  show: boolean;
  targetType: ReportTargetType;
  targetId: string;
}>();

const emit = defineEmits<{ "update:show": [boolean] }>();

const { t } = useI18n();
const toast = useToastStore();

const reasons: ReportReason[] = ["SPAM", "SCAM", "INAPPROPRIATE", "HARASSMENT", "FAKE_LISTING", "OTHER"];
const selectedReason = ref<ReportReason>("SPAM");
const details = ref("");
const isSubmitting = ref(false);

function close() {
  emit("update:show", false);
  selectedReason.value = "SPAM";
  details.value = "";
}

async function submit() {
  isSubmitting.value = true;
  try {
    await reportApi.create({
      target_type: props.targetType,
      target_id: props.targetId,
      reason: selectedReason.value,
      details: details.value.trim() || null,
    });
    toast.success(t("report.submitted"));
    close();
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-150 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-100 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="show"
        class="fixed inset-0 z-[998] flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm"
        @click.self="close"
      >
        <div class="w-full max-w-sm rounded-2xl bg-white p-6 shadow-card-hover">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-50 text-red-500">
              <Flag class="h-5 w-5" />
            </div>
            <h3 class="text-sm font-bold text-yulda-black">{{ t("report.title") }}</h3>
          </div>

          <div class="mt-4 flex flex-col gap-1.5">
            <label class="text-xs font-semibold uppercase text-yulda-gray-400">{{ t("report.reason") }}</label>
            <select
              v-model="selectedReason"
              class="rounded-xl border border-yulda-gray-200 bg-white px-3 py-2.5 text-sm focus:border-yulda-yellow focus:outline-none focus:ring-2 focus:ring-yulda-yellow"
            >
              <option v-for="reason in reasons" :key="reason" :value="reason">{{ t(`report.reasons.${reason}`) }}</option>
            </select>
          </div>

          <div class="mt-3 flex flex-col gap-1.5">
            <label class="text-xs font-semibold uppercase text-yulda-gray-400">{{ t("report.detailsOptional") }}</label>
            <textarea
              v-model="details"
              rows="3"
              maxlength="1000"
              class="resize-none rounded-xl border border-yulda-gray-200 bg-white px-3 py-2.5 text-sm focus:border-yulda-yellow focus:outline-none focus:ring-2 focus:ring-yulda-yellow"
              :placeholder="t('report.detailsPlaceholder')"
            />
          </div>

          <div class="mt-5 flex justify-end gap-2">
            <button type="button" class="btn-outline !px-4 !py-2 text-sm" @click="close">
              {{ t("common.cancel") }}
            </button>
            <button
              type="button"
              class="rounded-xl bg-red-500 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-600 disabled:opacity-50"
              :disabled="isSubmitting"
              @click="submit"
            >
              {{ t("report.submit") }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
