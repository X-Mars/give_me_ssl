<template>
  <div class="certificates-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title gradient-text">SSL Certificates</h1>
        <p class="page-subtitle">Manage your SSL certificates and monitor their status</p>
      </div>
      <div class="header-actions">
        <el-button @click="showFilters = !showFilters">
          <el-icon><Filter /></el-icon>
          Filters
        </el-button>
        <el-button type="primary" class="btn-gradient" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          New Certificate
        </el-button>
      </div>
    </div>

    <!-- Filters Panel -->
    <div v-show="showFilters" class="filters-panel glass-card">
      <div class="filter-grid">
        <el-input
          v-model="filters.search"
          placeholder="Search certificates..."
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-select
          v-model="filters.status"
          placeholder="Status"
          clearable
          @change="handleFilter"
        >
          <el-option label="All Status" value="" />
          <el-option label="Active" value="active" />
          <el-option label="Pending" value="pending" />
          <el-option label="Expired" value="expired" />
          <el-option label="Error" value="error" />
        </el-select>
        
        <el-select
          v-model="filters.provider"
          placeholder="Provider"
          clearable
          @change="handleFilter"
        >
          <el-option label="All Providers" value="" />
          <el-option label="Let's Encrypt" value="letsencrypt" />
          <el-option label="ZeroSSL" value="zerossl" />
          <el-option label="Manual" value="manual" />
        </el-select>
        
        <el-button @click="fetchData" :loading="loading" class="refresh-btn">
          <el-icon><Refresh /></el-icon>
          Refresh
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
        empty-text="No certificates found"
      >
        <el-table-column type="selection" width="50" />
        
        <el-table-column prop="domain" label="Domain" sortable min-width="200">
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
        
        <el-table-column prop="status" label="Status" width="120">
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
        
        <el-table-column prop="provider" label="Provider" width="140">
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
        
        <el-table-column prop="created_at" label="Created" width="120" sortable>
          <template #default="{ row }">
            <div class="date-cell">
              {{ formatDate(row.created_at) }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="expires_at" label="Expires" width="120" sortable>
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
        
        <el-table-column label="Actions" width="180" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-tooltip content="View Details">
                <el-button size="small" circle @click="viewCertificate(row)">
                  <el-icon><View /></el-icon>
                </el-button>
              </el-tooltip>
              
              <el-tooltip content="Download">
                <el-button size="small" circle @click="downloadCertificate(row)">
                  <el-icon><Download /></el-icon>
                </el-button>
              </el-tooltip>
              
              <el-tooltip content="Renew">
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
              
              <el-dropdown @command="(cmd) => handleAction(cmd, row)">
                <el-button size="small" circle>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">Edit</el-dropdown-item>
                    <el-dropdown-item command="revoke">Revoke</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>Delete</el-dropdown-item>
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
      title="Create New Certificate"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="create-form">
        <el-form :model="createForm" label-width="120px">
          <el-form-item label="Domain">
            <el-input v-model="createForm.domain" placeholder="example.com" />
          </el-form-item>
          <el-form-item label="Provider">
            <el-select v-model="createForm.provider" placeholder="Select provider">
              <el-option label="Let's Encrypt" value="letsencrypt" />
              <el-option label="ZeroSSL" value="zerossl" />
              <el-option label="Manual" value="manual" />
            </el-select>
          </el-form-item>
          <el-form-item label="Auto Renew">
            <el-switch v-model="createForm.auto_renew" />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="showCreateDialog = false">Cancel</el-button>
        <el-button type="primary" @click="createCertificate">Create</el-button>
      </template>
    </el-dialog>

    <!-- Certificate Details Dialog -->
    <el-dialog
      v-model="showDetailsDialog"
      title="Certificate Details"
      width="800px"
    >
      <div v-if="selectedCertificate" class="cert-details">
        <div class="detail-grid">
          <div class="detail-item">
            <label>Domain:</label>
            <span>{{ selectedCertificate.domain }}</span>
          </div>
          <div class="detail-item">
            <label>Status:</label>
            <el-tag :type="getStatusType(selectedCertificate.status)">
              {{ getStatusText(selectedCertificate.status) }}
            </el-tag>
          </div>
          <div class="detail-item">
            <label>Provider:</label>
            <span>{{ getProviderName(selectedCertificate.provider) }}</span>
          </div>
          <div class="detail-item">
            <label>Created:</label>
            <span>{{ formatDate(selectedCertificate.created_at) }}</span>
          </div>
          <div class="detail-item">
            <label>Expires:</label>
            <span>{{ formatDate(selectedCertificate.expires_at) }}</span>
          </div>
          <div class="detail-item">
            <label>Auto Renew:</label>
            <span>{{ selectedCertificate.auto_renew ? 'Yes' : 'No' }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Filter, Search, CircleCheck, Clock, Warning, Close,
  View, Download, Refresh, MoreFilled, Key, Lock, Document
} from '@element-plus/icons-vue'
import { apiFetch } from '../utils/http'

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
  let result = certificates.value

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
    case 'active': return 'Active'
    case 'pending': return 'Pending'
    case 'expired': return 'Expired'
    case 'error': return 'Error'
    default: return 'Unknown'
  }
}

function getProviderName(provider: string) {
  switch (provider) {
    case 'letsencrypt': return "Let's Encrypt"
    case 'zerossl': return 'ZeroSSL'
    case 'manual': return 'Manual'
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
  
  if (daysUntilExpiry < 0) return `Expired ${Math.abs(daysUntilExpiry)} days ago`
  if (daysUntilExpiry === 0) return 'Expires today'
  if (daysUntilExpiry === 1) return 'Expires tomorrow'
  return `${daysUntilExpiry} days left`
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
    `Are you sure you want to renew the certificate for ${certificate.domain}?`,
    'Confirm Renewal',
    {
      confirmButtonText: 'Renew',
      cancelButtonText: 'Cancel',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('Certificate renewal initiated')
  }).catch(() => {
    // User cancelled
  })
}

function handleAction(command: string, certificate: Certificate) {
  switch (command) {
    case 'edit':
      ElMessage.info(`Edit certificate for ${certificate.domain}`)
      break
    case 'revoke':
      ElMessageBox.confirm(
        `Are you sure you want to revoke the certificate for ${certificate.domain}?`,
        'Confirm Revocation',
        {
          confirmButtonText: 'Revoke',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }
      ).then(() => {
        ElMessage.success('Certificate revoked')
      })
      break
    case 'delete':
      ElMessageBox.confirm(
        `Are you sure you want to delete the certificate for ${certificate.domain}?`,
        'Confirm Deletion',
        {
          confirmButtonText: 'Delete',
          cancelButtonText: 'Cancel',
          type: 'error'
        }
      ).then(() => {
        ElMessage.success('Certificate deleted')
      })
      break
  }
}

function createCertificate() {
  if (!createForm.domain || !createForm.provider) {
    ElMessage.warning('Please fill in all required fields')
    return
  }
  
  // TODO: Call API to create certificate
  ElMessage.success(`Creating certificate for ${createForm.domain}`)
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
      certificates.value = res.data || []
    } else {
      ElMessage.error(res.message || 'Failed to load certificates')
    }
  } catch (error) {
    ElMessage.error('Failed to load certificates')
    console.error('Load certificates error:', error)
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
