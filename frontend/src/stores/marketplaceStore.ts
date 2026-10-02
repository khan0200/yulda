import { ref } from "vue";
import { defineStore } from "pinia";

import { marketplaceApi, type CreateListingPayload, type ListListingsParams } from "@/services/marketplaceApi";
import type { MarketplaceListing } from "@/types/marketplace";

export const useMarketplaceStore = defineStore("marketplace", () => {
  const listings = ref<MarketplaceListing[]>([]);
  const total = ref(0);
  const hasMore = ref(false);
  const isLoading = ref(false);
  const currentListing = ref<MarketplaceListing | null>(null);

  async function fetchListings(params: ListListingsParams = {}, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const page = await marketplaceApi.listListings(params);
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
      currentListing.value = await marketplaceApi.getListing(listingId);
    } finally {
      isLoading.value = false;
    }
  }

  async function createListing(payload: CreateListingPayload): Promise<MarketplaceListing> {
    const listing = await marketplaceApi.createListing(payload);
    listings.value = [listing, ...listings.value];
    return listing;
  }

  async function deleteListing(listingId: string): Promise<void> {
    await marketplaceApi.deleteListing(listingId);
    listings.value = listings.value.filter((listing) => listing.id !== listingId);
  }

  async function markSold(listingId: string): Promise<void> {
    const updated = await marketplaceApi.markSold(listingId);
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
