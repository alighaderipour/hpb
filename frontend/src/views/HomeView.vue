<template>
  <div class="home-view">
    <h1 class="page-title">داشبورد</h1>

    <!-- آمار کلی -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">🏢</div>
        <div class="stat-content">
          <h3>{{ stats.departments || 0 }}</h3>
          <p>دپارتمان</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-content">
          <h3>{{ stats.sections || 0 }}</h3>
          <p>بخش</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>{{ stats.staff || 0 }}</h3>
          <p>پرسنل</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📞</div>
        <div class="stat-content">
          <h3>{{ stats.total_phones || 0 }}</h3>
          <p>شماره تلفن</p>
        </div>
      </div>
    </div>

    <!-- دسترسی سریع -->
    <div class="card mt-4">
      <div class="card-header">
        <h2 class="card-title">دسترسی سریع</h2>
      </div>

      <div class="quick-actions">
        <RouterLink to="/departments" class="action-btn">
          <span class="action-icon">🏢</span>
          <span>مدیریت دپارتمان‌ها</span>
        </RouterLink>

        <RouterLink to="/sections" class="action-btn">
          <span class="action-icon">📋</span>
          <span>مدیریت بخش‌ها</span>
        </RouterLink>

        <RouterLink to="/staff" class="action-btn">
          <span class="action-icon">👥</span>
          <span>مدیریت پرسنل</span>
        </RouterLink>

        <RouterLink to="/search" class="action-btn">
          <span class="action-icon">🔍</span>
          <span>جستجو در دفترچه</span>
        </RouterLink>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from '@/api/axios'

const loading = ref(false)
const stats = ref({
  departments: 0,
  sections: 0,
  staff: 0,
  total_phones: 0
})

async function fetchStats() {
  loading.value = true
  try {
    const response = await axios.get('/statistics/')
    stats.value = response.data
  } catch (error) {
    console.error('خطا در دریافت آمار:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.home-view {
  padding: 1rem 0;
}

/* ===== Page Title ===== */
.page-title {
  font-size: 1.6rem;
  font-weight: 600;
  margin-bottom: 1.75rem;
  color: #1f2d3d;
}

/* ===== Statistics ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #1e88e5, #1565c0);
  color: #fff;
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content h3 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: #1e88e5;
}

.stat-content p {
  font-size: 0.8rem;
  color: #6b7a8c;
}

/* ===== Card ===== */
.card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.card-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eef1f4;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2d3d;
}

/* ===== Quick Actions ===== */
.quick-actions {
  padding: 1.25rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.9rem 1.1rem;
  background: #f4f6f8;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #2c3e50;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: linear-gradient(135deg, #1e88e5, #1565c0);
  color: #ffffff;
  transform: translateX(-4px);
}

.action-icon {
  font-size: 1.4rem;
}

/* ===== Loading ===== */
.loading-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.loading-spinner {
  width: 42px;
  height: 42px;
  border: 4px solid #e0e6ed;
  border-top-color: #1e88e5;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.3rem;
  }
}

</style>
