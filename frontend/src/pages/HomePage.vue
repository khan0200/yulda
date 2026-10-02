<script setup lang="ts">
import { Car, Package, ShoppingBag, Wrench } from "lucide-vue-next";

import CategoryCard from "@/components/common/CategoryCard.vue";

const categories = [
  {
    icon: Car,
    title: "Taxi",
    description: "Get where you need to go.",
    cta: "Book a ride",
    to: "/taxi",
    accent: true,
  },
  {
    icon: Package,
    title: "Delivery & Cargo",
    description: "Send anything, anywhere.",
    cta: "Send a package",
    to: "/delivery",
  },
  {
    icon: ShoppingBag,
    title: "Jobs",
    description: "Find work near you.",
    cta: "Find jobs",
    to: "/jobs",
  },
  {
    icon: Wrench,
    title: "Services",
    description: "Find trusted local professionals.",
    cta: "Find a service",
    to: "/services",
  },
];
</script>

<template>
  <div>
    <section class="relative overflow-hidden">
      <div class="mx-auto max-w-7xl px-6 pb-20 pt-20 sm:pt-28">
        <div class="max-w-3xl">
          <h1 class="text-5xl font-extrabold leading-[1.1] tracking-tight text-yulda-black sm:text-6xl">
            Everything you need, <span class="relative inline-block">nearby.
              <svg class="absolute -bottom-2 left-0 w-full" height="10" viewBox="0 0 220 10" fill="none" preserveAspectRatio="none">
                <path d="M2 8C40 2 160 2 218 8" stroke="#FFD600" stroke-width="5" stroke-linecap="round"/>
              </svg>
            </span>
          </h1>
          <p class="mt-6 max-w-xl text-lg text-yulda-gray-600">
            Ride. Deliver. Work. Get things done.
          </p>
          <div class="mt-10 flex flex-wrap gap-3">
            <RouterLink to="/taxi" class="btn-primary">Book a ride</RouterLink>
            <RouterLink to="/signup" class="btn-outline">Get started</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 pb-24">
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <CategoryCard v-for="category in categories" :key="category.to" v-bind="category" />
      </div>
    </section>
  </div>
</template>
