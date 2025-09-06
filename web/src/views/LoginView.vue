<template>
  <div class="login-container">
    
    <!-- Main Content -->
    <div class="login-content">
      <!-- Left Panel - Logo & Branding -->
      <div class="left-panel">
        <div class="branding-section">
          <div class="logo-wrapper">
            <el-icon class="logo-icon"><Lock /></el-icon>
            <h1 class="app-title">{{ $t('dashboard.title') }}</h1>
          </div>
          <p class="app-description">{{ $t('auth.systemDescription') }}</p>
          
          <!-- Features List -->
          <div class="features-list">
            <div class="feature-item">
              <el-icon class="feature-icon"><CircleCheck /></el-icon>
              <span>{{ $t('auth.feature1') }}</span>
            </div>
            <div class="feature-item">
              <el-icon class="feature-icon"><CircleCheck /></el-icon>
              <span>{{ $t('auth.feature2') }}</span>
            </div>
            <div class="feature-item">
              <el-icon class="feature-icon"><CircleCheck /></el-icon>
              <span>{{ $t('auth.feature3') }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right Panel - Login Form -->
      <div class="right-panel">
        <div class="login-card glass-card">
          <div class="login-header">
            <h2 class="login-title">{{ $t('auth.welcomeBack') }}</h2>
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
            <p class="footer-text">{{ $t('auth.footerText') }}</p>
          </div>
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
import { User, Lock, Right, CircleCheck } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const auth = useAuthStore()
const router = useRouter()
const { t } = useI18n()

const formRef = ref<FormInstance>()
const form = reactive({ username: '', password: '' })
const error = ref('')

const rules: FormRules = {
  username: [
    { required: true, message: t('auth.username') + ' is required', trigger: 'blur' },
    { min: 2, max: 50, message: 'Length should be 2 to 50', trigger: 'blur' }
  ],
  password: [
    { required: true, message: t('auth.password') + ' is required', trigger: 'blur' },
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
  /* height: 80vh; */
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-2xl);
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
  left: 60%;
  animation-delay: 2s;
}

.login-content {
  display: flex;
  width: 100%;
  height: 80vh;
  position: relative;
  z-index: 10;
  border-radius: var(--radius-2xl);
  overflow: hidden;
}

/* Left Panel */
.left-panel {
  flex: 1.4;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-2xl);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top-left-radius: var(--radius-2xl);
  border-bottom-left-radius: var(--radius-2xl);
}

.branding-section {
  max-width: 500px;
  text-align: center;
}

.logo-wrapper {
  margin-bottom: var(--space-2xl);
}

.logo-icon {
  font-size: 80px;
  color: white;
  margin: 0 auto var(--space-lg) auto;
  display: block;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.app-title {
  font-size: 48px;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
  color: white;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.app-description {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 var(--space-2xl) 0;
  line-height: 1.6;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
  text-align: left;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  color: white;
  font-size: 16px;
}

.feature-icon {
  color: var(--success-color);
  font-size: 20px;
  flex-shrink: 0;
}

/* Right Panel */
.right-panel {
  flex: 1.2;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-2xl);
  background: var(--bg-primary);
  border-top-right-radius: var(--radius-2xl);
  border-bottom-right-radius: var(--radius-2xl);
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: var(--space-2xl);
  border-radius: var(--radius-2xl);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: var(--shadow-2xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--space-sm) 0;
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
  background: var(--bg-secondary);
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
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-content {
    flex-direction: column;
  }
  
  .left-panel {
    flex: none;
    min-height: 40vh;
    padding: var(--space-xl) var(--space-lg);
  }
  
  .right-panel {
    flex: 1;
    padding: var(--space-lg);
  }
  
  .logo-icon {
    font-size: 60px;
  }
  
  .app-title {
    font-size: 32px;
  }
  
  .app-description {
    font-size: 16px;
  }
  
  .features-list {
    display: none;
  }
  
  .login-card {
    padding: var(--space-xl);
  }
  
  .login-title {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .left-panel {
    min-height: 30vh;
    padding: var(--space-lg);
  }
  
  .right-panel {
    padding: var(--space-md);
  }
  
  .login-card {
    padding: var(--space-lg);
  }
  
  .app-title {
    font-size: 28px;
  }
  
  .login-title {
    font-size: 20px;
  }
}
</style>
