import { createI18n } from 'vue-i18n'
import en from '../locales/en.json'
import zh from '../locales/zh-CN.json'

export const i18n = createI18n({
  legacy: false,
  locale: navigator.language.toLowerCase().startsWith('zh') ? 'zh-CN' : 'en',
  messages: {
    en,
    'zh-CN': zh,
  },
})
