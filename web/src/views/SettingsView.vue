<template>
  <div class="settings-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title gradient-text">System Settings</h1>
        <p class="page-subtitle">Configure system preferences and behavior</p>
      </div>
      <div class="header-actions">
        <el-button 
          type="primary" 
          class="btn-gradient"
          @click="saveAllSettings"
          :loading="saving"
        >
          <el-icon><Check /></el-icon>
          Save All Changes
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
            General Settings
          </h3>
          <p class="section-description">Basic system configuration</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.general" label-width="200px">
            <el-form-item label="System Name">
              <el-input 
                v-model="settings.general.system_name"
                placeholder="SSL Certificate Manager"
              />
            </el-form-item>
            
            <el-form-item label="Default Language">
              <el-select v-model="settings.general.default_language">
                <el-option label="English" value="en" />
                <el-option label="中文" value="zh" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="Timezone">
              <el-select v-model="settings.general.timezone" filterable>
                <el-option 
                  v-for="tz in timezones"
                  :key="tz.value"
                  :label="tz.label"
                  :value="tz.value"
                />
              </el-select>
            </el-form-item>
            
            <el-form-item label="Theme">
              <el-radio-group v-model="settings.general.theme">
                <el-radio value="light">Light</el-radio>
                <el-radio value="dark">Dark</el-radio>
                <el-radio value="auto">Auto</el-radio>
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
            Certificate Settings
          </h3>
          <p class="section-description">Default certificate behavior and preferences</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.certificates" label-width="200px">
            <el-form-item label="Auto Renewal">
              <el-switch 
                v-model="settings.certificates.auto_renewal_enabled"
                active-text="Enabled"
                inactive-text="Disabled"
              />
              <div class="setting-hint">
                Automatically renew certificates before expiration
              </div>
            </el-form-item>
            
            <el-form-item label="Renewal Buffer Days">
              <el-input-number 
                v-model="settings.certificates.renewal_buffer_days"
                :min="1"
                :max="90"
                controls-position="right"
              />
              <div class="setting-hint">
                Start renewal this many days before expiration
              </div>
            </el-form-item>
            
            <el-form-item label="Default Provider">
              <el-select 
                v-model="settings.certificates.default_provider"
                placeholder="Select default provider"
              >
                <el-option label="Let's Encrypt" value="letsencrypt" />
                <el-option label="ZeroSSL" value="zerossl" />
                <el-option label="Manual" value="manual" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="Key Size">
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
            Notification Settings
          </h3>
          <p class="section-description">Configure alerts and notifications</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.notifications" label-width="200px">
            <el-form-item label="Email Notifications">
              <el-switch 
                v-model="settings.notifications.email_enabled"
                active-text="Enabled"
                inactive-text="Disabled"
              />
            </el-form-item>
            
            <el-form-item 
              label="SMTP Server"
              v-if="settings.notifications.email_enabled"
            >
              <el-input 
                v-model="settings.notifications.smtp_host"
                placeholder="smtp.example.com"
              />
            </el-form-item>
            
            <el-form-item 
              label="SMTP Port"
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
              label="Username"
              v-if="settings.notifications.email_enabled"
            >
              <el-input 
                v-model="settings.notifications.smtp_username"
                placeholder="your@email.com"
              />
            </el-form-item>
            
            <el-form-item 
              label="Password"
              v-if="settings.notifications.email_enabled"
            >
              <el-input 
                v-model="settings.notifications.smtp_password"
                type="password"
                show-password
                placeholder="SMTP password"
              />
            </el-form-item>
            
            <el-form-item label="Expiry Notifications">
              <el-switch 
                v-model="settings.notifications.expiry_notifications"
                active-text="Enabled"
                inactive-text="Disabled"
              />
              <div class="setting-hint">
                Send notifications when certificates are about to expire
              </div>
            </el-form-item>
            
            <el-form-item label="Success Notifications">
              <el-switch 
                v-model="settings.notifications.success_notifications"
                active-text="Enabled"
                inactive-text="Disabled"
              />
              <div class="setting-hint">
                Send notifications when certificates are successfully renewed
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
            Security Settings
          </h3>
          <p class="section-description">Authentication and access control</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.security" label-width="200px">
            <el-form-item label="Session Timeout">
              <el-select v-model="settings.security.session_timeout">
                <el-option label="1 hour" :value="3600" />
                <el-option label="4 hours" :value="14400" />
                <el-option label="8 hours" :value="28800" />
                <el-option label="24 hours" :value="86400" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="Force HTTPS">
              <el-switch 
                v-model="settings.security.force_https"
                active-text="Enabled"
                inactive-text="Disabled"
              />
              <div class="setting-hint">
                Redirect all HTTP requests to HTTPS
              </div>
            </el-form-item>
            
            <el-form-item label="API Rate Limiting">
              <el-switch 
                v-model="settings.security.rate_limiting_enabled"
                active-text="Enabled"
                inactive-text="Disabled"
              />
            </el-form-item>
            
            <el-form-item 
              label="Requests per minute"
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
            Backup & Storage
          </h3>
          <p class="section-description">Data backup and storage configuration</p>
        </div>
        
        <div class="section-content">
          <el-form :model="settings.backup" label-width="200px">
            <el-form-item label="Auto Backup">
              <el-switch 
                v-model="settings.backup.auto_backup_enabled"
                active-text="Enabled"
                inactive-text="Disabled"
              />
            </el-form-item>
            
            <el-form-item 
              label="Backup Frequency"
              v-if="settings.backup.auto_backup_enabled"
            >
              <el-select v-model="settings.backup.backup_frequency">
                <el-option label="Daily" value="daily" />
                <el-option label="Weekly" value="weekly" />
                <el-option label="Monthly" value="monthly" />
              </el-select>
            </el-form-item>
            
            <el-form-item 
              label="Backup Retention"
              v-if="settings.backup.auto_backup_enabled"
            >
              <el-input-number 
                v-model="settings.backup.backup_retention_days"
                :min="7"
                :max="365"
                controls-position="right"
              />
              <div class="setting-hint">
                Number of days to keep backup files
              </div>
            </el-form-item>
            
            <el-form-item label="Storage Path">
              <el-input 
                v-model="settings.backup.storage_path"
                placeholder="/var/backups/ssl-manager"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button @click="createBackup" :loading="creatingBackup">
                <el-icon><Download /></el-icon>
                Create Backup Now
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Check, Setting, Document, Bell, Lock, FolderOpened, Download
} from '@element-plus/icons-vue'
import { apiFetch } from '../utils/http'

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

const settings = reactive({
  general: {
    system_name: 'SSL Certificate Manager',
    default_language: 'en',
    timezone: 'UTC',
    theme: 'light'
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
async function loadSettings() {
  try {
    const result = await apiFetch<SettingsData>('/system-settings/')
    if (result.code === 0 && result.data) {
      // Merge loaded settings with defaults
      Object.assign(settings, result.data)
    }
  } catch (error) {
    console.error('Load settings error:', error)
    // Use default settings if loading fails
  }
}

async function saveAllSettings() {
  saving.value = true
  try {
    const result = await apiFetch('/system-settings/', {
      method: 'POST',
      body: JSON.stringify(settings)
    })
    
    if (result.code === 0) {
      ElMessage.success('Settings saved successfully')
    } else {
      ElMessage.error(result.message || 'Failed to save settings')
    }
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
    const result = await apiFetch('/system-settings/backup/', {
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
  max-width: 1000px;
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
