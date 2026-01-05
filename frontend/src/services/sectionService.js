import apiClient from "@/api/axios";

export default {
  async getSections(params = {}) {
    const response = await apiClient.get("/sections/", { params });
    return response.data;
  },

  async getSection(id) {
    const response = await apiClient.get(`/sections/${id}/`);
    return response.data;
  },

  async createSection(data) {
    const response = await apiClient.post("/sections/", data);
    return response.data;
  },

  async updateSection(id, data) {
    const response = await apiClient.put(`/sections/${id}/`, data);
    return response.data;
  },

  async deleteSection(id) {
    await apiClient.delete(`/sections/${id}/`);
  },

  // دریافت انواع سکشن
  async getSectionTypes() {
    const response = await apiClient.get("/section-types/");
    return response.data;
  },

  // دریافت انواع تلفن
  async getPhoneTypes() {
    const response = await apiClient.get("/phone-types/");
    return response.data;
  },
};
