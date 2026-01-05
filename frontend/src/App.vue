<template>
  <div id="app" :class="{ 'rtl': true }">
    <!-- حالت عمومی: صفحه Search با یا بدون Navbar -->
    <template v-if="currentLayout === 'public'">
      <Navbar v-if="authStore.isAuthenticated" />
      <div :class="authStore.isAuthenticated ? 'app-container' : ''">
        <Sidebar v-if="authStore.isAuthenticated" />
        <main :class="authStore.isAuthenticated ? 'main-content' : 'public-content'">
          <RouterView />
        </main>
      </div>
    </template>

    <!-- حالت خالی: صفحات مثل Login -->
    <template v-else-if="currentLayout === 'empty'">
      <RouterView />
    </template>

    <!-- حالت پیش‌فرض: صفحات داخلی با Navbar و Sidebar -->
    <template v-else>
      <Navbar />
      <div class="app-container">
        <Sidebar />
        <main class="main-content">
          <RouterView />
        </main>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'

const route = useRoute()
const authStore = useAuthStore()

const currentLayout = computed(() => route.meta.layout || 'default')

onMounted(() => {
  authStore.initAuth()
})
</script>

<style>
/* همان استایل‌های قبلی... */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #4CAF50;
  --secondary-color: #2196F3;
  --danger-color: #f44336;
  --warning-color: #ff9800;
  --dark-color: #333;
  --light-color: #f5f5f5;
  --border-color: #ddd;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  --sidebar-width: 250px;
  --navbar-height: 60px;
}

body {
  font-family: 'Vazir', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--light-color);
  color: var(--dark-color);
  line-height: 1.6;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.rtl {
  direction: rtl;
  text-align: right;
}

.app-container {
  display: flex;
  flex: 1;
  padding-top: var(--navbar-height);
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-right: var(--sidebar-width);
  transition: margin-right 0.3s ease;
}

/* محتوای عمومی بدون Sidebar */
.public-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-right: 0;
  }
}

/* بقیه استایل‌ها... */
</style>
