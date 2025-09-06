import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '../stores/auth'
import { clearTokens } from '../utils/http'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'nav.dashboard',
        icon: 'Grid',
        showInMenu: true,
        order: 1
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        title: 'nav.login',
        showInMenu: false
      }
    },
    {
      path: '/certificates',
      name: 'certificates',
      component: () => import('../views/CertificatesView.vue'),
      meta: {
        title: 'nav.certificates',
        icon: 'Document',
        showInMenu: true,
        order: 2
      }
    },
    {
      path: '/providers',
      name: 'providers',
      component: () => import('../views/ProvidersView.vue'),
      meta: {
        title: 'nav.providers',
        icon: 'Key',
        showInMenu: true,
        order: 3
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
      meta: {
        title: 'nav.settings',
        icon: 'Tools',
        showInMenu: true,
        order: 4
      }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      meta: {
        title: 'nav.about',
        icon: 'InfoFilled',
        showInMenu: true,
        order: 5
      }
    },
  ],
})

router.beforeEach(async (to, _from, next) => {
  const auth = useAuthStore()
  const publicPages = new Set(['login'])
  if (!auth.user && localStorage.getItem('access_token')) {
    try { await auth.fetchUser() } catch { auth.logout(); clearTokens() }
  }
  if (!auth.user && !publicPages.has(String(to.name))) return next({ name: 'login' })
  if (auth.user && to.name === 'login') return next({ name: 'home' })
  next()
})

export default router

