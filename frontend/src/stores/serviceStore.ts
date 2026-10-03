import { ref } from "vue";
import { defineStore } from "pinia";

import { serviceApi, type CreateServicePostPayload, type ListServicesParams } from "@/services/serviceApi";
import type { ServicePost } from "@/types/service";

export const useServiceStore = defineStore("service", () => {
  const posts = ref<ServicePost[]>([]);
  const total = ref(0);
  const hasMore = ref(false);
  const isLoading = ref(false);
  const currentPost = ref<ServicePost | null>(null);

  async function fetchPosts(params: ListServicesParams = {}, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const page = await serviceApi.listPosts(params);
      posts.value = append ? [...posts.value, ...page.items] : page.items;
      total.value = page.total;
      hasMore.value = page.has_more;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchPost(serviceId: string): Promise<void> {
    isLoading.value = true;
    try {
      currentPost.value = await serviceApi.getPost(serviceId);
    } finally {
      isLoading.value = false;
    }
  }

  async function createPost(payload: CreateServicePostPayload): Promise<ServicePost> {
    const post = await serviceApi.createPost(payload);
    posts.value = [post, ...posts.value];
    return post;
  }

  async function deletePost(serviceId: string): Promise<void> {
    await serviceApi.deletePost(serviceId);
    posts.value = posts.value.filter((post) => post.id !== serviceId);
  }

  async function markUnavailable(serviceId: string): Promise<void> {
    const updated = await serviceApi.markUnavailable(serviceId);
    if (currentPost.value && currentPost.value.id === serviceId) {
      currentPost.value = updated;
    }
  }

  return {
    posts,
    total,
    hasMore,
    isLoading,
    currentPost,
    fetchPosts,
    fetchPost,
    createPost,
    deletePost,
    markUnavailable,
  };
});
