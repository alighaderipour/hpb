import apiClient from "@/api/axios";

export default {
  // دریافت لیست دپارتمان‌ها
  async getDepartments(params = {}) {
    const response = await apiClient.get("/departments/", { params });
    return response.data;
  },

  // دریافت یک دپارتمان
  async getDepartment(id) {
    const response = await apiClient.get(`/departments/${id}/`);
    return response.data;
  },

  // ایجاد دپارتمان
  async createDepartment(data) {
    const response = await apiClient.post("/departments/", data);
    return response.data;
  },

  // ویرایش دپارتمان
  async updateDepartment(id, data) {
    const response = await apiClient.put(`/departments/${id}/`, data);
    return response.data;
  },

  // حذف دپارتمان
  async deleteDepartment(id) {
    await apiClient.delete(`/departments/${id}/`);
  },

  // دریافت آمار
  async getStatistics() {
    const response = await apiClient.get("/departments/statistics/");
    return response.data;
  },
};
