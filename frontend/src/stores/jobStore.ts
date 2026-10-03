import { ref } from "vue";
import { defineStore } from "pinia";

import { jobApi, type CreateJobPostPayload, type ListJobsParams } from "@/services/jobApi";
import type { JobPost } from "@/types/job";

export const useJobStore = defineStore("job", () => {
  const posts = ref<JobPost[]>([]);
  const total = ref(0);
  const hasMore = ref(false);
  const isLoading = ref(false);
  const currentPost = ref<JobPost | null>(null);

  async function fetchPosts(params: ListJobsParams = {}, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const page = await jobApi.listPosts(params);
      posts.value = append ? [...posts.value, ...page.items] : page.items;
      total.value = page.total;
      hasMore.value = page.has_more;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchPost(jobId: string): Promise<void> {
    isLoading.value = true;
    try {
      currentPost.value = await jobApi.getPost(jobId);
    } finally {
      isLoading.value = false;
    }
  }

  async function createPost(payload: CreateJobPostPayload): Promise<JobPost> {
    const post = await jobApi.createPost(payload);
    posts.value = [post, ...posts.value];
    return post;
  }

  async function deletePost(jobId: string): Promise<void> {
    await jobApi.deletePost(jobId);
    posts.value = posts.value.filter((post) => post.id !== jobId);
  }

  async function markClosed(jobId: string): Promise<void> {
    const updated = await jobApi.markClosed(jobId);
    if (currentPost.value && currentPost.value.id === jobId) {
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
    markClosed,
  };
});
