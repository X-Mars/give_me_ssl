import { createI18n } from 'vue-i18n'
import en from '../i18n/locales/en-US.json'
import zh from '../i18n/locales/zh-CN.json'

export type Locale = 'zh-CN' | 'en-US'

// 检测浏览器语言
function getBrowserLanguage(): Locale {
  const browserLang = navigator.language || navigator.languages[0]
  
  // 支持的语言列表
  const supportedLocales: Locale[] = ['zh-CN', 'en-US']
  
  // 完全匹配
  if (supportedLocales.includes(browserLang as Locale)) {
    return browserLang as Locale
  }
  
  // 部分匹配（例如 zh 匹配 zh-CN）
  const langCode = browserLang.split('-')[0]
  const matchedLocale = supportedLocales.find(locale => 
    locale.startsWith(langCode)
  )
  
  // 如果找到匹配的语言，返回匹配的语言，否则返回英文
  return matchedLocale || 'en-US'
}

// 从 localStorage 获取保存的语言，或使用浏览器检测的语言
function getStoredLanguage(): Locale {
  const stored = localStorage.getItem('preferred-language')
  if (stored && ['zh-CN', 'en-US'].includes(stored)) {
    return stored as Locale
  }
  return getBrowserLanguage()
}

const messages = {
  'zh-CN': zh,
  'en-US': en
}

export const i18n = createI18n({
  legacy: false, // 使用 Composition API
  locale: getStoredLanguage(),
  fallbackLocale: 'en-US',
  messages,
  globalInjection: true, // 全局注入 $t
  allowComposition: true // 允许 composition API 和 legacy API 同时使用
})

// 监听语言变化，保存到 localStorage
export function setLanguage(locale: Locale) {
  if (['zh-CN', 'en-US'].includes(locale)) {
    i18n.global.locale.value = locale
    localStorage.setItem('preferred-language', locale)
    
    // 更新 HTML lang 属性
    document.documentElement.lang = locale
  }
}

// 获取当前语言
export function getCurrentLanguage(): Locale {
  return i18n.global.locale.value as Locale
}

// 获取支持的语言列表
export function getSupportedLanguages() {
  return [
    { value: 'zh-CN' as const, label: '中文' },
    { value: 'en-US' as const, label: 'English' }
  ]
}

// 初始化时设置 HTML lang 属性
document.documentElement.lang = getStoredLanguage()
