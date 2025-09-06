import { defineStore } from 'pinia'
import { login, getMe, clearTokens } from '../utils/http'

interface User { 
  id: number
  username: string
  email: string
  avatar?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null as User | null, loading: false }),
  actions: {
    async login(username: string, password: string) {
      this.loading = true
      try {
        const res = await login(username, password)
        if (res.code === 0) {
          this.user = res.data.user
          return true
        }
        return false
      } finally {
        this.loading = false
      }
    },
    async fetchUser() {
      const res = await getMe()
      if (res.code === 0) this.user = res.data
    },
  logout() { clearTokens(); this.user = null }
  }
})
