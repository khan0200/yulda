import { ref } from "vue";
import { defineStore } from "pinia";

import { autoApi, type CreateAutoListingPayload, type ListAutoParams } from "@/services/autoApi";
import type { AutoListing } from "@/types/auto";

export const useAutoStore = defineStore("auto", () => {
  const listings = ref<AutoListing[]>([]);
  const total = ref(0);
  const hasMore = ref(false);
  const isLoading = ref(false);
  const currentListing = ref<AutoListing | null>(null);

  async function fetchListings(params: ListAutoParams = {}, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const page = await autoApi.listListings(params);
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
      currentListing.value = await autoApi.getListing(listingId);
    } finally {
      isLoading.value = false;
    }
  }

  async function createListing(payload: CreateAutoListingPayload): Promise<AutoListing> {
    const listing = await autoApi.createListing(payload);
    listings.value = [listing, ...listings.value];
    return listing;
  }

  async function deleteListing(listingId: string): Promise<void> {
    await autoApi.deleteListing(listingId);
    listings.value = listings.value.filter((listing) => listing.id !== listingId);
  }

  async function markSold(listingId: string): Promise<void> {
    const updated = await autoApi.markSold(listingId);
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
    markSold,
  };
});
