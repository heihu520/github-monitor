<template>
  <div 
    class="milestone-badge" 
    :class="[
      `milestone-badge--${milestone.level}`,
      { 'milestone-badge--locked': !milestone.unlocked }
    ]"
    @mouseenter="showTooltip = true"
    @mouseleave="showTooltip = false"
  >
    <!-- 徽章图标 -->
    <div class="badge-icon">
      <span class="icon-emoji">{{ milestone.icon }}</span>
      <div v-if="!milestone.unlocked" class="lock-overlay">🔒</div>
    </div>
    
    <!-- 徽章等级指示器 -->
    <div class="badge-level-indicator"></div>
    
    <!-- 进度条（未解锁时显示） -->
    <div v-if="!milestone.unlocked && milestone.progress !== undefined" class="badge-progress">
      <div 
        class="badge-progress-bar" 
        :style="{ width: `${progressPercentage}%` }"
      ></div>
    </div>
    
    <!-- 悬停提示卡片 -->
    <Transition name="tooltip">
      <div v-if="showTooltip" class="badge-tooltip">
        <div class="tooltip-header">
          <span class="tooltip-icon">{{ milestone.icon }}</span>
          <span class="tooltip-level" :class="`level-${milestone.level}`">
            {{ levelLabel }}
          </span>
        </div>
        <div class="tooltip-title">{{ milestone.title }}</div>
        <div class="tooltip-description">{{ milestone.description }}</div>
        
        <!-- 已解锁信息 -->
        <div v-if="milestone.unlocked && milestone.unlockedAt" class="tooltip-unlocked">
          <span class="unlock-icon">✨</span>
          <span class="unlock-date">{{ formatDate(milestone.unlockedAt) }} 解锁</span>
        </div>
        
        <!-- 进度信息 -->
        <div v-else-if="milestone.progress !== undefined" class="tooltip-progress">
          <div class="progress-text">
            进度: {{ milestone.progress }} / {{ milestone.target }}
          </div>
          <div class="progress-bar-container">
            <div 
              class="progress-bar-fill" 
              :style="{ width: `${progressPercentage}%` }"
            ></div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Milestone } from '@/stores/stats'

interface Props {
  milestone: Milestone
}

const props = defineProps<Props>()

const showTooltip = ref(false)

// 计算进度百分比
const progressPercentage = computed(() => {
  if (!props.milestone.progress || !props.milestone.target) return 0
  return Math.min(100, (props.milestone.progress / props.milestone.target) * 100)
})

// 等级标签
const levelLabel = computed(() => {
  const labels = {
    bronze: '青铜',
    silver: '白银',
    gold: '黄金',
    diamond: '钻石',
    legendary: '传奇'
  }
  return labels[props.milestone.level]
})

// 格式化日期
function formatDate(date: Date) {
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
</script>

<style scoped>
.milestone-badge {
  position: relative;
  width: 72px;
  height: 72px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.milestone-badge:hover {
  transform: translateY(-4px) scale(1.05);
}

/* 徽章图标容器 */
.badge-icon {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 3px solid;
  background: var(--bg-card);
  transition: all 0.3s ease;
}

/* Emoji图标 */
.icon-emoji {
  font-size: 2rem;
  line-height: 1;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

/* 锁定覆盖层 */
.lock-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.milestone-badge--locked .lock-overlay {
  opacity: 0.8;
}

.milestone-badge--locked .icon-emoji {
  opacity: 0.3;
  filter: grayscale(100%);
}

/* 等级指示器 */
.badge-level-indicator {
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid var(--bg-primary);
  transition: all 0.3s ease;
}

/* 青铜徽章 */
.milestone-badge--bronze .badge-icon {
  border-color: #cd7f32;
  box-shadow: 0 0 20px rgba(205, 127, 50, 0.4);
}

.milestone-badge--bronze .badge-level-indicator {
  background: linear-gradient(135deg, #cd7f32 0%, #b8860b 100%);
}

.milestone-badge--bronze:hover .badge-icon {
  box-shadow: 0 0 30px rgba(205, 127, 50, 0.6);
}

/* 白银徽章 */
.milestone-badge--silver .badge-icon {
  border-color: #c0c0c0;
  box-shadow: 0 0 20px rgba(192, 192, 192, 0.4);
}

.milestone-badge--silver .badge-level-indicator {
  background: linear-gradient(135deg, #c0c0c0 0%, #a8a8a8 100%);
}

.milestone-badge--silver:hover .badge-icon {
  box-shadow: 0 0 30px rgba(192, 192, 192, 0.6);
}

/* 黄金徽章 */
.milestone-badge--gold .badge-icon {
  border-color: #ffd700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}

.milestone-badge--gold .badge-level-indicator {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
}

.milestone-badge--gold:hover .badge-icon {
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
}

/* 钻石徽章 */
.milestone-badge--diamond .badge-icon {
  border-color: #b9f2ff;
  box-shadow: 0 0 20px rgba(185, 242, 255, 0.5);
}

.milestone-badge--diamond .badge-level-indicator {
  background: linear-gradient(135deg, #b9f2ff 0%, #66d9ef 100%);
}

.milestone-badge--diamond:hover .badge-icon {
  box-shadow: 0 0 30px rgba(185, 242, 255, 0.7);
}

/* 传奇徽章 */
.milestone-badge--legendary .badge-icon {
  border-color: #ff6ec7;
  box-shadow: 0 0 20px rgba(255, 110, 199, 0.5);
  animation: legendary-pulse 2s ease-in-out infinite;
}

.milestone-badge--legendary .badge-level-indicator {
  background: linear-gradient(135deg, #ff6ec7 0%, #ffa500 50%, #ff6ec7 100%);
  background-size: 200% 200%;
  animation: legendary-gradient 3s ease infinite;
}

.milestone-badge--legendary:hover .badge-icon {
  box-shadow: 0 0 40px rgba(255, 110, 199, 0.8);
}

/* 锁定状态 */
.milestone-badge--locked .badge-icon {
  border-color: var(--border-subtle);
  box-shadow: none;
  background: var(--bg-secondary);
}

.milestone-badge--locked .badge-level-indicator {
  background: var(--text-disabled);
}

/* 进度条 */
.badge-progress {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 50px;
  height: 3px;
  background: rgba(155, 163, 176, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.badge-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-blue), var(--primary-purple));
  border-radius: 2px;
  transition: width 0.5s ease;
}

/* 提示卡片 */
.badge-tooltip {
  position: absolute;
  bottom: calc(100% + 12px);
  left: 50%;
  transform: translateX(-50%);
  min-width: 240px;
  max-width: 320px;
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), var(--shadow-glow-blue);
  z-index: 100;
  pointer-events: none;
  white-space: normal;
  word-wrap: break-word;
}

.badge-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: var(--border-primary);
}

.tooltip-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.tooltip-icon {
  font-size: 1.25rem;
}

.tooltip-level {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.level-bronze {
  background: rgba(205, 127, 50, 0.2);
  color: #cd7f32;
}

.level-silver {
  background: rgba(192, 192, 192, 0.2);
  color: #c0c0c0;
}

.level-gold {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.level-diamond {
  background: rgba(185, 242, 255, 0.2);
  color: #b9f2ff;
}

.level-legendary {
  background: linear-gradient(90deg, rgba(255, 110, 199, 0.2), rgba(255, 165, 0, 0.2));
  color: #ff6ec7;
}

.tooltip-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.tooltip-description {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
}

.tooltip-unlocked {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--border-subtle);
  font-size: 0.75rem;
  color: var(--primary-green);
}

.unlock-icon {
  font-size: 1rem;
}

.tooltip-progress {
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--border-subtle);
}

.progress-text {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  margin-bottom: var(--spacing-xs);
}

.progress-bar-container {
  height: 6px;
  background: rgba(155, 163, 176, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-blue), var(--primary-purple));
  border-radius: 3px;
  transition: width 0.3s ease;
}

/* 提示卡片过渡动画 */
.tooltip-enter-active,
.tooltip-leave-active {
  transition: all 0.2s ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(4px);
}

/* 传奇徽章动画 */
@keyframes legendary-pulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(255, 110, 199, 0.5);
  }
  50% {
    box-shadow: 0 0 40px rgba(255, 110, 199, 0.8);
  }
}

@keyframes legendary-gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>