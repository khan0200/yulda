import { ref } from "vue";
import { defineStore } from "pinia";

import { communityApi, type CreateCommentPayload, type CreatePostPayload, type ListPostsParams } from "@/services/communityApi";
import type { CommunityComment, CommunityPost } from "@/types/community";

export const useCommunityStore = defineStore("community", () => {
  const posts = ref<CommunityPost[]>([]);
  const total = ref(0);
  const hasMore = ref(false);
  const isLoading = ref(false);

  const currentPost = ref<CommunityPost | null>(null);
  const comments = ref<CommunityComment[]>([]);

  async function fetchPosts(params: ListPostsParams = {}, append = false): Promise<void> {
    isLoading.value = true;
    try {
      const page = await communityApi.listPosts(params);
      posts.value = append ? [...posts.value, ...page.items] : page.items;
      total.value = page.total;
      hasMore.value = page.has_more;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchPost(postId: string): Promise<void> {
    isLoading.value = true;
    try {
      currentPost.value = await communityApi.getPost(postId);
      const commentsPage = await communityApi.listComments(postId);
      comments.value = commentsPage.items;
    } finally {
      isLoading.value = false;
    }
  }

  async function createPost(payload: CreatePostPayload): Promise<CommunityPost> {
    const post = await communityApi.createPost(payload);
    posts.value = [post, ...posts.value];
    return post;
  }

  async function deletePost(postId: string): Promise<void> {
    await communityApi.deletePost(postId);
    posts.value = posts.value.filter((post) => post.id !== postId);
  }

  async function addComment(postId: string, payload: CreateCommentPayload): Promise<void> {
    const comment = await communityApi.addComment(postId, payload);
    comments.value = [...comments.value, comment];
    if (currentPost.value && currentPost.value.id === postId) {
      currentPost.value = { ...currentPost.value, comment_count: currentPost.value.comment_count + 1 };
    }
  }

  return {
    posts,
    total,
    hasMore,
    isLoading,
    currentPost,
    comments,
    fetchPosts,
    fetchPost,
    createPost,
    deletePost,
    addComment,
  };
});
