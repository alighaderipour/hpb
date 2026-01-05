<template>
  <div class="staff-form-view">
    <div class="page-header">
      <h1 class="page-title">
        {{ isEditMode ? 'ویرایش پرسنل' : 'افزودن پرسنل جدید' }}
      </h1>
      <RouterLink to="/staff" class="btn btn-outline">
        بازگشت به لیست
      </RouterLink>
    </div>

    <div class="card">
      <form @submit.prevent="handleSubmit">
        <div class="row">
          <div class="col-6">
            <div class="form-group">
              <label class="form-label">نام *</label>
              <input
                v-model="form.first_name"
                type="text"
                class="form-control"
                :class="{ error: errors.first_name }"
                required
              />
              <span v-if="errors.first_name" class="form-error">{{ errors.first_name }}</span>
            </div>
          </div>

          <div class="col-6">
            <div class="form-group">
              <label class="form-label">نام خانوادگی *</label>
              <input
                v-model="form.last_name"
                type="text"
                class="form-control"
                :class="{ error: errors.last_name }"
                required
              />
              <span v-if="errors.last_name" class="form-error">{{ errors.last_name }}</span>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-6">
            <div class="form-group">
              <label class="form-label">دپارتمان *</label>
              <select
                v-model="form.department"
                class="form-control"
                :class="{ error: errors.department }"
                required
                @change="loadSections"
              >
                <option value="">انتخاب دپارتمان</option>
                <option
                  v-for="dept in departmentStore.departments"
                  :key="dept.id"
                  :value="dept.id"
                >
                  {{ dept.name }}
                </option>
              </select>
              <span v-if="errors.department" class="form-error">{{ errors.department }}</span>
            </div>
          </div>

          <div class="col-6">
            <div class="form-group">
              <label class="form-label">بخش *</label>
              <select
                v-model="form.section"
                class="form-control"
                :class="{ error: errors.section }"
                required
                :disabled="!form.department"
              >
                <option value="">انتخاب بخش</option>
                <option
                  v-for="section in filteredSections"
                  :key="section.id"
                  :value="section.id"
                >
                  {{ section.name }}
                </option>
              </select>
              <span v-if="errors.section" class="form-error">{{ errors.section }}</span>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-6">
            <div class="form-group">
              <label class="form-label">شماره پرسنلی *</label>
              <input
                v-model="form.personnel_code"
                type="text"
                class="form-control"
                :class="{ error: errors.personnel_code }"
                required
              />
              <span v-if="errors.personnel_code" class="form-error">{{ errors.personnel_code }}</span>
            </div>
          </div>

          <div class="col-6">
            <div class="form-group">
              <label class="form-label">سمت</label>
              <input
                v-model="form.position"
                type="text"
                class="form-control"
              />
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-6">
            <div class="form-group">
              <label class="form-label">تلفن داخلی</label>
              <input
                v-model="form.internal_phone"
                type="text"
                class="form-control"
              />
            </div>
          </div>

          <div class="col-6">
            <div class="form-group">
              <label class="form-label">تلفن همراه</label>
              <input
                v-model="form.mobile_phone"
                type="text"
                class="form-control"
              />
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">ایمیل</label>
          <input
            v-model="form.email"
            type="email"
            class="form-control"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'در حال ذخیره...' : (isEditMode ? 'به‌روزرسانی' : 'ایجاد پرسنل') }}
          </button>
          <RouterLink to="/staff" class="btn btn-outline">
            انصراف
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { useStaffStore } from '@/stores/staffStore'
import { useSectionStore } from '@/stores/sectionStore'
import { useDepartmentStore } from '@/stores/departmentStore'

const router = useRouter()
const route = useRoute()
const staffStore = useStaffStore()
const sectionStore = useSectionStore()
const departmentStore = useDepartmentStore()

const loading = ref(false)
const errors = ref({})
const form = ref({
  first_name: '',
  last_name: '',
  personnel_code: '',
  position: '',
  department: '',
  section: '',
  internal_phone: '',
  mobile_phone: '',
  email: ''
})

const isEditMode = computed(() => !!route.params.id)

const filteredSections = computed(() => {
  if (!form.value.department) return []
  return sectionStore.sections.filter(s => s.department === form.value.department)
})

function loadSections() {
  form.value.section = ''
}

async function handleSubmit() {
  loading.value = true
  errors.value = {}

  try {
    if (isEditMode.value) {
      await staffStore.updateStaff(route.params.id, form.value)
    } else {
      await staffStore.createStaff(form.value)
    }
    router.push('/staff')
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  departmentStore.fetchDepartments()
  sectionStore.fetchSections()

  if (isEditMode.value) {
    const staff = await staffStore.fetchStaff(route.params.id)
    form.value = { ...staff }
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}
</style>
