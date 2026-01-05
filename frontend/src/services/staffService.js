// src/services/staffService.js
import axios from "@/api/axios";

export default {
  // لیست پرسنل
  async getAll(params = {}) {
    const response = await axios.get("/api/staff/", { params });
    return response;
  },

  // جزئیات یک پرسنل
  async getById(id) {
    const response = await axios.get(`/api/staff/${id}/`);
    return response;
  },

  // ایجاد پرسنل جدید
  async create(data) {
    const response = await axios.post("/api/staff/", data);
    return response;
  },

  // ویرایش پرسنل
  async update(id, data) {
    const response = await axios.put(`/api/staff/${id}/`, data);
    return response;
  },

  // حذف پرسنل
  async delete(id) {
    const response = await axios.delete(`/api/staff/${id}/`);
    return response;
  },

  // 🔍 جستجوی کلی در دفترچه تلفن
  async search(query) {
    const response = await axios.get("/api/phonebook/search/", {
      params: { q: query },
    });
    return response;
  },

  // تلفن‌های یک پرسنل
  async getPhones(staffId) {
    const response = await axios.get(`/api/staff/${staffId}/phones/`);
    return response;
  },

  // افزودن شماره تلفن
  async addPhone(staffId, phoneData) {
    const response = await axios.post(
      `/api/staff/${staffId}/add_phone/`,
      phoneData
    );
    return response;
  },

  // پرسنل فعال
  async getActive() {
    const response = await axios.get("/api/staff/active/");
    return response;
  },
};
