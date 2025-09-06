<template>
  <div class="login-container">
    <!-- Background Pattern -->
    <div class="bg-pattern">
      <div class="floating-shapes">
        <div class="shape shape-1 floating"></div>
        <div class="shape shape-2 floating"></div>
        <div class="shape shape-3 floating"></div>
      </div>
    </div>
    
    <!-- Login Card -->
    <div class="login-card glass-card">
      <div class="login-header">
        <div class="logo-section">
          <el-icon class="logo-icon"><Lock /></el-icon>
          <h1 class="app-title gradient-text">{{ $t('dashboard.title') }}</h1>
        </div>
        <p class="login-subtitle">{{ $t('auth.pleaseLogin') }}</p>
      </div>
      
      <el-form 
        ref="formRef"
        :model="form" 
        :rules="rules"
        @submit.prevent="handleLogin"
        class="login-form"
        label-position="top"
        size="large"
      >
        <el-form-item :label="$t('auth.username')" prop="username">
          <el-input 
            v-model.trim="form.username" 
            :prefix-icon="User"
            :placeholder="$t('auth.username')"
            autocomplete="username"
            clearable
          />
        </el-form-item>
        
        <el-form-item :label="$t('auth.password')" prop="password">
          <el-input 
            v-model="form.password" 
            type="password"
            :prefix-icon="Lock"
            :placeholder="$t('auth.password')"
            show-password
            autocomplete="current-password"
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <!-- Error Alert -->
        <transition name="slide-up">
          <el-alert 
            v-if="error" 
            :title="error" 
            type="error" 
            show-icon 
            class="error-alert"
            closable
            @close="error = ''"
          />
        </transition>
        
        <!-- Login Button -->
        <el-button 
          type="primary" 
          class="login-btn btn-gradient"
          :loading="auth.loading" 
          native-type="submit"
          size="large"
        >
          <el-icon v-if="!auth.loading"><Right /></el-icon>
          {{ $t('auth.login') }}
        </el-button>
      </el-form>
      
      <!-- Footer -->
      <div class="login-footer">
        <p class="footer-text">Give Me SSL - Free SSL Certificate Management</p>
        <div class="social-login">
          <el-button circle class="social-btn" disabled>
            <el-icon><ChatDotRound /></el-icon>
          </el-button>
          <el-button circle class="social-btn" disabled>
            <el-icon><Message /></el-icon>
          </el-button>
          <el-button circle class="social-btn" disabled>
            <el-icon><Phone /></el-icon>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useI18n } from 'vue-i18n'
import { User, Lock, Right, ChatDotRound, Message, Phone } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const auth = useAuthStore()
const router = useRouter()
const { t } = useI18n()

const formRef = ref<FormInstance>()
const form = reactive({ username: '', password: '' })
const error = ref('')

const rules: FormRules = {
  username: [
    { required: true, message: t('username') + ' is required', trigger: 'blur' },
    { min: 2, max: 50, message: 'Length should be 2 to 50', trigger: 'blur' }
  ],
  password: [
    { required: true, message: t('password') + ' is required', trigger: 'blur' },
    { min: 6, message: 'Password length should be at least 6', trigger: 'blur' }
  ]
}

async function handleLogin() {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    error.value = ''
    
    const success = await auth.login(form.username, form.password)
    if (success) {
      router.push('/')
    } else {
      error.value = 'Invalid username or password'
    }
  } catch (err) {
    console.error('Login validation failed:', err)
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-lg);
  position: relative;
  overflow: hidden;
}

.bg-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.shape-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  left: -150px;
  animation-delay: 0s;
}

.shape-2 {
  width: 200px;
  height: 200px;
  top: 60%;
  right: -100px;
  animation-delay: 1s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  bottom: 20%;
  left: 20%;
  animation-delay: 2s;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: var(--space-2xl);
  position: relative;
  z-index: 10;
  border-radius: var(--radius-2xl);
}

.login-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
}

.logo-icon {
  font-size: 48px;
  color: var(--primary-color);
  padding: var(--space-md);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.app-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
}

.login-subtitle {
  color: var(--text-secondary);
  font-size: 16px;
  margin: 0;
}

.login-form {
  margin-bottom: var(--space-xl);
}

.login-form :deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 600;
  font-size: 14px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 2px solid transparent;
  transition: var(--transition);
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-color);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(255, 107, 157, 0.2);
}

.error-alert {
  margin-bottom: var(--space-lg);
  border-radius: var(--radius-lg);
}

.login-btn {
  width: 100%;
  height: 48px;
  border-radius: var(--radius-lg);
  font-size: 16px;
  font-weight: 600;
  margin-top: var(--space-lg);
  border: none;
  box-shadow: var(--shadow-lg);
  transition: var(--transition);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}

.login-btn:active {
  transform: translateY(0);
}

.login-footer {
  text-align: center;
  border-top: 1px solid var(--border-light);
  padding-top: var(--space-lg);
}

.footer-text {
  color: var(--text-light);
  font-size: 12px;
  margin: 0 0 var(--space-md) 0;
}

.social-login {
  display: flex;
  justify-content: center;
  gap: var(--space-sm);
}

.social-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  color: var(--text-light);
  transition: var(--transition);
}

.social-btn:hover {
  background: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 480px) {
  .login-container {
    padding: var(--space-md);
  }
  
  .login-card {
    padding: var(--space-xl);
  }
  
  .app-title {
    font-size: 20px;
  }
  
  .shape-1, .shape-2, .shape-3 {
    display: none;
  }
}
</style>
