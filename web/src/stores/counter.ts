import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})

export const useUserStore = defineStore('user', () => {
  const user = ref<unknown>(null)
  const userInfo = ref<{ username?: string; email?: string } | null>(null)
  const isLoggedIn = computed(() => !!user.value)
  
  function login(userData: unknown) {
    user.value = userData
    // Set default userInfo if not provided
    if (userData && typeof userData === 'object' && 'username' in userData) {
      userInfo.value = userData as { username?: string; email?: string }
    } else {
      userInfo.value = { username: 'User' }
    }
  }
  
  function logout() {
    user.value = null
    userInfo.value = null
  }

  return { user, userInfo, isLoggedIn, login, logout }
})
