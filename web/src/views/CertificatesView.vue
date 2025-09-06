<template>
  <div class="certificates-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title gradient-text">{{ $t('certificates.title') }}</h1>
        <p class="page-subtitle">{{ $t('certificates.subtitle') }}</p>
      </div>
      <div class="header-actions">
        <el-button @click="showFilters = !showFilters">
          <el-icon><Filter /></el-icon>
          {{ $t('common.filters') }}
        </el-button>
                <el-button type="primary" class="glass-button" @click="createCertificate">
          <el-icon><Plus /></el-icon>
          {{ $t('certificates.createNew') }}
        </el-button>
      </div>
    </div>

    <!-- Filters Panel -->
    <div v-show="showFilters" class="filters-panel glass-card">
      <div class="filter-grid">
        <el-input
          v-model="filters.search"
          :placeholder="$t('certificates.searchPlaceholder')"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-select
          v-model="filters.status"
          :placeholder="$t('certificates.status')"
          clearable
          @change="handleFilter"
        >
          <el-option :label="$t('common.all')" value="" />
          <el-option :label="$t('certificates.statuses.active')" value="active" />
          <el-option :label="$t('certificates.statuses.pending')" value="pending" />
          <el-option :label="$t('certificates.statuses.expired')" value="expired" />
          <el-option :label="$t('certificates.statuses.error')" value="error" />
        </el-select>
        
        <el-select
          v-model="filters.provider"
          :placeholder="$t('certificates.provider')"
          clearable
          @change="handleFilter"
        >
          <el-option :label="$t('common.all')" value="" />
          <el-option label="Let's Encrypt" value="letsencrypt" />
          <el-option label="ZeroSSL" value="zerossl" />
          <el-option :label="$t('certificates.manual')" value="manual" />
        </el-select>
        
        <el-button @click="fetchData" :loading="loading" class="refresh-btn">
          <el-icon><Refresh /></el-icon>
          {{ $t('common.refresh') }}
        </el-button>
      </div>
    </div>

    <!-- Certificates Table -->
    <div class="table-container glass-card">
      <el-table
        v-loading="loading"
        :data="paginatedCertificates"
        stripe
        class="certificates-table"
        @sort-change="handleSort"
        :empty-text="$t('certificates.noCertificates')"
      >
        <el-table-column type="selection" width="50" />
        
        <el-table-column prop="domain" :label="$t('certificates.domain')" sortable min-width="200">
          <template #default="{ row }">
            <div class="domain-cell">
              <div class="domain-info">
                <h4 class="domain-name">{{ row.domain }}</h4>
                <div class="domain-tags">
                  <el-tag v-if="row.is_wildcard" size="small" type="info">Wildcard</el-tag>
                  <el-tag v-if="row.auto_renew" size="small" type="success">Auto-Renew</el-tag>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" :label="$t('certificates.status')" width="120">
          <template #default="{ row }">
            <el-tag 
              :type="getStatusType(row.status)" 
              size="small"
              class="status-tag"
            >
              <el-icon class="status-icon">
                <CircleCheck v-if="row.status === 'active'" />
                <Clock v-else-if="row.status === 'pending'" />
                <Warning v-else-if="row.status === 'expired'" />
                <Close v-else />
              </el-icon>
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="provider" :label="$t('certificates.provider')" width="140">
          <template #default="{ row }">
            <div class="provider-cell">
              <div class="provider-icon-wrapper">
                <el-icon class="provider-icon">
                  <Key v-if="row.provider === 'letsencrypt'" />
                  <Lock v-else-if="row.provider === 'zerossl'" />
                  <Document v-else />
                </el-icon>
              </div>
              {{ getProviderName(row.provider) }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" :label="$t('certificates.created')" width="120" sortable>
          <template #default="{ row }">
            <div class="date-cell">
              {{ formatDate(row.created_at) }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="expires_at" :label="$t('certificates.expires')" width="120" sortable>
          <template #default="{ row }">
            <div class="date-cell">
              <span :class="getExpiryClass(row.expires_at)">
                {{ formatDate(row.expires_at) }}
              </span>
              <div v-if="row.expires_at" class="expiry-info">
                {{ getExpiryText(row.expires_at) }}
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column :label="$t('common.actions')" width="180" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-tooltip :content="$t('certificates.viewDetails')">
                <el-button size="small" circle @click="viewCertificate(row)">
                  <el-icon><View /></el-icon>
                </el-button>
              </el-tooltip>
              
              <el-tooltip :content="$t('certificates.download')">
                <el-button size="small" circle @click="downloadCertificate(row)">
                  <el-icon><Download /></el-icon>
                </el-button>
              </el-tooltip>
              
              <el-tooltip :content="$t('certificates.renew')">
                <el-button 
                  size="small" 
                  circle 
                  type="warning"
                  :disabled="row.status === 'pending'"
                  @click="renewCertificate(row)"
                >
                  <el-icon><Refresh /></el-icon>
                </el-button>
              </el-tooltip>
              
              <el-dropdown @command="createDropdownHandler(row)">
                <el-button size="small" circle>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">{{ $t('common.edit') }}</el-dropdown-item>
                    <el-dropdown-item command="revoke">{{ $t('certificates.revoke') }}</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>{{ $t('common.delete') }}</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="filteredCertificates.length"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- Create Certificate Dialog -->
    <el-dialog
      v-model="showCreateDialog"
      :title="$t('certificates.createNew')"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="create-form">
        <el-form :model="createForm" label-width="120px">
          <el-form-item :label="$t('certificates.domain')">
            <el-input v-model="createForm.domain" placeholder="example.com" />
          </el-form-item>
          <el-form-item :label="$t('certificates.provider')">
            <el-select v-model="createForm.provider" :placeholder="$t('common.selectProvider')">
              <el-option label="Let's Encrypt" value="letsencrypt" />
              <el-option label="ZeroSSL" value="zerossl" />
              <el-option :label="$t('certificates.manual')" value="manual" />
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('certificates.autoRenew')">
            <el-switch v-model="createForm.auto_renew" />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="showCreateDialog = false">{{ $t('common.cancel') }}</el-button>
        <el-button type="primary" @click="createCertificate">{{ $t('common.create') }}</el-button>
      </template>
    </el-dialog>

    <!-- Certificate Details Dialog -->
    <el-dialog
      v-model="showDetailsDialog"
      :title="$t('certificates.details')"
      width="800px"
    >
      <div v-if="selectedCertificate" class="cert-details">
        <div class="detail-grid">
          <div class="detail-item">
            <label>{{ $t('certificates.domain') }}:</label>
            <span>{{ selectedCertificate.domain }}</span>
          </div>
          <div class="detail-item">
            <label>{{ $t('certificates.status') }}:</label>
            <el-tag :type="getStatusType(selectedCertificate.status)">
              {{ $t(`certificates.statuses.${selectedCertificate.status}`) }}
            </el-tag>
          </div>
          <div class="detail-item">
            <label>{{ $t('certificates.provider') }}:</label>
            <span>{{ getProviderName(selectedCertificate.provider) }}</span>
          </div>
          <div class="detail-item">
            <label>{{ $t('certificates.created') }}:</label>
            <span>{{ formatDate(selectedCertificate.created_at) }}</span>
          </div>
          <div class="detail-item">
            <label>{{ $t('certificates.expires') }}:</label>
            <span>{{ formatDate(selectedCertificate.expires_at) }}</span>
          </div>
          <div class="detail-item">
            <label>{{ $t('certificates.autoRenew') }}:</label>
            <span>{{ selectedCertificate.auto_renew ? $t('common.yes') : $t('common.no') }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useI18n } from 'vue-i18n'
import {
  Plus, Filter, Search, CircleCheck, Clock, Warning, Close,
  View, Download, Refresh, MoreFilled, Key, Lock, Document
} from '@element-plus/icons-vue'
import { apiFetch } from '../utils/http'

const { t } = useI18n()

interface Certificate {
  id: number
  domain: string
  status: 'active' | 'pending' | 'expired' | 'error'
  provider: string
  created_at: string
  expires_at: string
  is_wildcard?: boolean
  auto_renew?: boolean
}

// State
const loading = ref(false)
const showFilters = ref(false)
const showCreateDialog = ref(false)
const showDetailsDialog = ref(false)
const selectedCertificate = ref<Certificate | null>(null)

const certificates = ref<Certificate[]>([])
const currentPage = ref(1)
const pageSize = ref(20)

const filters = reactive({
  search: '',
  status: '',
  provider: ''
})

const createForm = reactive({
  domain: '',
  provider: '',
  auto_renew: true
})

// Computed
const filteredCertificates = computed(() => {
  let result = Array.isArray(certificates.value) ? certificates.value : []

  if (filters.search) {
    result = result.filter(cert => 
      cert.domain.toLowerCase().includes(filters.search.toLowerCase())
    )
  }

  if (filters.status) {
    result = result.filter(cert => cert.status === filters.status)
  }

  if (filters.provider) {
    result = result.filter(cert => cert.provider === filters.provider)
  }

  return result
})

const paginatedCertificates = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredCertificates.value.slice(start, end)
})

// Methods
function getStatusType(status: Certificate['status']) {
  switch (status) {
    case 'active': return 'success'
    case 'pending': return 'warning'
    case 'expired': return 'danger'
    case 'error': return 'danger'
    default: return 'info'
  }
}

function getStatusText(status: Certificate['status']) {
  switch (status) {
    case 'active': return t('certificates.statuses.active')
    case 'pending': return t('certificates.statuses.pending')
    case 'expired': return t('certificates.statuses.expired')
    case 'error': return t('certificates.statuses.error')
    default: return t('certificates.statuses.unknown')
  }
}

function getProviderName(provider: string) {
  switch (provider) {
    case 'letsencrypt': return "Let's Encrypt"
    case 'zerossl': return 'ZeroSSL'
    case 'manual': return t('certificates.manual')
    default: return provider
  }
}

function formatDate(dateString: string) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

function getExpiryClass(expiryDate: string) {
  if (!expiryDate) return 'expiring-normal'
  
  const expiry = new Date(expiryDate)
  const now = new Date()
  const daysUntilExpiry = Math.ceil((expiry.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  
  if (daysUntilExpiry < 0) return 'expired'
  if (daysUntilExpiry <= 7) return 'expiring-soon'
  if (daysUntilExpiry <= 30) return 'expiring-warning'
  return 'expiring-normal'
}

function getExpiryText(expiryDate: string) {
  if (!expiryDate) return ''
  
  const expiry = new Date(expiryDate)
  const now = new Date()
  const daysUntilExpiry = Math.ceil((expiry.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  
  if (daysUntilExpiry < 0) return t('certificates.expiredDaysAgo', { days: Math.abs(daysUntilExpiry) })
  if (daysUntilExpiry === 0) return t('certificates.expiresToday')
  if (daysUntilExpiry === 1) return t('certificates.expiresTomorrow')
  return t('certificates.daysLeft', { days: daysUntilExpiry })
}

function handleSearch() {
  currentPage.value = 1
}

function handleFilter() {
  currentPage.value = 1
}

function handleSort({ prop, order }: { prop: string; order: string }) {
  console.log('Sort:', prop, order)
}

function handleSizeChange(size: number) {
  pageSize.value = size
  currentPage.value = 1
}

function handlePageChange(page: number) {
  currentPage.value = page
}

function viewCertificate(certificate: Certificate) {
  selectedCertificate.value = certificate
  showDetailsDialog.value = true
}

function downloadCertificate(certificate: Certificate) {
  ElMessage.success(`Downloading certificate for ${certificate.domain}`)
}

function renewCertificate(certificate: Certificate) {
  ElMessageBox.confirm(
    t('certificates.renewConfirmMessage', { domain: certificate.domain }),
    t('certificates.renewConfirmTitle'),
    {
      confirmButtonText: t('common.confirm'),
      cancelButtonText: t('common.cancel'),
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success(t('certificates.renewSuccess'))
  }).catch(() => {
    // User cancelled
  })
}

// Helper to create dropdown command handler for a specific row
const createDropdownHandler = (row: Certificate) => {
  return (cmd: unknown) => handleAction(cmd, row)
}

function handleAction(command: unknown, certificate: Certificate) {
  const cmd = String(command)
  switch (cmd) {
    case 'edit':
      ElMessage.info(t('certificates.editMessage', { domain: certificate.domain }))
      break
    case 'revoke':
      ElMessageBox.confirm(
        t('certificates.revokeConfirmMessage', { domain: certificate.domain }),
        t('certificates.revokeConfirmTitle'),
        {
          confirmButtonText: t('common.confirm'),
          cancelButtonText: t('common.cancel'),
          type: 'warning'
        }
      ).then(() => {
        ElMessage.success(t('certificates.revokeSuccess'))
      })
      break
    case 'delete':
      ElMessageBox.confirm(
        t('certificates.deleteConfirmMessage', { domain: certificate.domain }),
        t('certificates.deleteConfirmTitle'),
        {
          confirmButtonText: t('common.confirm'),
          cancelButtonText: t('common.cancel'),
          type: 'error'
        }
      ).then(() => {
        ElMessage.success(t('certificates.deleteSuccess'))
      })
      break
  }
}

function createCertificate() {
  if (!createForm.domain || !createForm.provider) {
    ElMessage.warning(t('certificates.fillRequiredFields'))
    return
  }
  
  // TODO: Call API to create certificate
  ElMessage.success(t('certificates.createSuccess', { domain: createForm.domain }))
  showCreateDialog.value = false
  
  // Reset form
  Object.assign(createForm, {
    domain: '',
    provider: '',
    auto_renew: true
  })
}

async function fetchData() {
  loading.value = true
  try {
    const res = await apiFetch<Certificate[]>('/certificates/')
    if (res.code === 0) {
      certificates.value = Array.isArray(res.data) ? res.data : []
    } else {
      ElMessage.error(res.message || t('certificates.loadError'))
      certificates.value = []
    }
  } catch (error) {
    ElMessage.error(t('certificates.loadError'))
    console.error('Load certificates error:', error)
    certificates.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.certificates-page {
  max-width: 1400px;
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

.header-actions {
  display: flex;
  gap: var(--space-md);
}

.filters-panel {
  padding: var(--space-lg);
  border-radius: var(--radius-xl);
  margin-bottom: var(--space-lg);
}

.filter-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: var(--space-md);
  align-items: center;
}

.refresh-btn {
  white-space: nowrap;
}

.table-container {
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.certificates-table {
  --el-table-border-color: var(--border-light);
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: var(--bg-light);
}

.domain-cell {
  display: flex;
  align-items: center;
}

.domain-name {
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-xs) 0;
  font-size: 14px;
}

.domain-tags {
  display: flex;
  gap: var(--space-xs);
}

.status-tag {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.status-icon {
  font-size: 12px;
}

.provider-cell {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.provider-icon-wrapper {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-sm);
  background: var(--bg-light);
  display: flex;
  align-items: center;
  justify-content: center;
}

.provider-icon {
  font-size: 14px;
  color: var(--primary-color);
}

.date-cell {
  font-size: 13px;
}

.expiring-normal {
  color: var(--text-primary);
}

.expiring-warning {
  color: var(--warning-color);
}

.expiring-soon {
  color: var(--error-color);
  font-weight: 600;
}

.expired {
  color: var(--error-color);
  font-weight: 600;
}

.expiry-info {
  font-size: 11px;
  color: var(--text-light);
  margin-top: 2px;
}

.action-buttons {
  display: flex;
  gap: var(--space-xs);
}

.pagination-container {
  padding: var(--space-lg);
  border-top: 1px solid var(--border-light);
  display: flex;
  justify-content: center;
}

.create-form {
  padding: var(--space-md) 0;
}

.cert-details {
  padding: var(--space-md) 0;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-lg);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.detail-item label {
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 80px;
}

.detail-item span {
  color: var(--text-primary);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .filter-grid {
    grid-template-columns: 1fr 1fr auto;
    grid-row-gap: var(--space-md);
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: var(--space-md);
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: flex-end;
  }
  
  .filter-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-wrap: wrap;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
