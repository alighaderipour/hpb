<script setup>
import { ref, computed } from 'vue'
import staffService from '@/services/staffService'

const query = ref('')
const loading = ref(false)
const hasSearched = ref(false)
const results = ref({
  staff: [],
  sections: [],
  departments: []
})

// Live Search با Debounce
let searchTimeout = null
const handleLiveSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  
  if (query.value.trim().length < 2) {
    results.value = { staff: [], sections: [], departments: [] }
    hasSearched.value = false
    return
  }

  searchTimeout = setTimeout(async () => {
    await performSearch()
  }, 500)
}

// تابع اصلی جستجو
async function performSearch() {
  if (!query.value.trim()) return

  loading.value = true
  hasSearched.value = true

  try {
    const response = await staffService.search(query.value)
    results.value = response.data
    console.log('✅ نتایج جستجو:', results.value)
  } catch (error) {
    console.error('❌ خطا در جستجو:', error)
    results.value = { staff: [], sections: [], departments: [] }
  } finally {
    loading.value = false
  }
}

// جستجو با دکمه Enter یا کلیک
const handleSearch = async () => {
  await performSearch()
}

const totalResults = computed(() => {
  return results.value.staff.length + 
         results.value.sections.length + 
         results.value.departments.length
})
</script>

<template>
  <div class="search-view">
    <h1 class="page-title">جستجو در دفترچه تلفن</h1>

    <div class="card mb-4">
      <div class="search-box">
        <input
          v-model="query"
          type="text"
          class="form-control search-input"
          placeholder="نام، کدملی، شماره تلفن..."
          @input="handleLiveSearch"
          @keyup.enter="handleSearch"
        />
        <button 
          class="btn btn-primary" 
          @click="handleSearch" 
          :disabled="loading || query.trim().length < 2"
        >
          {{ loading ? '⏳ در حال جستجو...' : '🔍 جستجو' }}
        </button>
      </div>
    </div>

    <!-- نتایج جستجو -->
    <div v-if="hasSearched">
      <!-- پرسنل -->
      <div v-if="results.staff.length > 0" class="card mb-4">
        <div class="card-header">
          <h2 class="card-title">پرسنل ({{ results.staff.length }})</h2>
        </div>
        <div class="results-list">
          <div v-for="staff in results.staff" :key="staff.id" class="result-item">
            <div class="result-info">
              <h3>{{ staff.full_name }}</h3>
              <p class="text-muted">
                کد پرسنلی: {{ staff.personnel_code }}
              </p>
            </div>
            <div class="result-phones">
              <div v-for="phone in staff.active_phones" :key="phone.id" class="phone-badge">
                📞 {{ phone.phone_number }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- بخش‌ها -->
      <div v-if="results.sections.length > 0" class="card mb-4">
        <div class="card-header">
          <h2 class="card-title">بخش‌ها ({{ results.sections.length }})</h2>
        </div>
        <div class="results-list">
          <div v-for="section in results.sections" :key="section.id" class="result-item">
            <div class="result-info">
              <h3>{{ section.name }}</h3>
              <p class="text-muted">دپارتمان: {{ section.department_name }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- دپارتمان‌ها -->
      <div v-if="results.departments.length > 0" class="card">
        <div class="card-header">
          <h2 class="card-title">دپارتمان‌ها ({{ results.departments.length }})</h2>
        </div>
        <div class="results-list">
          <div v-for="dept in results.departments" :key="dept.id" class="result-item">
            <div class="result-info">
              <h3>{{ dept.name }}</h3>
              <p class="text-muted">کد: {{ dept.code }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- بدون نتیجه -->
      <div v-if="!loading && totalResults === 0" class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <p class="empty-state-text">نتیجه‌ای یافت نشد</p>
        <p class="text-muted">عبارت دیگری جستجو کنید</p>
      </div>
    </div>

    <!-- راهنما -->
    <div v-else class="search-guide">
      <div class="guide-icon">💡</div>
      <h3>راهنمای جستجو</h3>
      <ul>
        <li>حداقل 2 حرف تایپ کنید</li>
        <li>جستجو در نام، کد پرسنلی و شماره تلفن</li>
        <li>نتایج به صورت خودکار نمایش می‌یابند</li>
      </ul>
    </div>
  </div>
</template>
