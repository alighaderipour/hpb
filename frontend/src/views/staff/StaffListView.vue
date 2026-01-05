<template>
  <div class="staff-list-view">
    <div class="page-header">
      <h1 class="page-title">مدیریت پرسنل</h1>
      <RouterLink to="/staff/new" class="btn btn-primary">
        ➕ افزودن پرسنل جدید
      </RouterLink>
    </div>

    <!-- فیلترها -->
    <div class="card mb-3">
      <div class="filter-box">
        <div class="row">
          <div class="col-4">
            <label class="form-label">دپارتمان</label>
            <select v-model="filters.department" class="form-control" @change="onDepartmentChange">
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

          <div class="col-4">
            <label class="form-label">بخش</label>
            <select v-model="filters.section" class="form-control" :disabled="!filters.department">
              <option value="">همه بخش‌ها</option>
              <option
                v-for="section in filteredSections"
                :key="section.id"
                :value="section.id"
              >
                {{ section.name }}
              </option>
            </select>
          </div>

          <div class="col-4">
            <label class="form-label">جستجو</label>
            <input
              v-model="filters.search"
              type="text"
              class="form-control"
              placeholder="نام، کد پرسنلی، تلفن..."
            />
          </div>
        </div>
      </div>
    </div>

    <!-- لیست پرسنل -->
    <DataTable
      :columns="columns"
      :data="filteredStaff"
      :loading="staffStore.loading"
      @edit="handleEdit"
      @delete="handleDelete"
    >
      <!-- ✅ تغییر row به item -->
      <template #cell-personnel_code="{ item }">
        <span class="code-badge">{{ item.personnel_code }}</span>
      </template>

      <template #cell-section_info="{ item }">
        <div class="section-info">
          <div v-if="item.section_name" class="section-name">
            {{ item.section_name }}
          </div>
          <div v-else class="text-muted">بدون بخش</div>
        </div>
      </template>

      <template #cell-phones="{ item }">
        <div class="phones-list">
          <template v-if="item.phones && item.phones.length > 0">
            <span
              v-for="(phone, index) in item.phones"
              :key="index"
              class="phone-badge"
            >
              {{ formatPhoneNumber(phone.phone_number) }}
            </span>
          </template>
          <span v-else class="text-muted">بدون تلفن</span>
        </div>
      </template>

      <template #cell-status="{ item }">
        <span :class="['status-badge', item.is_active ? 'status-active' : 'status-inactive']">
          {{ item.is_active ? 'فعال' : 'غیرفعال' }}
        </span>
      </template>
    </DataTable>

    <!-- Empty State -->
    <div v-if="!staffStore.loading && filteredStaff.length === 0" class="empty-state">
      <div class="empty-state-icon">👥</div>
      <p class="empty-state-text">هیچ پرسنلی یافت نشد</p>
      <RouterLink to="/staff/new" class="btn btn-primary mt-2">
        افزودن اولین پرسنل
      </RouterLink>
    </div>

    <!-- آمار خلاصه -->
    <div v-if="filteredStaff.length > 0" class="stats-footer">
      <div class="stat-item">
        <span class="stat-label">مجموع:</span>
        <span class="stat-value">{{ filteredStaff.length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">فعال:</span>
        <span class="stat-value text-success">{{ activeStaffCount }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">غیرفعال:</span>
        <span class="stat-value text-danger">{{ inactiveStaffCount }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useStaffStore } from '@/stores/staffStore'
import { useDepartmentStore } from '@/stores/departmentStore'
import { useSectionStore } from '@/stores/sectionStore'
import DataTable from '@/components/shared/DataTable.vue'

const router = useRouter()
const staffStore = useStaffStore()
const departmentStore = useDepartmentStore()
const sectionStore = useSectionStore()

const filters = ref({
  department: '',
  section: '',
  search: ''
})

const columns = [
  { key: 'personnel_code', label: 'کد پرسنلی', width: '120px' },
  { key: 'full_name', label: 'نام و نام خانوادگی', width: '200px' },
  { key: 'section_info', label: 'محل خدمت', width: '200px' },
  { key: 'phones', label: 'شماره تماس', width: '180px' },
  { key: 'status', label: 'وضعیت', width: '100px' },
  { key: 'actions', label: 'عملیات', width: '120px' }
]

const filteredSections = computed(() => {
  if (!filters.value.department) return []
  return sectionStore.sections.filter(
    section => section.department === Number(filters.value.department)
  )
})

const filteredStaff = computed(() => {
  let result = [...staffStore.staff]

  if (filters.value.section) {
    const selectedSection = sectionStore.sections.find(
      s => s.id === Number(filters.value.section)
    )
    if (selectedSection) {
      result = result.filter(staff => 
        staff.section_name === selectedSection.name ||
        staff.current_section_name === selectedSection.name
      )
    }
  }

  if (filters.value.department && !filters.value.section) {
    const departmentSections = filteredSections.value.map(s => s.name)
    result = result.filter(staff => 
      departmentSections.includes(staff.section_name) ||
      departmentSections.includes(staff.current_section_name)
    )
  }

  if (filters.value.search) {
    const query = filters.value.search.toLowerCase()
    result = result.filter(staff => {
      const fullNameMatch = staff.full_name?.toLowerCase().includes(query)
      const firstNameMatch = staff.first_name?.toLowerCase().includes(query)
      const lastNameMatch = staff.last_name?.toLowerCase().includes(query)
      const codeMatch = staff.personnel_code?.toLowerCase().includes(query)
      const phoneMatch = staff.phones?.some(phone => {
        const phoneNum = typeof phone === 'string' ? phone : phone?.phone_number
        return phoneNum?.includes(query)
      })
      return fullNameMatch || firstNameMatch || lastNameMatch || codeMatch || phoneMatch
    })
  }

  return result
})

const activeStaffCount = computed(() => {
  return filteredStaff.value.filter(s => s.is_active).length
})

const inactiveStaffCount = computed(() => {
  return filteredStaff.value.filter(s => !s.is_active).length
})

function formatPhoneNumber(phone) {
  if (!phone) return ''
  
  phone = String(phone).replace(/\s/g, '')
  
  if (phone.startsWith('09')) {
    return phone.replace(/(\d{4})(\d{3})(\d{4})/, '$1-$2-$3')
  } else if (phone.startsWith('0')) {
    return phone.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3')
  }
  
  return phone
}

function onDepartmentChange() {
  filters.value.section = ''
}

function handleEdit(staff) {
  router.push({ name: 'staff-edit', params: { id: staff.id } })
}

async function handleDelete(staff) {
  if (confirm(`آیا از حذف پرسنل "${staff.full_name}" اطمینان دارید؟`)) {
    try {
      await staffStore.deleteStaff(staff.id)
    } catch (error) {
      alert('خطا در حذف پرسنل')
    }
  }
}

onMounted(async () => {
  await departmentStore.fetchDepartments()
  await sectionStore.fetchSections()
  await staffStore.fetchStaff()
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

.code-badge {
  display: inline-block;
  padding: 4px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.5px;
}

.section-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-name {
  font-weight: 600;
  color: var(--dark-color);
  font-size: 14px;
}

.text-muted {
  color: #999;
  font-size: 13px;
  font-style: italic;
}

.phones-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.phone-badge {
  display: inline-block;
  padding: 4px 10px;
  background: #f5f5f5;
  border-radius: 12px;
  font-size: 13px;
  direction: ltr;
  text-align: left;
  font-family: 'Courier New', monospace;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-inactive {
  background: #f8d7da;
  color: #721c24;
}

.stats-footer {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color);
}

.text-success {
  color: #28a745 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 20px;
}

.empty-state-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state-text {
  color: #666;
  font-size: 18px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .stats-footer {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
