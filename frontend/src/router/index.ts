import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "@/stores/authStore";

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior() {
    return { top: 0 };
  },
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/pages/HomePage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/pages/auth/LoginPage.vue"),
      meta: { layout: "auth", guestOnly: true },
    },
    {
      path: "/signup",
      name: "signup",
      component: () => import("@/pages/auth/SignupPage.vue"),
      meta: { layout: "auth", guestOnly: true },
    },
    {
      path: "/forgot-password",
      name: "forgot-password",
      component: () => import("@/pages/auth/ForgotPasswordPage.vue"),
      meta: { layout: "auth", guestOnly: true },
    },
    {
      path: "/taxi",
      name: "taxi",
      component: () => import("@/pages/TaxiPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/delivery",
      name: "delivery",
      component: () => import("@/pages/DeliveryPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/jobs",
      name: "jobs",
      component: () => import("@/pages/jobs/JobsPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/jobs/:id",
      name: "job-detail",
      component: () => import("@/pages/jobs/JobDetailPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/services",
      name: "services",
      component: () => import("@/pages/services/ServicesPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/services/:id",
      name: "service-detail",
      component: () => import("@/pages/services/ServiceDetailPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/community",
      name: "community",
      component: () => import("@/pages/community/CommunityPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/community/new",
      name: "community-new",
      component: () => import("@/pages/community/CreatePostPage.vue"),
      meta: { layout: "public", requiresAuth: true },
    },
    {
      path: "/community/:id",
      name: "community-post",
      component: () => import("@/pages/community/PostDetailPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/marketplace",
      name: "marketplace",
      component: () => import("@/pages/marketplace/MarketplacePage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/marketplace/new",
      name: "marketplace-new",
      component: () => import("@/pages/marketplace/CreateListingPage.vue"),
      meta: { layout: "public", requiresAuth: true },
    },
    {
      path: "/marketplace/:id",
      name: "marketplace-listing",
      component: () => import("@/pages/marketplace/ListingDetailPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/housing",
      name: "housing",
      component: () => import("@/pages/housing/HousingPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/housing/new",
      name: "housing-new",
      component: () => import("@/pages/housing/CreateHousingPage.vue"),
      meta: { layout: "public", requiresAuth: true },
    },
    {
      path: "/housing/:id",
      name: "housing-listing",
      component: () => import("@/pages/housing/HousingDetailPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/auto",
      name: "auto",
      component: () => import("@/pages/auto/AutoPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/auto/new",
      name: "auto-new",
      component: () => import("@/pages/auto/CreateAutoListingPage.vue"),
      meta: { layout: "public", requiresAuth: true },
    },
    {
      path: "/auto/:id",
      name: "auto-listing",
      component: () => import("@/pages/auto/AutoDetailPage.vue"),
      meta: { layout: "public" },
    },
    {
      path: "/orders",
      name: "orders",
      component: () => import("@/pages/PlaceholderPage.vue"),
      props: { titleKey: "orders.title", subtitleKey: "orders.subtitle" },
      meta: { layout: "app", requiresAuth: true },
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("@/pages/ProfilePage.vue"),
      meta: { layout: "app", requiresAuth: true },
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("@/pages/NotFoundPage.vue"),
      meta: { layout: "public" },
    },
  ],
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();
  if (!auth.isInitialized) {
    await auth.fetchCurrentUser();
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login", query: { redirect: to.fullPath } };
  }

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: "home" };
  }

  return true;
});

export default router;
