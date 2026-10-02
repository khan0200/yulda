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
      component: () => import("@/pages/PlaceholderPage.vue"),
      props: { title: "Delivery & Cargo", subtitle: "Send anything, anywhere." },
      meta: { layout: "public" },
    },
    {
      path: "/jobs",
      name: "jobs",
      component: () => import("@/pages/PlaceholderPage.vue"),
      props: { title: "Jobs", subtitle: "Find work near you." },
      meta: { layout: "public" },
    },
    {
      path: "/services",
      name: "services",
      component: () => import("@/pages/PlaceholderPage.vue"),
      props: { title: "Services", subtitle: "Find trusted local professionals." },
      meta: { layout: "public" },
    },
    {
      path: "/orders",
      name: "orders",
      component: () => import("@/pages/PlaceholderPage.vue"),
      props: { title: "Orders", subtitle: "Track your rides, deliveries and service requests." },
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
