<template>
  <div class="department-list-view">
    <div class="page-header">
      <h1 class="page-title">مدیریت دپارتمان‌ها</h1>
      <RouterLink to="/departments/new" class="btn btn-primary">
        ➕ افزودن دپارتمان جدید
      </RouterLink>
    </div>

    <!-- جستجو و فیلتر -->
    <div class="card mb-3">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="جستجو بر اساس نام یا کد..."
        />
      </div>
    </div>

    <!-- لیست دپارتمان‌ها -->
    <DataTable
      :columns="columns"
      :data="filteredDepartments"
      :loading="departmentStore.loading"
      @edit="handleEdit"
      @delete="handleDelete"
    />

    <!-- Empty State -->
    <div v-if="!departmentStore.loading && filteredDepartments.length === 0" class="empty-state">
      <div class="empty-state-icon">📂</div>
      <p class="empty-state-text">هیچ دپارتمانی یافت نشد</p>
      <RouterLink to="/departments/new" class="btn btn-primary mt-2">
        ایجاد اولین دپارتمان
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useDepartmentStore } from '@/stores/departmentStore'
import DataTable from '@/components/shared/DataTable.vue'

const router = useRouter()
const departmentStore = useDepartmentStore()
const searchQuery = ref('')

const columns = [
  { key: 'code', label: 'کد' },
  { key: 'name', label: 'نام دپارتمان' },
  { key: 'section_count', label: 'تعداد بخش‌ها' },
  { key: 'actions', label: 'عملیات' }
]

const filteredDepartments = computed(() => {
  if (!searchQuery.value) return departmentStore.departments

  const query = searchQuery.value.toLowerCase()
  return departmentStore.departments.filter(dept =>
    dept.name.toLowerCase().includes(query) ||
    dept.code.toLowerCase().includes(query)
  )
})

function handleEdit(department) {
  router.push({ name: 'department-edit', params: { id: department.id } })
}

async function handleDelete(department) {
  if (confirm(`آیا از حذف دپارتمان "${department.name}" اطمینان دارید؟`)) {
    await departmentStore.deleteDepartment(department.id)
  }
}

onMounted(() => {
  departmentStore.fetchDepartments()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 28px;
  color: var(--dark-color);
}

.search-box {
  padding: 15px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
}
</style>
