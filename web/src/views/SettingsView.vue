<template>
  <div class="settings-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title gradient-text">{{ $t('settings.title') }}</h1>
        <p class="page-subtitle">{{ $t('settings.subtitle') }}</p>
      </div>
      <div class="header-actions">
        <el-button 
          type="primary" 
          class="btn-gradient"
          @click="saveAllSettings"
          :loading="saving"
        >
          <el-icon><Check /></el-icon>
          {{ $t('settings.saveAll') }}
        </el-button>
      </div>
    </div>

    <!-- Settings Sections -->
    <div class="settings-container">
      <!-- General Settings -->
      <div class="settings-section glass-card">
        <div class="section-header">
          <h3 class="section-title">
            <el-icon><Setting /></el-icon>
            {{ $t('settings.general') }}
          </h3>
          <p class="section-description">{{ $t('settings.generalDesc') }}</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.general" label-width="200px">
            <el-form-item :label="$t('settings.systemName')">
              <el-input 
                v-model="settings.general.system_name"
                :placeholder="$t('settings.systemNamePlaceholder')"
              />
            </el-form-item>
            
            <el-form-item :label="$t('settings.defaultLanguage')">
              <el-select 
                v-model="settings.general.default_language"
                @change="handleLanguageChange"
              >
                <el-option 
                  v-for="lang in supportedLanguages"
                  :key="lang.value"
                  :label="lang.label"
                  :value="lang.value"
                />
              </el-select>
            </el-form-item>
            
            <el-form-item :label="$t('settings.timezone')">
              <el-select v-model="settings.general.timezone" filterable>
                <el-option 
                  v-for="tz in timezones"
                  :key="tz.value"
                  :label="tz.label"
                  :value="tz.value"
                />
              </el-select>
            </el-form-item>
            
            <el-form-item :label="$t('settings.theme')">
              <el-radio-group v-model="settings.general.theme" @change="handleThemeChange">
                <el-radio value="light">{{ $t('settings.light') }}</el-radio>
                <el-radio value="dark">{{ $t('settings.dark') }}</el-radio>
                <el-radio value="auto">{{ $t('settings.auto') }}</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- Certificate Settings -->
      <div class="settings-section glass-card">
        <div class="section-header">
          <h3 class="section-title">
            <el-icon><Document /></el-icon>
            {{ $t('settings.certificates') }}
          </h3>
          <p class="section-description">{{ $t('settings.certificatesDesc') }}</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.certificates" label-width="200px">
            <el-form-item :label="$t('settings.autoRenewal')">
              <el-switch 
                v-model="settings.certificates.auto_renewal_enabled"
                :active-text="$t('common.enabled')"
                :inactive-text="$t('common.disabled')"
              />
              <div class="setting-hint">
                {{ $t('settings.autoRenewalHint') }}
              </div>
            </el-form-item>
            
            <el-form-item :label="$t('settings.renewalBufferDays')">
              <el-input-number 
                v-model="settings.certificates.renewal_buffer_days"
                :min="1"
                :max="90"
                controls-position="right"
              />
              <div class="setting-hint">
                {{ $t('settings.renewalBufferHint') }}
              </div>
            </el-form-item>
            
            <el-form-item :label="$t('settings.defaultProvider')">
              <el-select 
                v-model="settings.certificates.default_provider"
                :placeholder="$t('settings.selectProvider')"
              >
                <el-option label="Let's Encrypt" value="letsencrypt" />
                <el-option label="ZeroSSL" value="zerossl" />
                <el-option :label="$t('settings.manual')" value="manual" />
              </el-select>
            </el-form-item>
            
            <el-form-item :label="$t('settings.keySize')">
              <el-select v-model="settings.certificates.default_key_size">
                <el-option label="2048 bits" :value="2048" />
                <el-option label="4096 bits" :value="4096" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- Notification Settings -->
      <div class="settings-section glass-card">
        <div class="section-header">
          <h3 class="section-title">
            <el-icon><Bell /></el-icon>
            {{ $t('settings.notifications') }}
          </h3>
          <p class="section-description">{{ $t('settings.notificationsDesc') }}</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.notifications" label-width="200px">
            <el-form-item :label="$t('settings.emailNotifications')">
              <el-switch 
                v-model="settings.notifications.email_enabled"
                :active-text="$t('common.enabled')"
                :inactive-text="$t('common.disabled')"
              />
            </el-form-item>
            
            <el-form-item 
              :label="$t('settings.smtpServer')"
              v-if="settings.notifications.email_enabled"
            >
              <el-input 
                v-model="settings.notifications.smtp_host"
                placeholder="smtp.example.com"
              />
            </el-form-item>
            
            <el-form-item 
              :label="$t('settings.smtpPort')"
              v-if="settings.notifications.email_enabled"
            >
              <el-input-number 
                v-model="settings.notifications.smtp_port"
                :min="1"
                :max="65535"
                controls-position="right"
              />
            </el-form-item>
            
            <el-form-item 
              :label="$t('settings.username')"
              v-if="settings.notifications.email_enabled"
            >
              <el-input 
                v-model="settings.notifications.smtp_username"
                placeholder="your@email.com"
              />
            </el-form-item>
            
            <el-form-item 
              :label="$t('settings.password')"
              v-if="settings.notifications.email_enabled"
            >
              <el-input 
                v-model="settings.notifications.smtp_password"
                type="password"
                show-password
                :placeholder="$t('settings.smtpPassword')"
              />
            </el-form-item>
            
            <el-form-item :label="$t('settings.expiryNotifications')">
              <el-switch 
                v-model="settings.notifications.expiry_notifications"
                :active-text="$t('common.enabled')"
                :inactive-text="$t('common.disabled')"
              />
              <div class="setting-hint">
                {{ $t('settings.expiryNotificationsHint') }}
              </div>
            </el-form-item>
            
            <el-form-item :label="$t('settings.successNotifications')">
              <el-switch 
                v-model="settings.notifications.success_notifications"
                :active-text="$t('common.enabled')"
                :inactive-text="$t('common.disabled')"
              />
              <div class="setting-hint">
                {{ $t('settings.successNotificationsHint') }}
              </div>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- Security Settings -->
      <div class="settings-section glass-card">
        <div class="section-header">
          <h3 class="section-title">
            <el-icon><Lock /></el-icon>
            {{ $t('settings.security') }}
          </h3>
          <p class="section-description">{{ $t('settings.securityDesc') }}</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.security" label-width="200px">
            <el-form-item :label="$t('settings.sessionTimeout')">
              <el-select v-model="settings.security.session_timeout">
                <el-option :label="$t('settings.oneHour')" :value="3600" />
                <el-option :label="$t('settings.fourHours')" :value="14400" />
                <el-option :label="$t('settings.eightHours')" :value="28800" />
                <el-option :label="$t('settings.twentyFourHours')" :value="86400" />
              </el-select>
            </el-form-item>
            
            <el-form-item :label="$t('settings.forceHttps')">
              <el-switch 
                v-model="settings.security.force_https"
                :active-text="$t('common.enabled')"
                :inactive-text="$t('common.disabled')"
              />
              <div class="setting-hint">
                {{ $t('settings.forceHttpsHint') }}
              </div>
            </el-form-item>
            
            <el-form-item :label="$t('settings.apiRateLimiting')">
              <el-switch 
                v-model="settings.security.rate_limiting_enabled"
                :active-text="$t('common.enabled')"
                :inactive-text="$t('common.disabled')"
              />
            </el-form-item>
            
            <el-form-item 
              :label="$t('settings.requestsPerMinute')"
              v-if="settings.security.rate_limiting_enabled"
            >
              <el-input-number 
                v-model="settings.security.rate_limit_requests"
                :min="10"
                :max="1000"
                controls-position="right"
              />
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- Backup Settings -->
      <div class="settings-section glass-card">
        <div class="section-header">
          <h3 class="section-title">
            <el-icon><FolderOpened /></el-icon>
            {{ $t('settings.backup') }}
          </h3>
          <p class="section-description">{{ $t('settings.backupDesc') }}</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.backup" label-width="200px">
            <el-form-item :label="$t('settings.autoBackup')">
              <el-switch 
                v-model="settings.backup.auto_backup_enabled"
                :active-text="$t('common.enabled')"
                :inactive-text="$t('common.disabled')"
              />
            </el-form-item>
            
            <el-form-item 
              :label="$t('settings.backupFrequency')"
              v-if="settings.backup.auto_backup_enabled"
            >
              <el-select v-model="settings.backup.backup_frequency">
                <el-option :label="$t('settings.daily')" value="daily" />
                <el-option :label="$t('settings.weekly')" value="weekly" />
                <el-option :label="$t('settings.monthly')" value="monthly" />
              </el-select>
            </el-form-item>
            
            <el-form-item 
              :label="$t('settings.backupRetention')"
              v-if="settings.backup.auto_backup_enabled"
            >
              <el-input-number 
                v-model="settings.backup.backup_retention_days"
                :min="7"
                :max="365"
                controls-position="right"
              />
              <div class="setting-hint">
                {{ $t('settings.backupRetentionHint') }}
              </div>
            </el-form-item>
            
            <el-form-item :label="$t('settings.storagePath')">
              <el-input 
                v-model="settings.backup.storage_path"
                placeholder="/var/backups/ssl-manager"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button @click="createBackup" :loading="creatingBackup">
                <el-icon><Download /></el-icon>
                {{ $t('settings.createBackupNow') }}
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import {
  Check, Setting, Document, Bell, Lock, FolderOpened, Download
} from '@element-plus/icons-vue'
import { apiFetch } from '../utils/http'
import { setLanguage, getCurrentLanguage, getSupportedLanguages, type Locale } from '../plugins/i18n'
import { useThemeStore, type ThemeMode } from '../stores/theme'

const { t, locale } = useI18n() // 添加 locale 引用以确保响应性
const themeStore = useThemeStore() // 添加主题store引用

interface PlatformSetting {
  id: number
  key: string
  value: string
  description: string
  created_at: string
  updated_at: string
}

interface SettingsData {
  general: {
    system_name: string
    default_language: string
    timezone: string
    theme: string
  }
  certificates: {
    auto_renewal_enabled: boolean
    renewal_buffer_days: number
    default_provider: string
    default_key_size: number
  }
  notifications: {
    email_enabled: boolean
    smtp_host: string
    smtp_port: number
    smtp_username: string
    smtp_password: string
    expiry_notifications: boolean
    success_notifications: boolean
  }
  security: {
    session_timeout: number
    force_https: boolean
    rate_limiting_enabled: boolean
    rate_limit_requests: number
  }
  backup: {
    auto_backup_enabled: boolean
    backup_frequency: string
    backup_retention_days: number
    storage_path: string
  }
}

// State
const saving = ref(false)
const creatingBackup = ref(false)

// 支持的语言列表
const supportedLanguages = getSupportedLanguages()

const settings = reactive({
  general: {
    system_name: 'SSL Certificate Manager',
    default_language: getCurrentLanguage(), // 使用当前语言作为默认值
    timezone: 'UTC',
    theme: themeStore.theme // 从主题store获取当前主题
  },
  certificates: {
    auto_renewal_enabled: true,
    renewal_buffer_days: 30,
    default_provider: 'letsencrypt',
    default_key_size: 2048
  },
  notifications: {
    email_enabled: false,
    smtp_host: '',
    smtp_port: 587,
    smtp_username: '',
    smtp_password: '',
    expiry_notifications: true,
    success_notifications: true
  },
  security: {
    session_timeout: 28800,
    force_https: true,
    rate_limiting_enabled: true,
    rate_limit_requests: 100
  },
  backup: {
    auto_backup_enabled: false,
    backup_frequency: 'weekly',
    backup_retention_days: 30,
    storage_path: '/var/backups/ssl-manager'
  }
})

// 监听语言变化，同步到设置表单
watch(locale, (newLocale) => {
  settings.general.default_language = String(newLocale) as Locale
}, { immediate: true })

// 监听主题store变化，同步到设置表单
watch(() => themeStore.theme, (newTheme) => {
  settings.general.theme = newTheme
}, { immediate: true })

const timezones = [
  { label: 'UTC', value: 'UTC' },
  { label: 'America/New_York', value: 'America/New_York' },
  { label: 'America/Los_Angeles', value: 'America/Los_Angeles' },
  { label: 'Europe/London', value: 'Europe/London' },
  { label: 'Europe/Paris', value: 'Europe/Paris' },
  { label: 'Asia/Shanghai', value: 'Asia/Shanghai' },
  { label: 'Asia/Tokyo', value: 'Asia/Tokyo' }
]

// Methods
// 处理主题变更
function handleThemeChange(newTheme: string) {
  // 立即应用主题变更
  themeStore.setTheme(newTheme as ThemeMode)
  
  // 显示成功消息
  ElMessage.success(t('settings.themeChanged'))
}

// 处理语言变更
function handleLanguageChange(newLanguage: string) {
  // 映射简短语言代码到完整代码
  const languageMap: Record<string, Locale> = {
    'zh': 'zh-CN',
    'zh-CN': 'zh-CN',
    'en': 'en-US',
    'en-US': 'en-US'
  }
  
  const mappedLanguage = languageMap[newLanguage] || 'en-US'
  
  // 立即切换应用语言
  setLanguage(mappedLanguage)
  
  // 显示成功消息（会使用新语言显示）
  ElMessage.success(t('settings.languageChanged'))
}

async function loadSettings() {
  try {
    const result = await apiFetch<PlatformSetting[]>('/platform-settings/')
    if (result.code === 0 && Array.isArray(result.data)) {
      // Convert key-value pairs to structured settings
      const loadedSettings: Record<string, unknown> = {}
      result.data.forEach((setting: PlatformSetting) => {
        const keys = setting.key.split('.')
        let current: Record<string, unknown> = loadedSettings
        for (let i = 0; i < keys.length - 1; i++) {
          if (!current[keys[i]]) {
            current[keys[i]] = {}
          }
          current = current[keys[i]] as Record<string, unknown>
        }
        try {
          current[keys[keys.length - 1]] = JSON.parse(setting.value)
        } catch {
          current[keys[keys.length - 1]] = setting.value
        }
      })
      
      // Merge loaded settings with defaults
      Object.assign(settings, loadedSettings)
      
      // 同步当前语言到设置中
      settings.general.default_language = getCurrentLanguage()
    }
  } catch (error) {
    console.error('Load settings error:', error)
    // Use default settings if loading fails
  }
}

async function saveAllSettings() {
  saving.value = true
  try {
    // Convert structured settings to key-value pairs
    const settingsArray: Array<{key: string, value: string}> = []
    
    function flattenSettings(obj: Record<string, unknown>, prefix = '') {
      for (const [key, value] of Object.entries(obj)) {
        const fullKey = prefix ? `${prefix}.${key}` : key
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
          flattenSettings(value as Record<string, unknown>, fullKey)
        } else {
          settingsArray.push({
            key: fullKey,
            value: JSON.stringify(value)
          })
        }
      }
    }
    
    flattenSettings(settings)
    
    // First get existing settings to check which ones to update vs create
    const existingResult = await apiFetch<PlatformSetting[]>('/platform-settings/')
    const existingKeys = new Set(
      Array.isArray(existingResult.data) ? existingResult.data.map(s => s.key) : []
    )
    
    // Save each setting individually
    for (const setting of settingsArray) {
      try {
        if (existingKeys.has(setting.key)) {
          // Update existing setting - find the ID first
          const existing = (existingResult.data as PlatformSetting[]).find(s => s.key === setting.key)
          if (existing) {
            await apiFetch(`/platform-settings/${existing.id}/`, {
              method: 'PUT',
              body: JSON.stringify({
                key: setting.key,
                value: setting.value,
                description: ''
              })
            })
          }
        } else {
          // Create new setting
          await apiFetch('/platform-settings/', {
            method: 'POST',
            body: JSON.stringify({
              key: setting.key,
              value: setting.value,
              description: ''
            })
          })
        }
      } catch (error) {
        console.error(`Failed to save setting ${setting.key}:`, error)
      }
    }
    
    ElMessage.success('Settings saved successfully')
  } catch (error) {
    ElMessage.error('Failed to save settings')
    console.error('Save settings error:', error)
  } finally {
    saving.value = false
  }
}

async function createBackup() {
  creatingBackup.value = true
  try {
    const result = await apiFetch('/platform-settings/backup/', {
      method: 'POST'
    })
    
    if (result.code === 0) {
      ElMessage.success('Backup created successfully')
    } else {
      ElMessage.error(result.message || 'Failed to create backup')
    }
  } catch (error) {
    ElMessage.error('Failed to create backup')
    console.error('Create backup error:', error)
  } finally {
    creatingBackup.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-xl);
}

.header-content h1 {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 var(--space-xs) 0;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 16px;
  margin: 0;
}

.settings-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.settings-section {
  padding: var(--space-xl);
  border-radius: var(--radius-xl);
}

.section-header {
  margin-bottom: var(--space-lg);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--border-light);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-sm) 0;
}

.section-description {
  color: var(--text-secondary);
  margin: 0;
}

.section-content {
  padding-left: var(--space-lg);
}

.setting-hint {
  font-size: 12px;
  color: var(--text-light);
  margin-top: var(--space-xs);
}

/* Form Styling */
:deep(.el-form-item) {
  margin-bottom: var(--space-lg);
}

:deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  background-color: var(--bg-light);
  border: 1px solid var(--border-light);
}

:deep(.el-select .el-input__wrapper) {
  background-color: var(--bg-light);
}

:deep(.el-radio) {
  margin-right: var(--space-lg);
}

:deep(.el-switch) {
  margin-right: var(--space-md);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: var(--space-md);
    align-items: stretch;
  }
  
  .section-content {
    padding-left: 0;
  }
  
  :deep(.el-form-item__label) {
    text-align: left !important;
  }
}
</style>
