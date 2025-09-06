import type { RouteRecordNormalized } from 'vue-router'

export interface MenuItem {
  index: string
  icon: string
  title: string
  order: number
}

export function generateMenuFromRoutes(routes: RouteRecordNormalized[]): MenuItem[] {
  return routes
    .filter(route => route.meta?.showInMenu === true)
    .sort((a, b) => {
      const orderA = typeof a.meta?.order === 'number' ? a.meta.order : 0
      const orderB = typeof b.meta?.order === 'number' ? b.meta.order : 0
      return orderA - orderB
    })
    .map(route => ({
      index: route.path,
      icon: route.meta?.icon || 'Menu',
      title: route.meta?.title || String(route.name || ''),
      order: typeof route.meta?.order === 'number' ? route.meta.order : 0
    }))
}
