<template>
  <aside class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <button @click="toggleSidebar" class="toggle-btn">
      {{ isCollapsed ? '→' : '←' }}
    </button>

    <nav class="sidebar-nav">
      <RouterLink
        v-for="item in menuItems"
        :key="item.name"
        :to="{ name: item.name }"
        class="nav-link"
        active-class="active"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span v-if="!isCollapsed" class="nav-text">{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div v-if="!isCollapsed" class="sidebar-footer">
      <p class="version">نسخه 1.0.0</p>
      <p class="copyright">© 1404 بیمارستان</p>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const isCollapsed = ref(false)

const menuItems = [
  { name: 'home', label: 'داشبورد', icon: '🏠' },
  { name: 'departments', label: 'دپارتمان‌ها', icon: '🏢' },
  { name: 'sections', label: 'بخش‌ها', icon: '📋' },
  { name: 'staff', label: 'پرسنل', icon: '👥' },
  { name: 'search', label: 'جستجو', icon: '🔍' }
]

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 64px;
  right: 0;
  width: 240px;
  height: calc(100vh - 64px);
  background: #ffffff;
  border-left: 1px solid #eef1f4;
  box-shadow: -4px 0 14px rgba(0, 0, 0, 0.04);
  transition: width 0.25s ease;
  z-index: 90;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: 64px;
}

/* ===== Toggle ===== */
.toggle-btn {
  border: none;
  background: #f4f6f8;
  padding: 0.9rem;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;
}

.toggle-btn:hover {
  background: #e9edf2;
}

/* ===== Navigation ===== */
.sidebar-nav {
  padding: 0.75rem 0;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 1.25rem;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  color: #2c3e50;
  border-right: 3px solid transparent;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-link:hover {
  background: #f4f6f8;
}

.nav-link.active {
  background: linear-gradient(
    90deg,
    rgba(30, 136, 229, 0.12),
    transparent
  );
  border-right-color: #1e88e5;
  color: #1e88e5;
  font-weight: 600;
}

.nav-icon {
  font-size: 1.2rem;
  min-width: 20px;
  text-align: center;
}

.nav-text {
  white-space: nowrap;
}

/* ===== Footer ===== */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #eef1f4;
  text-align: center;
  font-size: 0.7rem;
  color: #9aa6b2;
}

.version {
  margin-bottom: 0.25rem;
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(100%);
  }

  .sidebar.collapsed {
    transform: translateX(0);
    width: 64px;
  }
}


</style>
