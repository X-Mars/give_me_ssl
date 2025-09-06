<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { setLanguage, getCurrentLanguage, type Locale } from './plugins/i18n'
import { generateMenuFromRoutes } from './utils/menu'
import { 
  Menu, SwitchButton, Switch
} from '@element-plus/icons-vue'

const auth = useAuthStore()
const collapsed = ref(false)
const router = useRouter()
const { t } = useI18n()

function logout() { 
  auth.logout()
  router.push('/login') 
}

function toggleLocale() {
  const currentLang = getCurrentLanguage()
  const newLang: Locale = currentLang === 'zh-CN' ? 'en-US' : 'zh-CN'
  setLanguage(newLang)
}

const menuItems = computed(() => {
  const routes = router.getRoutes()
  return generateMenuFromRoutes(routes).map(item => ({
    index: item.index,
    icon: item.icon,
    title: t(item.title)
  }))
})
</script>

<template>
  <div class="app-container">
    <!-- Authenticated Layout -->
    <div class="layout" v-if="auth.user">
      <!-- Sidebar -->
      <aside class="sidebar" :class="{ collapsed }">
        <div class="sidebar-header">
          <div class="logo" v-if="!collapsed">
            <el-icon class="logo-icon"><Lock /></el-icon>
            <span class="logo-text gradient-text">SSL Manager</span>
          </div>
          <el-icon v-else class="logo-icon-collapsed"><Lock /></el-icon>
        </div>
        
        <nav class="sidebar-nav">
          <el-menu 
            :default-active="$route.path" 
            class="sidebar-menu" 
            router
            :collapse="collapsed"
            background-color="transparent"
            text-color="rgba(255,255,255,0.8)"
            active-text-color="#fff"
          >
            <el-menu-item 
              v-for="item in menuItems" 
              :key="item.index"
              :index="item.index"
              class="menu-item"
            >
              <el-icon><component :is="item.icon" /></el-icon>
              <span>{{ item.title }}</span>
            </el-menu-item>
          </el-menu>
        </nav>
        
        <div class="sidebar-footer">
          <el-button 
            v-if="!collapsed"
            class="logout-btn" 
            @click="logout"
            size="small"
          >
            <el-icon><SwitchButton /></el-icon>
            {{ t('nav.logout') }}
          </el-button>
          <el-button 
            v-else
            class="logout-btn-collapsed" 
            @click="logout"
            size="small"
            circle
          >
            <el-icon><SwitchButton /></el-icon>
          </el-button>
        </div>
      </aside>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Top Bar -->
        <header class="topbar glass-card">
          <div class="topbar-left">
            <el-button 
              class="collapse-btn"
              @click="collapsed = !collapsed"
              text
              circle
            >
              <el-icon><Menu /></el-icon>
            </el-button>
            <h1 class="page-title">{{ $route.meta?.title ? t($route.meta.title) : t('nav.dashboard') }}</h1>
          </div>
          
          <div class="topbar-right">
            <el-tooltip 
              :content="t('nav.switchLanguage')"
              placement="bottom"
              effect="dark"
            >
              <el-button 
                class="locale-btn"
                @click="toggleLocale"
                text
                circle
              >
                <el-icon><Switch /></el-icon>
              </el-button>
            </el-tooltip>
            
            <div class="user-info">
              <el-avatar 
                class="user-avatar" 
                :size="32"
                :src="auth.user?.avatar"
              >
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="username">{{ auth.user?.username }}</span>
            </div>
          </div>
        </header>

        <!-- Page Content -->
        <main class="page-content">
          <RouterView v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </RouterView>
        </main>
      </div>
    </div>

    <!-- Login Layout -->
    <div v-else class="login-layout">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background: var(--bg-primary);
}

.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Sidebar Styles */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, var(--secondary-color) 0%, var(--primary-color) 100%);
  color: white;
  display: flex;
  flex-direction: column;
  transition: var(--transition);
  position: relative;
  z-index: 100;
  box-shadow: var(--shadow-xl);
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  padding: var(--space-lg);
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
}

.logo-icon {
  font-size: 24px;
  color: white;
}

.logo-icon-collapsed {
  font-size: 24px;
  color: white;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: white;
}

.sidebar-nav {
  flex: 1;
  padding: var(--space-md) 0;
}

.sidebar-menu {
  border: none;
}

/* Fix icon centering when sidebar is collapsed */
.sidebar.collapsed .sidebar-menu .menu-item {
  padding: 0 !important;
  justify-content: center;
}

.sidebar.collapsed .sidebar-menu .el-menu-item {
  padding: 0 !important;
  justify-content: center;
}

.sidebar.collapsed .sidebar-menu .el-menu-item .el-icon {
  margin-right: 0 !important;
}

.menu-item {
  margin: var(--space-xs) var(--space-md);
  border-radius: var(--radius-lg);
  transition: var(--transition);
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.menu-item.is-active {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.sidebar-footer {
  padding: var(--space-lg);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-btn {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: var(--radius-lg);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.logout-btn-collapsed {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

/* Main Content Styles */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.topbar {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-lg);
  margin: var(--space-md);
  margin-bottom: 0;
  border-radius: var(--radius-xl);
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.collapse-btn {
  color: var(--primary-color);
  font-size: 18px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.locale-btn {
  color: var(--secondary-color);
  font-size: 18px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.user-avatar {
  border: 2px solid var(--primary-color);
}

.username {
  font-weight: 600;
  color: var(--text-primary);
}

.page-content {
  flex: 1;
  padding: var(--space-lg);
  overflow: auto;
}

/* Login Layout */
.login-layout {
  min-height: 100vh;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
  }
  
  .sidebar.collapsed {
    transform: translateX(0);
    width: 64px;
  }
  
  .main-content {
    width: 100%;
  }
  
  .topbar {
    margin: var(--space-sm);
    margin-bottom: 0;
  }
  
  .page-content {
    padding: var(--space-md);
  }
}
</style>
