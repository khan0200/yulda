import { ref } from "vue";
import { defineStore } from "pinia";

import { housingApi, type CreateHousingPayload, type ListHousingParams } from "@/services/housingApi";
import type { HousingListing } from "@/types/housing";

export const useHousingStore = defineStore("housing", () => {
  const listings = ref<HousingListing[]>([]);
  const total = ref(0);
  const hasMore = ref(false);
  const isLoading = ref(false);
  const currentListing = ref<HousingListing | null>(null);

  async function fetchListings(params: ListHousingParams = {}, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const page = await housingApi.listListings(params);
      listings.value = append ? [...listings.value, ...page.items] : page.items;
      total.value = page.total;
      hasMore.value = page.has_more;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchListing(listingId: string): Promise<void> {
    isLoading.value = true;
    try {
      currentListing.value = await housingApi.getListing(listingId);
    } finally {
      isLoading.value = false;
    }
  }

  async function createListing(payload: CreateHousingPayload): Promise<HousingListing> {
    const listing = await housingApi.createListing(payload);
    listings.value = [listing, ...listings.value];
    return listing;
  }

  async function deleteListing(listingId: string): Promise<void> {
    await housingApi.deleteListing(listingId);
    listings.value = listings.value.filter((listing) => listing.id !== listingId);
  }

  async function markRented(listingId: string): Promise<void> {
    const updated = await housingApi.markRented(listingId);
    if (currentListing.value && currentListing.value.id === listingId) {
      currentListing.value = updated;
    }
  }

  return {
    listings,
    total,
    hasMore,
    isLoading,
    currentListing,
    fetchListings,
    fetchListing,
    createListing,
    deleteListing,
    markRented,
  };
});
