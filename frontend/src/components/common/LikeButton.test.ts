import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { favoriteApi } from "@/services/favoriteApi";
import { useAuthStore } from "@/stores/authStore";

import LikeButton from "./LikeButton.vue";

vi.mock("@/services/favoriteApi", () => ({
  favoriteApi: {
    toggle: vi.fn(),
  },
}));

function flushPromises() {
  return new Promise((resolve) => setTimeout(resolve, 0));
}

describe("LikeButton", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("renders the initial like count and unliked state", () => {
    const wrapper = mount(LikeButton, {
      props: { targetType: "MARKETPLACE", targetId: "l1", liked: false, likeCount: 5 },
    });
    expect(wrapper.text()).toContain("5");
  });

  it("optimistically increments and calls the API when an authenticated user likes", async () => {
    const auth = useAuthStore();
    auth.setUser({
      id: "u1",
      email: "a@example.com",
      phone: null,
      name: "A",
      avatar: null,
      roles: ["CUSTOMER"],
      verification_status: "UNVERIFIED",
      location: null,
      is_banned: false,
      created_at: "",
      updated_at: "",
    });
    vi.mocked(favoriteApi.toggle).mockResolvedValueOnce({ is_favorited: true, like_count: 6 });

    const wrapper = mount(LikeButton, {
      props: { targetType: "MARKETPLACE", targetId: "l1", liked: false, likeCount: 5 },
    });

    await wrapper.find("button").trigger("click");
    // Optimistic update happens synchronously before the API call resolves.
    expect(wrapper.text()).toContain("6");

    await flushPromises();
    expect(favoriteApi.toggle).toHaveBeenCalledWith("MARKETPLACE", "l1");
    expect(wrapper.emitted("change")).toEqual([[true, 6]]);
  });

  it("reverts the optimistic update when the API call fails", async () => {
    const auth = useAuthStore();
    auth.setUser({
      id: "u1",
      email: "a@example.com",
      phone: null,
      name: "A",
      avatar: null,
      roles: ["CUSTOMER"],
      verification_status: "UNVERIFIED",
      location: null,
      is_banned: false,
      created_at: "",
      updated_at: "",
    });
    vi.mocked(favoriteApi.toggle).mockRejectedValueOnce(new Error("network error"));

    const wrapper = mount(LikeButton, {
      props: { targetType: "MARKETPLACE", targetId: "l1", liked: false, likeCount: 5 },
    });

    await wrapper.find("button").trigger("click");
    await flushPromises();

    expect(wrapper.text()).toContain("5");
    expect(wrapper.emitted("change")).toBeUndefined();
  });

  it("does not call the API for an unauthenticated user", async () => {
    const wrapper = mount(LikeButton, {
      props: { targetType: "MARKETPLACE", targetId: "l1", liked: false, likeCount: 5 },
      attachTo: undefined,
    });

    await wrapper.find("button").trigger("click");
    await flushPromises();

    expect(favoriteApi.toggle).not.toHaveBeenCalled();
  });

  it("does not trigger parent click handlers (stops propagation)", async () => {
    const parentClick = vi.fn();
    const wrapper = mount(
      {
        components: { LikeButton },
        template: `<div @click="onParentClick"><LikeButton target-type="MARKETPLACE" target-id="l1" :like-count="5" /></div>`,
        methods: { onParentClick: parentClick },
      },
    );

    await wrapper.find("button").trigger("click");

    expect(parentClick).not.toHaveBeenCalled();
  });
});
