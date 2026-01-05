<template>
  <div class="section-list-view">
    <div class="page-header">
      <h1 class="page-title">مدیریت بخش‌ها</h1>
      <RouterLink to="/sections/new" class="btn btn-primary">
        ➕ افزودن بخش جدید
      </RouterLink>
    </div>

    <!-- فیلتر بر اساس دپارتمان -->
    <div class="card mb-3">
      <div class="filter-box">
        <div class="row">
          <div class="col-6">
            <label class="form-label">فیلتر بر اساس دپارتمان</label>
            <select v-model="selectedDepartment" class="form-control">
              <option value="">همه دپارتمان‌ها</option>
              <option
                v-for="dept in departmentStore.departments"
                :key="dept.id"
                :value="dept.id"
              >
                {{ dept.name }}
              </option>
            </select>
          </div>
          <div class="col-6">
            <label class="form-label">جستجو</label>
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="جستجو بر اساس نام یا کد..."
            />
          </div>
        </div>
      </div>
    </div>

    <!-- لیست بخش‌ها -->
    <DataTable
      :columns="columns"
      :data="filteredSections"
      :loading="sectionStore.loading"
      @edit="handleEdit"
      @delete="handleDelete"
    >
      <template #cell-department="{ row }">
  <span v-if="row && row.department_name" class="badge badge-info">
    {{ row.department_name }}
  </span>
  <span v-else class="badge badge-secondary">
    نامشخص
  </span>
</template>

    </DataTable>

    <!-- Empty State -->
    <div v-if="!sectionStore.loading && filteredSections.length === 0" class="empty-state">
      <div class="empty-state-icon">📋</div>
      <p class="empty-state-text">هیچ بخشی یافت نشد</p>
      <RouterLink to="/sections/new" class="btn btn-primary mt-2">
        ایجاد اولین بخش
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useSectionStore } from '@/stores/sectionStore'
import { useDepartmentStore } from '@/stores/departmentStore'
import DataTable from '@/components/shared/DataTable.vue'

const router = useRouter()
const sectionStore = useSectionStore()
const departmentStore = useDepartmentStore()

const searchQuery = ref('')
const selectedDepartment = ref('')

const columns = [
  { key: 'code', label: 'کد' },
  { key: 'name', label: 'نام بخش' },
  { key: 'department_name', label: 'دپارتمان' }, // ✅
  { key: 'head_name', label: 'رئیس بخش' },
  { key: 'staff_count', label: 'تعداد پرسنل' },
  { key: 'actions', label: 'عملیات' }
]


// ✅ اضافه کردن نام دپارتمان به بخش‌ها
const sectionsWithDepartmentNames = computed(() => {
  return sectionStore.sections.map(section => {
    const department = departmentStore.getDepartmentById(section.department)
    return {
      ...section,
      department_name: department?.name || 'نامشخص'
    }
  })
})

// ✅ فیلتر بر اساس دپارتمان و جستجو
const filteredSections = computed(() => {
  let result = sectionsWithDepartmentNames.value

  // فیلتر بر اساس دپارتمان
  if (selectedDepartment.value) {
    result = result.filter(section => section.department === Number(selectedDepartment.value))
  }

  // جستجو
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(section =>
      section.name.toLowerCase().includes(query) ||
      section.code.toLowerCase().includes(query) ||
      (section.department_name && section.department_name.toLowerCase().includes(query))
    )
  }

  return result
})

function handleEdit(section) {
  router.push({ name: 'section-edit', params: { id: section.id } })
}

async function handleDelete(section) {
  if (confirm(`آیا از حذف بخش "${section.name}" اطمینان دارید؟`)) {
    await sectionStore.deleteSection(section.id)
  }
}

onMounted(async () => {
  // ✅ حتماً اول دپارتمان‌ها باید لود بشن
  await departmentStore.fetchDepartments()
  await sectionStore.fetchSections()
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

.filter-box {
  padding: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--dark-color);
}

.form-control {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
}

.badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.badge-info {
  background: #e3f2fd;
  color: #1976d2;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  margin-top: 20px;
}

.empty-state-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state-text {
  font-size: 18px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.row {
  display: flex;
  gap: 15px;
  margin: 0 -7.5px;
}

.col-6 {
  flex: 0 0 50%;
  padding: 0 7.5px;
}

.mb-3 {
  margin-bottom: 20px;
}

.mt-2 {
  margin-top: 10px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .row {
    flex-direction: column;
  }

  .col-6 {
    flex: 0 0 100%;
  }
}
</style>
