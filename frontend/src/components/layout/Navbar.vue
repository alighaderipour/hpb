
<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <h2>🏥 دفترچه تلفن بیمارستان</h2>
      </div>

      <div class="navbar-menu">
        <!-- دکمه جستجو فقط برای کاربران لاگین شده -->
        <button 
          v-if="authStore.isAuthenticated" 
          @click="toggleSearch" 
          class="nav-item"
        >
          <span class="icon">🔍</span>
          <span>جستجو</span>
        </button>

        <!-- منوی کاربر فقط برای کاربران لاگین شده -->
        <div 
          v-if="authStore.isAuthenticated" 
          class="nav-item user-menu" 
          @click="toggleDropdown"
        >
          <span class="icon">👤</span>
          <span>{{ authStore.currentUser?.username || 'کاربر' }}</span>
          <div v-if="showDropdown" class="dropdown">
            <button @click.stop="handleLogout" class="dropdown-item">
              <span class="icon">🚪</span>
              خروج از سیستم
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()
const showDropdown = ref(false)

function toggleSearch() {
  router.push({ name: 'search' })
}

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

function handleLogout() {
  if (confirm('آیا مطمئن هستید که می‌خواهید خارج شوید؟')) {
    authStore.logout()
    router.push({ name: 'login' })
  }
  showDropdown.value = false
}
</script>

<style scoped>
/* همان استایل قبلی Navbar... */
</style>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  height: var(--navbar-height);
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.navbar-brand h2 {
  color: var(--primary-color);
  font-size: 22px;
  font-weight: 700;
  margin: 0;
}

.navbar-menu {
  display: flex;
  gap: 15px;
  align-items: center;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
  position: relative;
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.nav-item:hover {
  background-color: #f0f4ff;
  color: var(--primary-color);
}

.icon {
  font-size: 18px;
}

.user-menu {
  position: relative;
}

.dropdown {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  min-width: 180px;
  overflow: hidden;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 14px 18px;
  border: none;
  background: transparent;
  text-align: right;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.dropdown-item:hover {
  background-color: #f0f4ff;
  color: var(--primary-color);
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0 15px;
  }

  .navbar-brand h2 {
    font-size: 16px;
  }

  .nav-item span:not(.icon) {
    display: none;
  }

  .nav-item {
    padding: 10px;
  }
}
</style>
