<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="hospital-logo">🏥</div>
          <h1>دفترچه تلفن بیمارستان</h1>
          <p>ورود به سیستم مدیریت</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">نام کاربری  👤</label>
            <div class="input-wrapper">
             
              <input
                id="username"
                v-model="credentials.username"
                type="text"
                class="form-control"
                placeholder="نام کاربری خود را وارد کنید"
                required
                autocomplete="username"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="password">رمز عبور 🔒</label>
            <div class="input-wrapper">
             
              <input
                id="password"
                v-model="credentials.password"
                type="password"
                class="form-control"
                placeholder="رمز عبور خود را وارد کنید"
                required
                autocomplete="current-password"
              />
            </div>
          </div>

          <div v-if="error" class="alert alert-error">
            ❌ {{ error }}
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            <span v-if="loading">در حال ورود...</span>
            <span v-else>ورود به سیستم</span>
          </button>

          <!-- <div class="login-info">
            <p>برای تست از این اطلاعات استفاده کنید:</p>
            <p><strong>نام کاربری:</strong> admin</p>
            <p><strong>رمز عبور:</strong> admin123</p>
          </div> -->
        </form>

        <div class="login-footer">
          <p>© 2026 بیمارستان - تمامی حقوق محفوظ است</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const credentials = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(credentials.value.username, credentials.value.password)
    router.push({ name: 'home' })
  } catch (err) {
    console.error('Login error:', err)
    if (err.response?.status === 401) {
      error.value = 'نام کاربری یا رمز عبور اشتباه است'
    } else if (err.response?.status === 400) {
      error.value = 'لطفاً نام کاربری و رمز عبور را وارد کنید'
    } else {
      error.value = 'خطا در اتصال به سرور. لطفاً دوباره تلاش کنید'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e3f2fd, #f4f6f8);
}

.login-container {
  width: 100%;
  max-width: 420px;
  padding: 1rem;
}

.login-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  padding: 2rem;
}

.login-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.hospital-logo {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.login-header h1 {
  font-size: 1.3rem;
  margin-bottom: 0.25rem;
}

.login-header p {
  font-size: 0.85rem;
  color: #6b7a8c;
}

/* ===== Form ===== */
.login-form {
  margin-top: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
  color: #4a5a6a;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1rem;
  opacity: 0.6;
}

.form-control {
  width: 100%;
  padding: 0.7rem 0.75rem 0.7rem 2.2rem;
  border-radius: 8px;
  border: 1px solid #dcdfe3;
  font-size: 0.9rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-control:focus {
  border-color: #1e88e5;
  box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.15);
}

/* ===== Info Box ===== */
.login-info {
  margin-top: 1.25rem;
  padding: 0.75rem;
  background: #f8f9fb;
  border-radius: 8px;
  font-size: 0.75rem;
  color: #5f6c7b;
}

.login-info p {
  margin-bottom: 0.25rem;
}

/* ===== Footer ===== */
.login-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.7rem;
  color: #9aa6b2;
}


</style>
