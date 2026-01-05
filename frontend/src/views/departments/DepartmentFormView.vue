<template>
  <div class="department-form-view">
    <div class="page-header">
      <h1 class="page-title">
        {{ isEditMode ? 'ویرایش دپارتمان' : 'افزودن دپارتمان جدید' }}
      </h1>
      <RouterLink to="/departments" class="btn btn-outline">
        بازگشت به لیست
      </RouterLink>
    </div>

    <div class="card">
      <form @submit.prevent="handleSubmit">
        <div class="row">
          <div class="col-6">
            <div class="form-group">
              <label class="form-label">کد دپارتمان *</label>
              <input
                v-model="form.code"
                type="text"
                class="form-control"
                :class="{ error: errors.code }"
                required
              />
              <span v-if="errors.code" class="form-error">{{ errors.code }}</span>
            </div>
          </div>

          <div class="col-6">
            <div class="form-group">
              <label class="form-label">نام دپارتمان *</label>
              <input
                v-model="form.name"
                type="text"
                class="form-control"
                :class="{ error: errors.name }"
                required
              />
              <span v-if="errors.name" class="form-error">{{ errors.name }}</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">رئیس دپارتمان</label>
          <input
            v-model="form.head_name"
            type="text"
            class="form-control"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'در حال ذخیره...' : (isEditMode ? 'به‌روزرسانی' : 'ایجاد دپارتمان') }}
          </button>
          <RouterLink to="/departments" class="btn btn-outline">
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
import { useDepartmentStore } from '@/stores/departmentStore'

const router = useRouter()
const route = useRoute()
const departmentStore = useDepartmentStore()

const loading = ref(false)
const errors = ref({})
const form = ref({
  code: '',
  name: '',
  head_name: ''
})

const isEditMode = computed(() => !!route.params.id)

async function handleSubmit() {
  loading.value = true
  errors.value = {}

  try {
    if (isEditMode.value) {
      await departmentStore.updateDepartment(route.params.id, form.value)
    } else {
      await departmentStore.createDepartment(form.value)
    }
    router.push('/departments')
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (isEditMode.value) {
    const department = await departmentStore.fetchDepartment(route.params.id)
    form.value = { ...department }
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
