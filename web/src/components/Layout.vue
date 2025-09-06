<template>
  <div class="layout-container">
    <!-- 侧边栏 -->
    <div class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <el-icon v-if="!sidebarCollapsed"><Lock /></el-icon>
          <span v-if="!sidebarCollapsed">SSL管理</span>
        </div>
        <el-button 
          text 
          @click="toggleSidebar"
          class="collapse-btn"
        >
          <el-icon><Fold v-if="!sidebarCollapsed" /><Expand v-else /></el-icon>
        </el-button>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        :collapse="sidebarCollapsed"
        :unique-opened="true"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Monitor /></el-icon>
          <template #title>仪表板</template>
        </el-menu-item>
        
        <el-menu-item index="/certificates">
          <el-icon><Document /></el-icon>
          <template #title>证书管理</template>
        </el-menu-item>
        
        <el-menu-item index="/deployment-targets">
          <el-icon><Setting /></el-icon>
          <template #title>部署配置</template>
        </el-menu-item>
        
        <el-menu-item index="/notifications">
          <el-icon><Bell /></el-icon>
          <template #title>通知设置</template>
        </el-menu-item>
        
        <el-menu-item index="/settings">
          <el-icon><Tools /></el-icon>
          <template #title>系统设置</template>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 顶部导航栏 -->
      <div class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="breadcrumbItems.length > 0">
              {{ breadcrumbItems[breadcrumbItems.length - 1] }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <!-- 通知图标 -->
          <el-badge :value="unreadNotifications" :hidden="unreadNotifications === 0">
            <el-button text @click="showNotifications">
              <el-icon><Bell /></el-icon>
            </el-button>
          </el-badge>
          
          <!-- 用户菜单 -->
          <el-dropdown @command="handleUserCommand">
            <div class="user-info">
              <el-avatar :size="32">
                {{ userStore.userInfo?.username?.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userStore.userInfo?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="settings">设置</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 页面内容 -->
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/counter'

const route = useRoute()
const userStore = useUserStore()

const sidebarCollapsed = ref(false)
const unreadNotifications = ref(0)

const activeMenu = computed(() => {
  return route.path
})

const breadcrumbItems = computed(() => {
  const routeMap: Record<string, string> = {
    '/dashboard': '仪表板',
    '/certificates': '证书管理',
    '/certificates/apply': '申请证书',
    '/deployment-targets': '部署配置',
    '/notifications': '通知设置',
    '/settings': '系统设置',
    '/about': '关于'
  }
  
  const currentPath = route.path
  const items = []
  
  // 处理动态路由
  if (currentPath.startsWith('/certificates/') && currentPath !== '/certificates') {
    items.push('证书管理')
    if (currentPath.includes('/apply')) {
      items.push('申请证书')
    } else {
      items.push('证书详情')
    }
  } else if (routeMap[currentPath]) {
    items.push(routeMap[currentPath])
  }
  
  return items
})

onMounted(() => {
  // TODO: 获取用户信息
  console.log('Layout component mounted')
})

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const showNotifications = () => {
  console.log('Show notifications')
}

const handleUserCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      console.log('View profile')
      break
    case 'settings':
      console.log('View settings')
      break
    case 'logout':
      console.log('Logout')
      break
  }
}
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  background: #f5f7fa;
}

.sidebar {
  width: 250px;
  background: #ffffff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  transition: width 0.3s ease;
  position: relative;
  z-index: 1000;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid #e6e6e6;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.collapse-btn {
  padding: 8px;
}

.sidebar-menu {
  border: none;
  height: calc(100vh - 60px);
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 250px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: 60px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 999;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  font-size: 14px;
  color: #333;
}

.content {
  flex: 1;
  overflow-y: auto;
  background: #f5f7fa;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1001;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.collapsed {
    width: 250px;
    transform: translateX(0);
  }
  
  .main-content {
    width: 100%;
    margin-left: 0;
  }
  
  .header {
    padding: 0 15px;
  }
  
  .username {
    display: none;
  }
}
</style>
