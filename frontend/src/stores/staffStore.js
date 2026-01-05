import { defineStore } from "pinia";
import apiClient from "@/config/axios";

export const useStaffStore = defineStore("staff", {
  state: () => ({
    staff: [],
    currentStaff: null,
    loading: false,
    error: null,
  }),

  getters: {
    activeStaff: (state) => state.staff.filter((s) => s.is_active),

    getStaffById: (state) => (id) => {
      return state.staff.find((s) => s.id === id);
    },

    getStaffBySection: (state) => (sectionId) => {
      return state.staff.filter((s) => s.current_section?.id === sectionId);
    },
  },

  actions: {
    async fetchStaff() {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get("/api/staff/");

        // 🔥 مپ کردن داده‌ها برای هماهنگی با StaffListSerializer
        this.staff = response.data.map((staff) => ({
          ...staff,
          // اطمینان از وجود فیلدهای اصلی
          full_name:
            staff.full_name ||
            `${staff.first_name || ""} ${staff.last_name || ""}`.trim(),
          personnel_code: staff.personnel_code || "N/A",
          // اگر current_section_name نداره، null بذار
          section_name: staff.current_section_name || null,
          department_name: null, // در ListSerializer این فیلد نیست
          // اگر primary_mobile داره، به عنوان تلفن اولیه استفاده کن
          phones: staff.primary_mobile
            ? [{ phone_number: staff.primary_mobile, phone_type: "Mobile" }]
            : [],
        }));

        console.log("✅ Staff loaded:", this.staff.length);
        console.log("📦 Sample staff:", this.staff[0]);
      } catch (error) {
        this.error =
          error.response?.data?.message || "خطا در دریافت لیست پرسنل";
        console.error("❌ fetchStaff error:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchStaffDetail(id) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get(`/api/staff/${id}/`);
        this.currentStaff = response.data;
        return response.data;
      } catch (error) {
        this.error =
          error.response?.data?.message || "خطا در دریافت اطلاعات پرسنل";
        console.error("❌ fetchStaffDetail error:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createStaff(staffData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.post("/api/staff/", staffData);
        await this.fetchStaff(); // رفرش لیست
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در ایجاد پرسنل";
        console.error("❌ createStaff error:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateStaff(id, staffData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.put(`/api/staff/${id}/`, staffData);
        await this.fetchStaff(); // رفرش لیست
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در ویرایش پرسنل";
        console.error("❌ updateStaff error:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteStaff(id) {
      this.loading = true;
      this.error = null;
      try {
        await apiClient.delete(`/api/staff/${id}/`);
        await this.fetchStaff(); // رفرش لیست
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در حذف پرسنل";
        console.error("❌ deleteStaff error:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async transferStaff(staffId, transferData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.post("/api/staff/transfer/", {
          staff_id: staffId,
          ...transferData,
        });
        await this.fetchStaff(); // رفرش لیست
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "خطا در جابجایی پرسنل";
        console.error("❌ transferStaff error:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    clearCurrentStaff() {
      this.currentStaff = null;
    },

    clearError() {
      this.error = null;
    },
  },
});
