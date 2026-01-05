<template>
  <div class="staff-view">
    <h1>مدیریت پرسنل</h1>
    <StaffList />
  </div>
</template>

<script setup>
import StaffList from '@/components/phonebook/StaffList.vue'
</script>

<style scoped>
.staff-view {
  padding: 20px;
}
</style>
