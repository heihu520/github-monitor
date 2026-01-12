<template>
  <div class="tech-card" :class="{ 'is-loading': loading, 'is-hoverable': hoverable }">
    <!-- 卡片头部 -->
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <div class="header-content">
          <span v-if="icon" class="card-icon">{{ icon }}</span>
          <h3 class="card-title">{{ title }}</h3>
        </div>
      </slot>
      <div v-if="$slots.extra" class="header-extra">
        <slot name="extra"></slot>
      </div>
    </div>

    <!-- 卡片主体 -->
    <div class="card-body">
      <slot></slot>
    </div>

    <!-- 卡片底部 -->
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  icon?: string
  loading?: boolean
  hoverable?: boolean
}

withDefaults(defineProps<Props>(), {
  title: '',
  icon: '',
  loading: false,
  hoverable: true
})
</script>

<style scoped>
.tech-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-card);
}

.tech-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(74, 144, 226, 0.05),
    transparent
  );
  transition: left 0.6s ease;
}

.tech-card.is-hoverable:hover {
  transform: translateY(-2px);
  border-color: var(--border-primary);
  box-shadow: var(--shadow-glow-blue);
}

.tech-card.is-hoverable:hover::before {
  left: 100%;
}

/* 卡片头部 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-subtle);
}

.header-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.card-icon {
  font-size: 1.5rem;
  line-height: 1;
  filter: drop-shadow(0 0 4px currentColor);
}

.card-title {
  font-family: var(--font-title);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.header-extra {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

/* 卡片主体 */
.card-body {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* 卡片底部 */
.card-footer {
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-subtle);
}

/* 加载状态 */
.tech-card.is-loading {
  pointer-events: none;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 20, 25, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(2px);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--primary-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .tech-card {
    padding: var(--spacing-md);
  }

  .card-header {
    margin-bottom: var(--spacing-sm);
    padding-bottom: var(--spacing-sm);
  }

  .card-title {
    font-size: 1rem;
  }
}
</style>