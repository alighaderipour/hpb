import { defineStore } from "pinia";
import apiClient from "@/config/axios";

export const useSectionStore = defineStore("section", {
  state: () => ({
    sections: [],
    currentSection: null,
    loading: false,
    error: null,
  }),

  getters: {
    getSectionById: (state) => (id) => {
      return state.sections.find((section) => section.id === id);
    },
    getSectionsByDepartment: (state) => (departmentId) => {
      return state.sections.filter(
        (section) => section.department === departmentId
      );
    },
  },

  actions: {
    async fetchSections() {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get("/api/sections/"); // ✅ تغییر axios به apiClient
        this.sections = response.data;
        console.log("✅ بخش‌ها لود شدند:", this.sections);
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در دریافت بخش‌ها";
        console.error("❌ خطا در fetchSections:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchSection(id) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get(`/api/sections/${id}/`); // ✅
        this.currentSection = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در دریافت بخش";
        console.error("❌ خطا در fetchSection:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createSection(sectionData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.post("/api/sections/", sectionData); // ✅
        this.sections.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در ایجاد بخش";
        console.error("❌ خطا در createSection:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateSection(id, sectionData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.put(
          `/api/sections/${id}/`,
          sectionData
        ); // ✅
        const index = this.sections.findIndex((s) => s.id === id);
        if (index !== -1) {
          this.sections[index] = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در ویرایش بخش";
        console.error("❌ خطا در updateSection:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteSection(id) {
      this.loading = true;
      this.error = null;
      try {
        await apiClient.delete(`/api/sections/${id}/`); // ✅
        this.sections = this.sections.filter((s) => s.id !== id);
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در حذف بخش";
        console.error("❌ خطا در deleteSection:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },
  },
});
