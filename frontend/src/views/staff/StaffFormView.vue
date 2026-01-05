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
        <!-- اطلاعات پایه -->
        <h3 class="section-title">اطلاعات پایه</h3>

        <div class="row">
          <div class="col-6">
            <div class="form-group">
              <label class="form-label">کد پرسنلی *</label>
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
        </div>

        <div class="row">
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

          <div class="col-6">
            <div class="form-group">
              <label class="form-label">کد ملی</label>
              <input
                v-model="form.national_code"
                type="text"
                class="form-control"
                :class="{ error: errors.national_code }"
                maxlength="10"
              />
              <span v-if="errors.national_code" class="form-error">{{ errors.national_code }}</span>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-6">
            <div class="form-group">
              <label class="form-label">ایمیل</label>
              <input
                v-model="form.email"
                type="email"
                class="form-control"
                :class="{ error: errors.email }"
              />
              <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
            </div>
          </div>

          <div class="col-6">
            <div class="form-group">
              <label class="form-label">تاریخ استخدام</label>
              <input
                v-model="form.hire_date"
                type="date"
                class="form-control"
                :class="{ error: errors.hire_date }"
              />
              <span v-if="errors.hire_date" class="form-error">{{ errors.hire_date }}</span>
            </div>
          </div>
        </div>

        <!-- محل خدمت -->
        <h3 class="section-title">محل خدمت</h3>

        <div class="row">
          <div class="col-6">
            <div class="form-group">
              <label class="form-label">دپارتمان *</label>
              <select
                v-model="selectedDepartment"
                class="form-control"
                :class="{ error: errors.department }"
                @change="onDepartmentChange"
                required
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
                v-model="form.section_id"
                class="form-control"
                :class="{ error: errors.section }"
                :disabled="!selectedDepartment"
                required
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
          <div class="col-12">
            <div class="form-group">
              <label class="form-label">سمت</label>
              <input
                v-model="form.position"
                type="text"
                class="form-control"
                placeholder="مثال: کارشناس، مدیر، ..."
              />
            </div>
          </div>
        </div>

        <!-- شماره تماس -->
        <h3 class="section-title">شماره‌های تماس</h3>

        <div class="phones-container">
          <div
            v-for="(phone, index) in form.phones"
            :key="index"
            class="phone-input-group"
          >
            <input
              v-model="phone.phone_number"
              type="text"
              class="form-control"
              placeholder="مثال: 09123456789"
              @input="validatePhone(index)"
            />

            <select v-model="phone.phone_type" class="form-control" style="max-width: 150px;">
              <option value="">نوع تلفن</option>
              <option
                v-for="type in phoneTypes"
                :key="type.id"
                :value="type.id"
              >
                {{ type.name }}
              </option>
            </select>

            <label class="checkbox-label">
              <input type="checkbox" v-model="phone.is_public" />
              عمومی
            </label>

            <button
              type="button"
              class="btn btn-danger btn-sm"
              @click="removePhone(index)"
              :disabled="form.phones.length === 1"
            >
              ❌
            </button>
          </div>

          <button type="button" class="btn btn-outline btn-sm" @click="addPhone">
            ➕ افزودن شماره
          </button>

          <span v-if="errors.phones" class="form-error">{{ errors.phones }}</span>
        </div>

        <!-- دکمه‌ها -->
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
import { useDepartmentStore } from '@/stores/departmentStore'
import { useSectionStore } from '@/stores/sectionStore'
import apiClient from '@/config/axios'

const router = useRouter()
const route = useRoute()
const staffStore = useStaffStore()
const departmentStore = useDepartmentStore()
const sectionStore = useSectionStore()

const loading = ref(false)
const errors = ref({})
const selectedDepartment = ref('')
const phoneTypes = ref([])

const form = ref({
  personnel_code: '',
  first_name: '',
  last_name: '',
  national_code: '',
  email: '',
  hire_date: '',
  section_id: '',
  position: '',
  phones: [{
    phone_number: '',
    phone_type: '',
    is_public: true
  }]
})

const isEditMode = computed(() => !!route.params.id)

const filteredSections = computed(() => {
  if (!selectedDepartment.value) return []
  return sectionStore.sections.filter(
    section => section.department === Number(selectedDepartment.value)
  )
})

function onDepartmentChange() {
  form.value.section_id = ''
}

function addPhone() {
  form.value.phones.push({
    phone_number: '',
    phone_type: '',
    is_public: true
  })
}

function removePhone(index) {
  if (form.value.phones.length > 1) {
    form.value.phones.splice(index, 1)
  }
}

function validatePhone(index) {
  const phone = form.value.phones[index].phone_number
  if (phone && !/^[\d\-\s()]+$/.test(phone)) {
    errors.value.phones = 'فرمت شماره تلفن معتبر نیست'
  } else {
    delete errors.value.phones
  }
}

async function handleSubmit() {
  loading.value = true
  errors.value = {}

  // ✅ فیلتر شماره‌های خالی
  const validPhones = form.value.phones.filter(phone => phone.phone_number.trim() && phone.phone_type)

  if (validPhones.length === 0) {
    errors.value.phones = 'حداقل یک شماره تلفن با نوع مشخص الزامی است'
    loading.value = false
    return
  }

  try {
    // ✅ ساختار صحیح برای Backend
    const payload = {
      personnel_code: form.value.personnel_code,
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      national_code: form.value.national_code || null,
      email: form.value.email || null,
      hire_date: form.value.hire_date || null,
      is_active: true
    }

    let staffResponse

    if (isEditMode.value) {
      // ✅ به‌روزرسانی Staff
      staffResponse = await apiClient.put(`/api/staff/${route.params.id}/`, payload)
    } else {
      // ✅ ایجاد Staff
      staffResponse = await apiClient.post('/api/staff/', payload)
    }

    const staffId = staffResponse.data.id

    // ✅ ایجاد/به‌روزرسانی Assignment (محل خدمت)
    if (form.value.section_id) {
      const assignmentPayload = {
        staff: staffId,
        section: form.value.section_id,
        is_current: true,
        position: form.value.position || null,
        start_date: form.value.hire_date || new Date().toISOString().split('T')[0]
      }

      if (isEditMode.value) {
        // چک کردن Assignment فعلی
        const assignments = await apiClient.get(`/api/staff-assignments/?staff=${staffId}&is_current=true`)
        if (assignments.data.length > 0) {
          await apiClient.put(`/api/staff-assignments/${assignments.data[0].id}/`, assignmentPayload)
        } else {
          await apiClient.post('/api/staff-assignments/', assignmentPayload)
        }
      } else {
        await apiClient.post('/api/staff-assignments/', assignmentPayload)
      }
    }

    // ✅ ایجاد/به‌روزرسانی Phones
    if (isEditMode.value) {
      // حذف شماره‌های قبلی
      await apiClient.delete(`/api/staff-phones/?staff=${staffId}`)
    }

    // افزودن شماره‌های جدید
    for (const phone of validPhones) {
      await apiClient.post('/api/staff-phones/', {
        staff: staffId,
        phone_type: phone.phone_type,
        phone_number: phone.phone_number,
        is_public: phone.is_public,
        is_active: true
      })
    }

    router.push('/staff')
  } catch (error) {
    console.error('❌ خطا در ذخیره:', error)
    if (error.response?.data) {
      errors.value = error.response.data
    } else {
      errors.value = { general: 'خطا در ذخیره اطلاعات' }
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await departmentStore.fetchDepartments()
  await sectionStore.fetchSections()

  // ✅ لود نوع تلفن‌ها
  try {
    const response = await apiClient.get('/api/phone-types/')
    phoneTypes.value = response.data.filter(type => type.is_active)
  } catch (error) {
    console.error('❌ خطا در لود نوع تلفن‌ها:', error)
  }

  // ✅ لود اطلاعات در حالت ویرایش
  if (isEditMode.value) {
    try {
      const staff = await staffStore.fetchStaffDetail(route.params.id)
      
      form.value = {
        personnel_code: staff.personnel_code,
        first_name: staff.first_name,
        last_name: staff.last_name,
        national_code: staff.national_code || '',
        email: staff.email || '',
        hire_date: staff.hire_date || '',
        section_id: staff.current_section?.id || '',
        position: staff.assignments?.[0]?.position || '',
        phones: staff.phones.length > 0 ? staff.phones.map(p => ({
          phone_number: p.phone_number,
          phone_type: p.phone_type,
          is_public: p.is_public
        })) : [{
          phone_number: '',
          phone_type: '',
          is_public: true
        }]
      }

      // ✅ تنظیم دپارتمان برای فیلتر بخش‌ها
      if (staff.current_section) {
        const section = sectionStore.getSectionById(staff.current_section.id)
        if (section) {
          selectedDepartment.value = section.department
        }
      }
    } catch (error) {
      console.error('❌ خطا در لود Staff:', error)
    }
  }
})
</script>

<style scoped>
/* همون استایل‌های قبلی */
.section-title {
  font-size: 18px;
  margin: 30px 0 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--border-color);
  color: var(--primary-color);
}

.section-title:first-of-type {
  margin-top: 0;
}

.phones-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.phone-input-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.phone-input-group .form-control {
  flex: 1;
}

.phone-input-group .btn {
  flex-shrink: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.form-error {
  color: #dc3545;
  font-size: 13px;
  margin-top: 5px;
  display: block;
}

.row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.col-6 {
  flex: 0 0 calc(50% - 7.5px);
}

.col-12 {
  flex: 0 0 100%;
}

.form-group {
  margin-bottom: 0;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.form-control.error {
  border-color: #dc3545;
}

.form-control:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}
</style>
