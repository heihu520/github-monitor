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

        <!-- 统计卡片网格 -->
        <div class="stats-grid">
          <StatCard
            icon="📊"
            label="今日提交"
            :value="stats.todayCommits"
            :trend="15"
            variant="primary"
          />
          <StatCard
            icon="💻"
            label="代码行数"
            :value="stats.codeLines"
            unit="行"
            :trend="8"
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
            :trend="-5"
            variant="primary"
          />
        </div>

        <!-- 图表区域 -->
        <div class="charts-section">
          <TechCard title="📈 提交趋势" icon="📈" class="chart-card">
            <div class="chart-container">
              <div class="chart-placeholder">
                <p class="placeholder-text">图表区域 - 等待集成ECharts</p>
                <p class="placeholder-hint">这里将显示7天提交趋势折线图</p>
              </div>
            </div>
          </TechCard>

          <div class="chart-grid">
            <TechCard title="💻 语言分布" icon="💻" class="chart-card">
              <div class="chart-container chart-small">
                <div class="chart-placeholder">
                  <p class="placeholder-text">饼图</p>
                  <p class="placeholder-hint">编程语言使用占比</p>
                </div>
              </div>
            </TechCard>

            <TechCard title="⏰ 时段分析" icon="⏰" class="chart-card">
              <div class="chart-container chart-small">
                <div class="chart-placeholder">
                  <p class="placeholder-text">柱状图</p>
                  <p class="placeholder-hint">24小时活跃度分布</p>
                </div>
              </div>
            </TechCard>
          </div>
        </div>

        <!-- 最近活动 -->
        <TechCard title="🕐 最近活动" icon="🕐" class="activity-card">
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
import { ref } from 'vue'
import AppNav from '@/components/AppNav.vue'
import TechCard from '@/components/TechCard.vue'
import StatCard from '@/components/StatCard.vue'

interface Stats {
  todayCommits: number
  codeLines: number
  streakDays: number
  workHours: number
}

interface Activity {
  id: number
  icon: string
  title: string
  time: string
  type: string
  typeLabel: string
}

// 模拟统计数据
const stats = ref<Stats>({
  todayCommits: 8,
  codeLines: 1234,
  streakDays: 42,
  workHours: 4.5
})

// 模拟最近活动
const recentActivities = ref<Activity[]>([
  {
    id: 1,
    icon: '✨',
    title: 'feat: 添加用户认证功能',
    time: '2分钟前',
    type: 'feat',
    typeLabel: '功能'
  },
  {
    id: 2,
    icon: '🐛',
    title: 'fix: 修复登录页面样式问题',
    time: '15分钟前',
    type: 'fix',
    typeLabel: '修复'
  },
  {
    id: 3,
    icon: '📝',
    title: 'docs: 更新API文档',
    time: '1小时前',
    type: 'docs',
    typeLabel: '文档'
  },
  {
    id: 4,
    icon: '🎨',
    title: 'style: 优化按钮组件样式',
    time: '2小时前',
    type: 'style',
    typeLabel: '样式'
  },
  {
    id: 5,
    icon: '⚡',
    title: 'perf: 优化数据加载性能',
    time: '3小时前',
    type: 'perf',
    typeLabel: '性能'
  }
])
</script>

<style scoped>
.dashboard-view {
  min-height: 100vh;
  background: var(--bg-primary);
}

.dashboard-content {
  padding: var(--spacing-2xl) 0;
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