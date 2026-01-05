import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./assets/main.css";
import "./config/axios"; // ✅ اضافه کردن این خط
import { useAuthStore } from "./stores/authStore";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);

// بازیابی اطلاعات authentication
const authStore = useAuthStore();
authStore.initAuth();

app.use(router);
app.mount("#app");
