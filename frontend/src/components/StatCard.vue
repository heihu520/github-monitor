<template>
  <div class="stat-card" :class="`stat-card--${variant}`">
    <div class="stat-icon">{{ icon }}</div>
    <div class="stat-content">
      <div class="stat-label">{{ label }}</div>
      <div class="stat-value">
        <CountUp :value="value" :duration="1.5" />
        <span v-if="unit" class="stat-unit">{{ unit }}</span>
      </div>
      <div v-if="trend !== undefined" class="stat-trend" :class="trendClass">
        <span class="trend-icon">{{ trendIcon }}</span>
        <span class="trend-value">{{ Math.abs(trend) }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import CountUp from './CountUp.vue'

interface Props {
  icon: string
  label: string
  value: number
  unit?: string
  trend?: number
  variant?: 'primary' | 'success' | 'warning' | 'danger'
}

const props = withDefaults(defineProps<Props>(), {
  unit: '',
  variant: 'primary'
})

const trendClass = computed(() => ({
  'trend-up': props.trend !== undefined && props.trend > 0,
  'trend-down': props.trend !== undefined && props.trend < 0,
  'trend-neutral': props.trend === 0
}))

const trendIcon = computed(() => {
  if (props.trend === undefined) return ''
  if (props.trend > 0) return '↑'
  if (props.trend < 0) return '↓'
  return '→'
})
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--primary-blue);
  transition: width 0.3s ease;
}

.stat-card:hover {
  border-color: var(--border-primary);
  box-shadow: var(--shadow-glow-blue);
  transform: translateY(-2px);
}

.stat-card:hover::before {
  width: 6px;
}

/* 变体颜色 */
.stat-card--primary::before {
  background: var(--primary-blue);
}

.stat-card--success::before {
  background: var(--primary-green);
}

.stat-card--warning::before {
  background: var(--primary-orange);
}

.stat-card--danger::before {
  background: var(--primary-red);
}

/* 图标 */
.stat-icon {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  background: rgba(74, 144, 226, 0.1);
  border-radius: var(--radius-md);
  filter: drop-shadow(0 0 8px rgba(74, 144, 226, 0.3));
}

.stat-card--success .stat-icon {
  background: rgba(82, 196, 26, 0.1);
  filter: drop-shadow(0 0 8px rgba(82, 196, 26, 0.3));
}

.stat-card--warning .stat-icon {
  background: rgba(250, 140, 22, 0.1);
  filter: drop-shadow(0 0 8px rgba(250, 140, 22, 0.3));
}

.stat-card--danger .stat-icon {
  background: rgba(245, 34, 45, 0.1);
  filter: drop-shadow(0 0 8px rgba(245, 34, 45, 0.3));
}

/* 内容 */
.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.stat-value {
  font-family: var(--font-mono);
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.stat-unit {
  font-size: 1rem;
  color: var(--text-tertiary);
  font-weight: 400;
}

/* 趋势 */
.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 6px;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.trend-up {
  background: rgba(82, 196, 26, 0.15);
  color: var(--primary-green);
}

.trend-down {
  background: rgba(245, 34, 45, 0.15);
  color: var(--primary-red);
}

.trend-neutral {
  background: rgba(155, 163, 176, 0.15);
  color: var(--text-secondary);
}

.trend-icon {
  font-size: 0.875rem;
}

/* 响应式 */
@media (max-width: 768px) {
  .stat-card {
    padding: var(--spacing-md);
    gap: var(--spacing-md);
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    font-size: 1.5rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }
}
</style>