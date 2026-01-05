<template>
  <div class="data-table">
    <div class="table-header">
      <input 
        v-model="searchQuery"
        type="text" 
        placeholder="جستجو..."
        class="search-input"
      />
      <button @click="$emit('add')" class="btn-primary">
        افزودن جدید
      </button>
    </div>

    <table>
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key">
            {{ column.label }}
          </th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in filteredData" :key="item.id">
          <td v-for="column in columns" :key="column.key">
            <slot :name="`cell-${column.key}`" :item="item">
              {{ getNestedValue(item, column.key) }}
            </slot>
          </td>
          <td class="actions">
            <button @click="$emit('edit', item)" class="btn-edit">
              ویرایش
            </button>
            <button @click="$emit('delete', item)" class="btn-delete">
              حذف
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="filteredData.length === 0" class="no-data">
      هیچ داده‌ای یافت نشد
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  }
})

defineEmits(['add', 'edit', 'delete'])

const searchQuery = ref('')

const filteredData = computed(() => {
  if (!searchQuery.value) return props.data
  
  const query = searchQuery.value.toLowerCase()
  return props.data.filter(item => {
    return props.columns.some(column => {
      const value = getNestedValue(item, column.key)
      return String(value).toLowerCase().includes(query)
    })
  })
})

function getNestedValue(obj, path) {
  return path.split('.').reduce((current, prop) => current?.[prop], obj)
}
</script>

<style scoped>
.data-table {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 300px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: right;
  border-bottom: 1px solid #eee;
}

th {
  background: #f5f5f5;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-primary {
  background: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-edit {
  background: #2196F3;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-delete {
  background: #f44336;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
}
</style>
