import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/auth/LoginView.vue"),
    meta: { requiresGuest: true, layout: "empty" },
  },
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
    meta: { requiresAuth: true },
  },

  // 🔹 Departments Routes
  {
    path: "/departments",
    name: "departments",
    component: () => import("@/views/departments/DepartmentListView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/departments/new",
    name: "department-create",
    component: () => import("@/views/departments/DepartmentFormView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/departments/:id/edit",
    name: "department-edit",
    component: () => import("@/views/departments/DepartmentFormView.vue"),
    meta: { requiresAuth: true },
  },

  // 🔹 Sections Routes
  {
    path: "/sections",
    name: "sections",
    component: () => import("@/views/sections/SectionListView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/sections/new",
    name: "section-create",
    component: () => import("@/views/sections/SectionFormView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/sections/:id/edit",
    name: "section-edit",
    component: () => import("@/views/sections/SectionFormView.vue"),
    meta: { requiresAuth: true },
  },

  // 🔹 Staff Routes
  {
    path: "/staff",
    name: "staff",
    component: () => import("@/views/staff/StaffListView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/staff/new",
    name: "staff-create",
    component: () => import("@/views/staff/StaffFormView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/staff/:id/edit",
    name: "staff-edit",
    component: () => import("@/views/staff/StaffFormView.vue"),
    meta: { requiresAuth: true },
  },

  // 🔹 Search (Public)
  {
    path: "/search",
    name: "search",
    component: () => import("@/views/SearchView.vue"),
    meta: { requiresAuth: false, public: true, layout: "public" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "login" });
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: "home" });
  } else {
    next();
  }
});

export default router;
