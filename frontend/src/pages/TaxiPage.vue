<script setup lang="ts">
import { MapPin, Navigation } from "lucide-vue-next";

import BaseButton from "@/components/common/BaseButton.vue";
</script>

<template>
  <div class="flex h-[calc(100vh-4rem)] flex-col lg:flex-row">
    <div class="w-full border-r border-yulda-gray-100 bg-white p-6 lg:w-[380px] lg:p-8">
      <h1 class="text-xl font-bold text-yulda-black">Book a ride</h1>

      <div class="mt-6 flex flex-col gap-3">
        <div class="flex items-center gap-3 rounded-xl border border-yulda-gray-200 px-4 py-3">
          <MapPin class="h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
          <input placeholder="Pickup location" class="w-full border-none p-0 text-sm focus:outline-none focus:ring-0" />
        </div>
        <div class="flex items-center gap-3 rounded-xl border border-yulda-gray-200 px-4 py-3">
          <Navigation class="h-4 w-4 flex-shrink-0 text-yulda-gray-400" />
          <input placeholder="Destination" class="w-full border-none p-0 text-sm focus:outline-none focus:ring-0" />
        </div>
      </div>

      <div class="mt-8 card p-10 text-center text-sm text-yulda-gray-500">
        Ride type, pricing and live dispatch are coming soon.
      </div>

      <BaseButton full-width class="mt-6" disabled>Book ride</BaseButton>
    </div>

    <div class="relative flex-1 bg-yulda-gray-100">
      <div class="flex h-full items-center justify-center text-sm text-yulda-gray-400">
        Map integration coming soon
      </div>
    </div>
  </div>
</template>
