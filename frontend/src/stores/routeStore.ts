import { ref } from "vue";
import { defineStore } from "pinia";

import { routeApi, type CreateRoutePostPayload, type SearchRoutesParams } from "@/services/routeApi";
import type { RoutePost } from "@/types/route";

export const useRouteStore = defineStore("route", () => {
  const items = ref<RoutePost[]>([]);
  const suggestedOtherDates = ref<RoutePost[]>([]);
  const total = ref(0);
  const hasMore = ref(false);
  const isLoading = ref(false);

  const myPosts = ref<RoutePost[]>([]);

  async function search(params: SearchRoutesParams = {}, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const result = await routeApi.search(params);
      items.value = append ? [...items.value, ...result.items] : result.items;
      suggestedOtherDates.value = result.suggested_other_dates;
      total.value = result.total;
      hasMore.value = result.has_more;
    } finally {
      isLoading.value = false;
    }
  }

  async function createPost(payload: CreateRoutePostPayload): Promise<RoutePost> {
    const post = await routeApi.createPost(payload);
    myPosts.value = [post, ...myPosts.value];
    return post;
  }

  function upsertMyPost(post: RoutePost): void {
    const index = myPosts.value.findIndex((p) => p.id === post.id);
    if (index === -1) {
      myPosts.value = [post, ...myPosts.value];
    } else {
      myPosts.value = [...myPosts.value.slice(0, index), post, ...myPosts.value.slice(index + 1)];
    }
  }

  async function deactivate(postId: string): Promise<void> {
    const updated = await routeApi.deactivate(postId);
    upsertMyPost(updated);
  }

  async function repost(postId: string, departureAt: string): Promise<void> {
    const updated = await routeApi.repost(postId, departureAt);
    upsertMyPost(updated);
  }

  async function deletePost(postId: string): Promise<void> {
    await routeApi.deletePost(postId);
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
