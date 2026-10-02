import { ref } from "vue";
import { defineStore } from "pinia";

import { cargoApi, type CreateCargoPostPayload, type SearchCargoParams } from "@/services/cargoApi";
import type { CargoPost } from "@/types/cargo";

export const useCargoStore = defineStore("cargo", () => {
  const items = ref<CargoPost[]>([]);
  const suggestedOtherDates = ref<CargoPost[]>([]);
  const total = ref(0);
  const hasMore = ref(false);
  const isLoading = ref(false);

  const myPosts = ref<CargoPost[]>([]);

  async function search(params: SearchCargoParams = {}, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const result = await cargoApi.search(params);
      items.value = append ? [...items.value, ...result.items] : result.items;
      suggestedOtherDates.value = result.suggested_other_dates;
      total.value = result.total;
      hasMore.value = result.has_more;
    } finally {
      isLoading.value = false;
    }
  }

  async function createPost(payload: CreateCargoPostPayload): Promise<CargoPost> {
    const post = await cargoApi.createPost(payload);
    myPosts.value = [post, ...myPosts.value];
    return post;
  }

  function upsertMyPost(post: CargoPost): void {
    const index = myPosts.value.findIndex((p) => p.id === post.id);
    if (index === -1) {
      myPosts.value = [post, ...myPosts.value];
    } else {
      myPosts.value = [...myPosts.value.slice(0, index), post, ...myPosts.value.slice(index + 1)];
    }
  }

  async function deactivate(postId: string): Promise<void> {
    const updated = await cargoApi.deactivate(postId);
    upsertMyPost(updated);
  }

  async function repost(postId: string, departureAt: string): Promise<void> {
    const updated = await cargoApi.repost(postId, departureAt);
    upsertMyPost(updated);
  }

  async function deletePost(postId: string): Promise<void> {
    await cargoApi.deletePost(postId);
    myPosts.value = myPosts.value.filter((p) => p.id !== postId);
  }

  return {
    items,
    suggestedOtherDates,
    total,
    hasMore,
    isLoading,
    myPosts,
    search,
    createPost,
    deactivate,
    repost,
    deletePost,
  };
});
