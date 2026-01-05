<template>
  <div class="staff-list">
    <DataTable
      :data="staffStore.staffList"
      :columns="columns"
      @add="openAddModal"
      @edit="openEditModal"
      @delete="confirmDelete"
    >
      <template #cell-phones="{ item }">
        <div class="phones">
          <div v-for="phone in item.phones" :key="phone.id" class="phone-item">
            <span class="phone-type">{{ phone.phone_type_name }}:</span>
            <span class="phone-number">{{ phone.phone_number }}</span>
          </div>
        </div>
      </template>

      <template #cell-current_section="{ item }">
        <span v-if="item.current_assignment">
          {{ item.current_assignment.section_name }}
        </span>
        <span v-else class="text-muted">بدون انتساب</span>
      </template>
    </DataTable>

    <Modal v-model="showModal" :title="modalTitle" @confirm="saveStaff">
      <StaffForm v-model="formData" />
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStaffStore } from '@/stores/staffStore'
import { useAuthStore } from '@/stores/authStore'
import DataTable from '@/components/shared/DataTable.vue'
import Modal from '@/components/shared/Modal.vue'
import StaffForm from './StaffForm.vue'

const staffStore = useStaffStore()
const authStore = useAuthStore()

const showModal = ref(false)
const modalTitle = ref('')
const formData = ref({})
const editingId = ref(null)

const columns = ref([
  { key: 'first_name', label: 'نام' },
  { key: 'last_name', label: 'نام خانوادگی' },
  { key: 'personnel_code', label: 'کد پرسنلی' },
  { key: 'current_section', label: 'بخش فعلی' },
  { key: 'phones', label: 'شماره تماس' }
])

onMounted(() => {
  staffStore.fetchStaff()
})

function openAddModal() {
  modalTitle.value = 'افزودن پرسنل جدید'
  formData.value = {}
  editingId.value = null
  showModal.value = true
}

function openEditModal(item) {
  modalTitle.value = 'ویرایش پرسنل'
  formData.value = { ...item }
  editingId.value = item.id
  showModal.value = true
}

async function saveStaff() {
  try {
    if (editingId.value) {
      await staffStore.updateStaff(editingId.value, formData.value)
    } else {
      await staffStore.createStaff(formData.value)
    }
    showModal.value = false
  } catch (error) {
    alert('خطا در ذخیره اطلاعات')
  }
}

async function confirmDelete(item) {
  if (confirm(`آیا از حذف ${item.first_name} ${item.last_name} مطمئن هستید؟`)) {
    try {
      await staffStore.deleteStaff(item.id)
    } catch (error) {
      alert('خطا در حذف پرسنل')
    }
  }
}
</script>

<style scoped>
.phones {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.phone-item {
  font-size: 14px;
}

.phone-type {
  font-weight: bold;
  margin-left: 5px;
}

.text-muted {
  color: #999;
}
</style>
