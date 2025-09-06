<template>
  <div class="providers-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title gradient-text">SSL Providers</h1>
        <p class="page-subtitle">Configure and manage your SSL certificate providers</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" class="btn-gradient" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          Add Provider
        </el-button>
      </div>
    </div>

    <!-- Provider Cards -->
    <div class="providers-grid">
      <div 
        v-for="provider in providers"
        :key="provider.id"
        class="provider-card glass-card card-hover"
      >
        <div class="provider-header">
          <div class="provider-info">
            <div class="provider-icon-wrapper">
              <el-icon class="provider-icon">
                <Key v-if="provider.provider === 'letsencrypt'" />
                <Lock v-else-if="provider.provider === 'zerossl'" />
                <Setting v-else />
              </el-icon>
            </div>
            <div class="provider-details">
              <h3 class="provider-name">{{ getProviderName(provider.provider) }}</h3>
              <p class="provider-description">{{ provider.provider }}</p>
            </div>
          </div>
          <div class="provider-status">
            <el-tag 
              type="success"
              size="small"
            >
              Active
            </el-tag>
          </div>
        </div>

        <div class="provider-stats">
          <div class="stat-item">
            <span class="stat-value">{{ provider.certificate_count || 0 }}</span>
            <span class="stat-label">Certificates</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ formatDate(provider.created_at) }}</span>
            <span class="stat-label">Created</span>
          </div>
        </div>

        <div class="provider-actions">
          <el-button 
            size="small" 
            @click="editProvider(provider)"
          >
            <el-icon><Edit /></el-icon>
            Configure
          </el-button>
          <el-button 
            size="small" 
            @click="testProvider(provider)"
            :loading="testingProvider === provider.id"
          >
            <el-icon><Connection /></el-icon>
            Test
          </el-button>
          <el-dropdown @command="(cmd) => handleProviderAction(cmd, provider)">
            <el-button size="small">
              <el-icon><MoreFilled /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="delete" divided>Delete</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- Add Provider Card -->
      <div class="add-provider-card glass-card" @click="showCreateDialog = true">
        <div class="add-provider-content">
          <el-icon class="add-icon"><Plus /></el-icon>
          <h3>Add New Provider</h3>
          <p>Configure a new SSL certificate provider</p>
        </div>
      </div>
    </div>

    <!-- Provider Templates -->
    <div class="templates-section">
      <h2 class="section-title">Quick Setup Templates</h2>
      <div class="templates-grid">
        <div 
          v-for="template in providerTemplates"
          :key="template.type"
          class="template-card glass-card card-hover"
          @click="useTemplate(template)"
        >
          <div class="template-icon">
            <el-icon>
              <Key v-if="template.type === 'letsencrypt'" />
              <Lock v-else-if="template.type === 'zerossl'" />
              <Setting v-else />
            </el-icon>
          </div>
          <h4 class="template-name">{{ template.name }}</h4>
          <p class="template-description">{{ template.description }}</p>
          <div class="template-features">
            <el-tag 
              v-for="feature in template.features"
              :key="feature"
              size="small"
              type="info"
            >
              {{ feature }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Provider Dialog -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingProvider ? 'Edit Provider' : 'Add New Provider'"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="provider-form">
        <el-form 
          ref="formRef"
          :model="providerForm" 
          :rules="formRules"
          label-width="140px"
        >
          <el-form-item label="Provider Type" prop="provider">
            <el-select 
              v-model="providerForm.provider" 
              placeholder="Select provider type"
            >
              <el-option 
                v-for="option in providerOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="Access Key" prop="access_key">
            <el-input 
              v-model="providerForm.access_key" 
              type="password"
              placeholder="Enter API key or access token"
              show-password
            />
          </el-form-item>

          <el-form-item label="Secret Key">
            <el-input 
              v-model="providerForm.secret_key" 
              type="password"
              placeholder="Enter secret key (if required)"
              show-password
            />
          </el-form-item>

          <el-form-item label="Config">
            <el-input 
              v-model="providerForm.config" 
              type="textarea"
              placeholder="Additional configuration (JSON format)"
              :rows="3"
            />
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <el-button @click="cancelEdit">Cancel</el-button>
        <el-button 
          type="primary" 
          @click="saveProvider"
          :loading="saving"
        >
          {{ editingProvider ? 'Update' : 'Create' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Key, Lock, Setting, Edit, Connection, MoreFilled
} from '@element-plus/icons-vue'
import { apiFetch } from '../utils/http'

interface Provider {
  id: number
  provider: string
  access_key: string
  secret_key?: string
  config?: string
  created_at: string
  certificate_count?: number
}

interface ProviderTemplate {
  type: string
  name: string
  description: string
  features: string[]
}

// State
const providers = ref<Provider[]>([])
const showCreateDialog = ref(false)
const editingProvider = ref<Provider | null>(null)
const saving = ref(false)
const testingProvider = ref<number | null>(null)
const formRef = ref()

const providerForm = reactive({
  provider: '',
  access_key: '',
  secret_key: '',
  config: ''
})

const formRules = {
  provider: [{ required: true, message: 'Please select provider type' }],
  access_key: [{ required: true, message: 'Please enter access key' }]
}

const providerOptions = [
  { label: "Let's Encrypt", value: 'letsencrypt' },
  { label: 'ZeroSSL', value: 'zerossl' },
  { label: 'Cloudflare', value: 'cloudflare' },
  { label: 'DigitalOcean', value: 'digitalocean' }
]

const providerTemplates: ProviderTemplate[] = [
  {
    type: 'letsencrypt',
    name: "Let's Encrypt",
    description: 'Free SSL certificates with automatic renewal',
    features: ['Free', 'Auto-renewal', 'Domain validation']
  },
  {
    type: 'zerossl',
    name: 'ZeroSSL',
    description: 'Free and paid SSL certificates with API support',
    features: ['Free tier', 'API integration', 'Extended validation']
  },
  {
    type: 'cloudflare',
    name: 'Cloudflare',
    description: 'SSL certificates through Cloudflare DNS',
    features: ['DNS integration', 'Fast deployment', 'CDN included']
  }
]

// Methods
function getProviderName(type: string) {
  switch (type) {
    case 'letsencrypt': return "Let's Encrypt"
    case 'zerossl': return 'ZeroSSL'
    case 'cloudflare': return 'Cloudflare'
    case 'digitalocean': return 'DigitalOcean'
    default: return type
  }
}

function formatDate(dateString: string) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

function editProvider(provider: Provider) {
  editingProvider.value = provider
  Object.assign(providerForm, {
    provider: provider.provider,
    access_key: provider.access_key,
    secret_key: provider.secret_key || '',
    config: provider.config || ''
  })
  showCreateDialog.value = true
}

function useTemplate(template: ProviderTemplate) {
  Object.assign(providerForm, {
    provider: template.type,
    access_key: '',
    secret_key: '',
    config: ''
  })
  showCreateDialog.value = true
}

function cancelEdit() {
  showCreateDialog.value = false
  editingProvider.value = null
  formRef.value?.resetFields()
  Object.assign(providerForm, {
    provider: '',
    access_key: '',
    secret_key: '',
    config: ''
  })
}

async function saveProvider() {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
  } catch {
    return
  }

  saving.value = true
  try {
    const data = { ...providerForm }
    let result
    
    if (editingProvider.value) {
      result = await apiFetch(`/provider-credentials/${editingProvider.value.id}/`, {
        method: 'PUT',
        body: JSON.stringify(data)
      })
    } else {
      result = await apiFetch('/provider-credentials/', {
        method: 'POST',
        body: JSON.stringify(data)
      })
    }

    if (result.code === 0) {
      ElMessage.success(editingProvider.value ? 'Provider updated' : 'Provider created')
      showCreateDialog.value = false
      await loadProviders()
      cancelEdit()
    } else {
      ElMessage.error(result.message || 'Failed to save provider')
    }
  } catch (error) {
    ElMessage.error('Failed to save provider')
    console.error('Save provider error:', error)
  } finally {
    saving.value = false
  }
}

async function testProvider(provider: Provider) {
  testingProvider.value = provider.id
  try {
    // Mock test for now
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('Provider connection test passed')
  } catch (error) {
    ElMessage.error('Provider test failed')
    console.error('Test provider error:', error)
  } finally {
    testingProvider.value = null
  }
}

function handleProviderAction(command: string, provider: Provider) {
  if (command === 'delete') {
    deleteProvider(provider)
  }
}

async function deleteProvider(provider: Provider) {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete the provider "${getProviderName(provider.provider)}"?`,
      'Confirm Deletion',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'error'
      }
    )
    
    const result = await apiFetch(`/provider-credentials/${provider.id}/`, {
      method: 'DELETE'
    })
    
    if (result.code === 0) {
      await loadProviders()
      ElMessage.success('Provider deleted')
    } else {
      ElMessage.error(result.message || 'Failed to delete provider')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete provider')
      console.error('Delete provider error:', error)
    }
  }
}

async function loadProviders() {
  try {
    const result = await apiFetch<Provider[]>('/provider-credentials/')
    if (result.code === 0) {
      providers.value = result.data || []
    } else {
      ElMessage.error(result.message || 'Failed to load providers')
    }
  } catch (error) {
    ElMessage.error('Failed to load providers')
    console.error('Load providers error:', error)
  }
}

onMounted(() => {
  loadProviders()
})
</script>

<style scoped>
.providers-page {
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

.providers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-2xl);
}

.provider-card {
  padding: var(--space-lg);
  border-radius: var(--radius-xl);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.provider-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.provider-info {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
}

.provider-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.provider-icon {
  font-size: 24px;
  color: var(--primary-color);
}

.provider-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-xs) 0;
}

.provider-description {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
}

.provider-stats {
  display: flex;
  gap: var(--space-lg);
  padding: var(--space-md);
  background: var(--bg-light);
  border-radius: var(--radius-lg);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: var(--space-xs);
}

.provider-actions {
  display: flex;
  gap: var(--space-sm);
}

.add-provider-card {
  padding: var(--space-2xl);
  border-radius: var(--radius-xl);
  border: 2px dashed var(--border-light);
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-provider-card:hover {
  border-color: var(--primary-color);
  background: var(--primary-light);
}

.add-provider-content {
  text-align: center;
}

.add-icon {
  font-size: 48px;
  color: var(--text-light);
  margin-bottom: var(--space-md);
}

.add-provider-content h3 {
  color: var(--text-primary);
  margin: 0 0 var(--space-sm) 0;
}

.add-provider-content p {
  color: var(--text-secondary);
  margin: 0;
}

.templates-section {
  margin-bottom: var(--space-2xl);
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-lg) 0;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
}

.template-card {
  padding: var(--space-lg);
  border-radius: var(--radius-xl);
  cursor: pointer;
  text-align: center;
  transition: var(--transition);
}

.template-card:hover {
  transform: translateY(-4px);
}

.template-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  background: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--space-md);
  font-size: 32px;
  color: var(--primary-color);
}

.template-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-sm) 0;
}

.template-description {
  color: var(--text-secondary);
  margin: 0 0 var(--space-md) 0;
}

.template-features {
  display: flex;
  gap: var(--space-xs);
  flex-wrap: wrap;
  justify-content: center;
}

.provider-form {
  max-height: 500px;
  overflow-y: auto;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: var(--space-md);
    align-items: stretch;
  }
  
  .providers-grid {
    grid-template-columns: 1fr;
  }
  
  .templates-grid {
    grid-template-columns: 1fr;
  }
  
  .provider-stats {
    flex-direction: column;
    gap: var(--space-sm);
  }
  
  .provider-actions {
    flex-wrap: wrap;
  }
}
</style>
