<template>
  <div class="dashboard">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title gradient-text">{{ $t('dashboard') }}</h1>
        <p class="page-subtitle">{{ $t('welcome') }}, {{ auth.user?.username }}!</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" class="btn-gradient">
          <el-icon><Plus /></el-icon>
          {{ $t('create') }} Certificate
        </el-button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card glass-card card-hover">
        <div class="stat-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.totalCerts }}</h3>
            <p class="stat-label">Total Certificates</p>
          </div>
          <div class="stat-icon">
            <el-icon class="icon-primary"><Document /></el-icon>
          </div>
        </div>
        <div class="stat-trend">
          <span class="trend-value positive">+12%</span>
          <span class="trend-label">vs last month</span>
        </div>
      </div>

      <div class="stat-card glass-card card-hover">
        <div class="stat-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.activeCerts }}</h3>
            <p class="stat-label">Active Certificates</p>
          </div>
          <div class="stat-icon">
            <el-icon class="icon-success"><CircleCheck /></el-icon>
          </div>
        </div>
        <div class="stat-trend">
          <span class="trend-value positive">+8%</span>
          <span class="trend-label">vs last month</span>
        </div>
      </div>

      <div class="stat-card glass-card card-hover">
        <div class="stat-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.expiringCerts }}</h3>
            <p class="stat-label">Expiring Soon</p>
          </div>
          <div class="stat-icon">
            <el-icon class="icon-warning"><Warning /></el-icon>
          </div>
        </div>
        <div class="stat-trend">
          <span class="trend-value negative">+3</span>
          <span class="trend-label">this week</span>
        </div>
      </div>

      <div class="stat-card glass-card card-hover">
        <div class="stat-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.providers }}</h3>
            <p class="stat-label">Providers</p>
          </div>
          <div class="stat-icon">
            <el-icon class="icon-info"><Setting /></el-icon>
          </div>
        </div>
        <div class="stat-trend">
          <span class="trend-value">{{ stats.providers }} configured</span>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Recent Certificates -->
      <div class="content-card glass-card">
        <div class="card-header">
          <h3 class="card-title">Recent Certificates</h3>
          <el-button text @click="$router.push('/certificates')">
            View All <el-icon><Right /></el-icon>
          </el-button>
        </div>
        <div class="card-content">
          <div v-if="recentCerts.length === 0" class="empty-state">
            <el-icon class="empty-icon"><Document /></el-icon>
            <p class="empty-text">No certificates yet</p>
            <el-button type="primary" class="btn-gradient" @click="$router.push('/certificates')">
              Create First Certificate
            </el-button>
          </div>
          <div v-else class="cert-list">
            <div 
              v-for="cert in recentCerts" 
              :key="cert.id" 
              class="cert-item"
            >
              <div class="cert-info">
                <h4 class="cert-domain">{{ cert.domain }}</h4>
                <p class="cert-provider">{{ cert.provider }}</p>
              </div>
              <div class="cert-status">
                <el-tag 
                  :type="getCertStatusType(cert.status)"
                  size="small"
                >
                  {{ cert.status }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="content-card glass-card">
        <div class="card-header">
          <h3 class="card-title">Quick Actions</h3>
        </div>
        <div class="card-content">
          <div class="action-grid">
            <div class="action-item" @click="$router.push('/certificates')">
              <el-icon class="action-icon"><Document /></el-icon>
              <span class="action-text">Manage Certificates</span>
            </div>
            <div class="action-item" @click="$router.push('/providers')">
              <el-icon class="action-icon"><Setting /></el-icon>
              <span class="action-text">Configure Providers</span>
            </div>
            <div class="action-item" @click="$router.push('/settings')">
              <el-icon class="action-icon"><Tools /></el-icon>
              <span class="action-text">System Settings</span>
            </div>
            <div class="action-item">
              <el-icon class="action-icon"><Bell /></el-icon>
              <span class="action-text">Notifications</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="chart-section">
      <div class="content-card glass-card">
        <div class="card-header">
          <h3 class="card-title">Certificate Status Overview</h3>
          <div class="chart-controls">
            <el-select v-model="chartPeriod" size="small">
              <el-option label="Last 7 days" value="7d" />
              <el-option label="Last 30 days" value="30d" />
              <el-option label="Last 90 days" value="90d" />
            </el-select>
          </div>
        </div>
        <div class="card-content">
          <div class="chart-container" ref="chartRef">
            <!-- Chart will be rendered here -->
            <div class="chart-placeholder">
              <el-icon class="chart-icon"><TrendCharts /></el-icon>
              <p>Certificate analytics chart will be displayed here</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { 
  Plus, Document, CircleCheck, Warning, Setting, Right, 
  Tools, Bell, TrendCharts 
} from '@element-plus/icons-vue'

interface Certificate {
  id: number
  domain: string
  provider: string
  status: 'active' | 'pending' | 'expired' | 'error'
  created_at: string
  expires_at: string
}

const auth = useAuthStore()

const chartRef = ref()
const chartPeriod = ref('30d')

const stats = reactive({
  totalCerts: 0,
  activeCerts: 0,
  expiringCerts: 0,
  providers: 0
})

const recentCerts = ref<Certificate[]>([])

function getCertStatusType(status: Certificate['status']) {
  switch (status) {
    case 'active': return 'success'
    case 'pending': return 'warning'
    case 'expired': return 'danger'
    default: return 'info'
  }
}

async function loadDashboardData() {
  // TODO: Load real data from API
  stats.totalCerts = 0
  stats.activeCerts = 0
  stats.expiringCerts = 0
  stats.providers = 0
  recentCerts.value = []
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.dashboard {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.stat-card {
  padding: var(--space-lg);
  border-radius: var(--radius-xl);
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-md);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--space-xs) 0;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.icon-primary {
  color: var(--primary-color);
  background: rgba(255, 107, 157, 0.1);
}

.icon-success {
  color: var(--success-color);
  background: rgba(89, 216, 161, 0.1);
}

.icon-warning {
  color: var(--warning-color);
  background: rgba(255, 179, 71, 0.1);
}

.icon-info {
  color: var(--info-color);
  background: rgba(103, 199, 255, 0.1);
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.trend-value {
  font-weight: 600;
  font-size: 12px;
}

.trend-value.positive {
  color: var(--success-color);
}

.trend-value.negative {
  color: var(--error-color);
}

.trend-label {
  color: var(--text-light);
  font-size: 12px;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.content-card {
  padding: var(--space-lg);
  border-radius: var(--radius-xl);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-lg);
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--border-light);
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: var(--space-2xl) var(--space-lg);
}

.empty-icon {
  font-size: 48px;
  color: var(--text-light);
  margin-bottom: var(--space-md);
}

.empty-text {
  color: var(--text-secondary);
  margin-bottom: var(--space-lg);
}

.cert-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.cert-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md);
  border-radius: var(--radius-lg);
  background: var(--bg-light);
  margin-bottom: var(--space-sm);
}

.cert-domain {
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-xs) 0;
}

.cert-provider {
  color: var(--text-secondary);
  font-size: 12px;
  margin: 0;
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  background: var(--bg-light);
  cursor: pointer;
  transition: var(--transition);
  text-align: center;
}

.action-item:hover {
  background: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}

.action-icon {
  font-size: 24px;
  margin-bottom: var(--space-sm);
}

.action-text {
  font-size: 12px;
  font-weight: 500;
}

.chart-section {
  margin-bottom: var(--space-xl);
}

.chart-controls {
  display: flex;
  gap: var(--space-sm);
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: var(--text-light);
}

.chart-icon {
  font-size: 48px;
  margin-bottom: var(--space-md);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
    gap: var(--space-md);
    align-items: stretch;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content h1 {
    font-size: 24px;
  }
}
</style>
