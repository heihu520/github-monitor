<template>
  <div class="dashboard-view">
    <AppNav />
    
    <div class="container">
      <div class="dashboard-content">
        <!-- 页面标题 -->
        <div class="page-header">
          <h1 class="page-title">代码追踪仪表盘</h1>
          <p class="page-subtitle">实时监控你的编码活动和生产力指标</p>
        </div>

        <!-- 里程碑成就徽章区域 -->
        <TechCard
          v-if="unlockedMilestones.length > 0"
          title="最近成就"
          icon="🏆"
          class="milestones-card"
        >
          <div class="milestones-grid">
            <MilestoneBadge
              v-for="milestone in displayMilestones"
              :key="milestone.id"
              :milestone="milestone"
            />
          </div>
        </TechCard>

        <!-- 统计卡片网格 -->
        <div class="stats-grid">
          <StatCard
            icon="📊"
            label="今日提交"
            :value="stats.todayCommits"
            :trend="todayTrend"
            variant="primary"
          />
          <StatCard
            icon="💻"
            label="代码行数"
            :value="stats.codeLines"
            unit="行"
            :trend="weekTrend"
            variant="success"
          />
          <StatCard
            icon="🔥"
            label="连续天数"
            :value="stats.streakDays"
            unit="天"
            :trend="0"
            variant="warning"
          />
          <StatCard
            icon="⚡"
            label="工作时长"
            :value="stats.workHours"
            unit="小时"
            :trend="weekTrend"
            variant="primary"
          />
        </div>

        <!-- 图表区域 -->
        <div class="charts-section">
          <TechCard title="提交趋势" icon="📈" class="chart-card">
            <div class="chart-container">
              <CommitTrendChart :data="trendData" />
            </div>
          </TechCard>

          <div class="chart-grid">
            <TechCard title="语言分布" icon="💻" class="chart-card">
              <div class="chart-container chart-small">
                <LanguagePieChart :data="languageStats" />
              </div>
            </TechCard>

            <TechCard title="时段分析" icon="⏰" class="chart-card">
              <div class="chart-container chart-small">
                <HourlyActivityChart />
              </div>
            </TechCard>
          </div>
        </div>

        <!-- 最近活动 -->
        <TechCard title="最近活动" icon="🕐" class="activity-card">
          <div class="activity-list">
            <div 
              v-for="activity in recentActivities" 
              :key="activity.id"
              class="activity-item"
            >
              <span class="activity-icon">{{ activity.icon }}</span>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-time">{{ activity.time }}</div>
              </div>
              <span class="activity-badge" :class="`badge-${activity.type}`">
                {{ activity.typeLabel }}
              </span>
            </div>
          </div>
        </TechCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import AppNav from '@/components/AppNav.vue'
import TechCard from '@/components/TechCard.vue'
import StatCard from '@/components/StatCard.vue'
import CommitTrendChart from '@/components/CommitTrendChart.vue'
import LanguagePieChart from '@/components/LanguagePieChart.vue'
import HourlyActivityChart from '@/components/HourlyActivityChart.vue'
import MilestoneBadge from '@/components/MilestoneBadge.vue'
import { useStatsStore } from '@/stores'

// 使用统计数据 store
const statsStore = useStatsStore()

// 从 store 获取数据
const stats = computed(() => statsStore.dashboardStats)
const recentActivities = computed(() => statsStore.recentActivities)
const trendData = computed(() => statsStore.trendData)
const languageStats = computed(() => statsStore.languageStats)
const todayTrend = computed(() => statsStore.todayTrend)
const weekTrend = computed(() => statsStore.weekTrend)

// 成就里程碑数据
const unlockedMilestones = computed(() =>
  statsStore.milestones.filter(m => m.unlocked)
)

// 显示最近解锁的6个成就
const displayMilestones = computed(() => {
  const unlocked = unlockedMilestones.value
    .sort((a, b) => {
      if (!a.unlockedAt || !b.unlockedAt) return 0
      return new Date(b.unlockedAt).getTime() - new Date(a.unlockedAt).getTime()
    })
    .slice(0, 6)
  
  // 如果解锁成就少于6个，添加一些未解锁的成就
  const locked = statsStore.milestones
    .filter(m => !m.unlocked)
    .slice(0, Math.max(0, 6 - unlocked.length))
  
  return [...unlocked, ...locked]
})

// 组件挂载时加载数据
onMounted(async () => {
  await statsStore.refreshAllData()
})
</script>

<style scoped>
.dashboard-view {
  min-height: 100vh;
  background: var(--bg-primary);
}

.dashboard-content {
  padding: var(--spacing-2xl) 0;
}

/* 里程碑成就区域 */
.milestones-card {
  margin-bottom: var(--spacing-2xl);
  overflow: visible !important;
}

.milestones-card :deep(.card-body) {
  overflow: visible;
}

.milestones-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(72px, 72px));
  gap: var(--spacing-lg);
  justify-content: center;
  padding: var(--spacing-sm) 0;
  max-height: 120px;
  overflow: visible;
}

/* 页面标题 */
.page-header {
  margin-bottom: var(--spacing-2xl);
  text-align: center;
}

.page-title {
  margin-bottom: var(--spacing-sm);
  animation: fadeInUp 0.6s ease-out;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
  animation: fadeInUp 0.6s ease-out 0.1s both;
}

/* 统计卡片网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}

/* 图表区域 */
.charts-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-small {
  height: 250px;
}

.chart-placeholder {
  text-align: center;
  color: var(--text-tertiary);
}

.placeholder-text {
  font-size: 1.25rem;
  margin-bottom: var(--spacing-sm);
}

.placeholder-hint {
  font-size: 0.875rem;
  color: var(--text-disabled);
}

/* 活动列表 */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.activity-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  transition: all 0.3s ease;
}

.activity-item:hover {
  border-color: var(--border-primary);
  transform: translateX(4px);
}

.activity-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-title {
  color: var(--text-primary);
  font-weight: 500;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.activity-time {
  color: var(--text-tertiary);
  font-size: 0.75rem;
}

.activity-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-feat {
  background: rgba(74, 144, 226, 0.15);
  color: var(--primary-blue);
}

.badge-fix {
  background: rgba(82, 196, 26, 0.15);
  color: var(--primary-green);
}

.badge-docs {
  background: rgba(124, 92, 219, 0.15);
  color: var(--primary-purple);
}

.badge-style {
  background: rgba(250, 140, 22, 0.15);
  color: var(--primary-orange);
}

.badge-perf {
  background: rgba(245, 34, 45, 0.15);
  color: var(--primary-red);
}

/* 响应式 */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    padding: var(--spacing-xl) 0;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .milestones-grid {
    grid-template-columns: repeat(auto-fit, minmax(64px, 64px));
    gap: var(--spacing-md);
  }
}

/* 动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>