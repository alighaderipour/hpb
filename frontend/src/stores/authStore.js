import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")) || null,
    token: localStorage.getItem("token") || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
  },

  actions: {
    async login(username, password) {
      try {
        console.log("🔄 در حال ارسال درخواست لاگین...");

        const response = await axios.post("/api/auth/login/", {
          username,
          password,
        });

        console.log("✅ پاسخ دریافت شد:", response.data);

        this.token = response.data.access;
        this.user = { username };

        // ذخیره در localStorage
        localStorage.setItem("token", response.data.access);
        localStorage.setItem("refresh_token", response.data.refresh);
        localStorage.setItem("user", JSON.stringify({ username }));

        // تنظیم توکن در Axios برای درخواست‌های بعدی
        axios.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;

        console.log("✅ لاگین موفقیت‌آمیز بود");
        return response.data;
      } catch (error) {
        console.error("❌ خطا در لاگین:", error);
        console.error("❌ پاسخ سرور:", error.response?.data);
        throw error;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
      delete axios.defaults.headers.common["Authorization"];
    },

    initAuth() {
      const token = localStorage.getItem("token");
      const user = localStorage.getItem("user");

      if (token && user) {
        this.token = token;
        this.user = JSON.parse(user);
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        console.log("✅ توکن از localStorage بازیابی شد");
      }
    },
  },
});
