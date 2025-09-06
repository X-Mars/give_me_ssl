import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export type ThemeMode = 'light' | 'dark' | 'auto'

export const useThemeStore = defineStore('theme', () => {
  // 从localStorage获取保存的主题，默认为auto
  const theme = ref<ThemeMode>((localStorage.getItem('theme') as ThemeMode) || 'auto')
  
  // 检测系统主题偏好
  const prefersDark = ref(window.matchMedia('(prefers-color-scheme: dark)').matches)
  
  // 计算当前实际应用的主题
  const currentTheme = computed(() => {
    if (theme.value === 'auto') {
      return prefersDark.value ? 'dark' : 'light'
    }
    return theme.value
  })
  
  // 应用主题到DOM
  function applyTheme() {
    const root = document.documentElement
    const isDark = currentTheme.value === 'dark'
    
    if (isDark) {
      root.classList.add('dark-theme')
      root.classList.remove('light-theme')
    } else {
      root.classList.add('light-theme')
      root.classList.remove('dark-theme')
    }
    
    // 保存到localStorage
    localStorage.setItem('theme', theme.value)
    
    // 触发主题变更事件
    window.dispatchEvent(new CustomEvent('theme-changed', { 
      detail: { theme: currentTheme.value } 
    }))
  }
  
  // 设置主题
  function setTheme(newTheme: ThemeMode) {
    theme.value = newTheme
    applyTheme()
  }
  
  // 切换主题
  function toggleTheme() {
    const themes: ThemeMode[] = ['light', 'dark', 'auto']
    const currentIndex = themes.indexOf(theme.value)
    const nextIndex = (currentIndex + 1) % themes.length
    setTheme(themes[nextIndex])
  }
  
  // 监听系统主题变化
  function initThemeListener() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      prefersDark.value = e.matches
      if (theme.value === 'auto') {
        applyTheme()
      }
    })
  }
  
  // 初始化主题
  function initTheme() {
    initThemeListener()
    applyTheme()
  }
  
  return {
    theme,
    currentTheme,
    setTheme,
    toggleTheme,
    initTheme,
    applyTheme
  }
})
