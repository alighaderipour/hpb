import { defineStore } from "pinia";
import apiClient from "@/config/axios"; // ✅ درست

export const useDepartmentStore = defineStore("department", {
  state: () => ({
    departments: [],
    currentDepartment: null,
    loading: false,
    error: null,
  }),

  getters: {
    getDepartmentById: (state) => (id) => {
      return state.departments.find((dept) => dept.id === id);
    },
  },

  actions: {
    async fetchDepartments() {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get("/api/departments/"); // ✅ استفاده از apiClient
        this.departments = response.data;
        console.log("✅ دپارتمان‌ها لود شدند:", response.data); // 👈 برای دیباگ
      } catch (error) {
        this.error =
          error.response?.data?.message || "خطا در دریافت دپارتمان‌ها";
        console.error("❌ خطا در fetchDepartments:", error);
        console.error("❌ Response:", error.response); // 👈 برای دیباگ
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchDepartment(id) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get(`/api/departments/${id}/`);
        this.currentDepartment = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در دریافت دپارتمان";
        console.error("❌ خطا در fetchDepartment:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createDepartment(departmentData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.post(
          "/api/departments/",
          departmentData
        );
        this.departments.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در ایجاد دپارتمان";
        console.error("❌ خطا در createDepartment:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateDepartment(id, departmentData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.put(
          `/api/departments/${id}/`,
          departmentData
        );
        const index = this.departments.findIndex((d) => d.id === id);
        if (index !== -1) {
          this.departments[index] = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در ویرایش دپارتمان";
        console.error("❌ خطا در updateDepartment:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteDepartment(id) {
      this.loading = true;
      this.error = null;
      try {
        await apiClient.delete(`/api/departments/${id}/`);
        this.departments = this.departments.filter((d) => d.id !== id);
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در حذف دپارتمان";
        console.error("❌ خطا در deleteDepartment:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },
  },
});
