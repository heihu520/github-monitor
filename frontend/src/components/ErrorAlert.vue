<template>
  <div class="error-alert" :class="typeClass">
    <div class="alert-icon">⚠️</div>
    <div class="alert-content">
      <div class="alert-title">{{ title }}</div>
      <div class="alert-message">{{ message }}</div>
    </div>
    <div class="alert-actions">
      <button v-if="showRetry" class="btn-retry" @click="handleRetry">
        重试
      </button>
      <button v-if="showClose" class="btn-close" @click="handleClose">
        ✕
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  message: string
  type?: 'error' | 'warning' | 'info'
  showRetry?: boolean
  showClose?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '错误',
  type: 'error',
  showRetry: true,
  showClose: true
})

const emit = defineEmits<{
  retry: []
  close: []
}>()

const typeClass = computed(() => `alert-${props.type}`)

function handleRetry() {
  emit('retry')
}

function handleClose() {
  emit('close')
}
</script>

<style scoped>
.error-alert {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid;
  backdrop-filter: blur(10px);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 错误类型 */
.alert-error {
  border-color: var(--neon-red, #ff4757);
  background: rgba(255, 71, 87, 0.1);
}

.alert-error .alert-icon {
  color: var(--neon-red, #ff4757);
  text-shadow: 0 0 10px var(--neon-red, #ff4757);
}

/* 警告类型 */
.alert-warning {
  border-color: var(--neon-yellow, #ffa502);
  background: rgba(255, 165, 2, 0.1);
}

.alert-warning .alert-icon {
  color: var(--neon-yellow, #ffa502);
  text-shadow: 0 0 10px var(--neon-yellow, #ffa502);
}

/* 信息类型 */
.alert-info {
  border-color: var(--neon-blue, #00d4ff);
  background: rgba(0, 212, 255, 0.1);
}

.alert-info .alert-icon {
  color: var(--neon-blue, #00d4ff);
  text-shadow: 0 0 10px var(--neon-blue, #00d4ff);
}

/* 图标 */
.alert-icon {
  font-size: 24px;
  flex-shrink: 0;
}

/* 内容区 */
.alert-content {
  flex: 1;
  min-width: 0;
}

.alert-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary, #ffffff);
  margin-bottom: 0.25rem;
}

.alert-message {
  font-size: 14px;
  color: var(--text-secondary, #a0aec0);
  line-height: 1.5;
  word-break: break-word;
}

/* 操作按钮 */
.alert-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.btn-retry,
.btn-close {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary, #ffffff);
}

.btn-retry {
  border: 1px solid var(--neon-blue, #00d4ff);
  color: var(--neon-blue, #00d4ff);
}

.btn-retry:hover {
  background: var(--neon-blue, #00d4ff);
  color: #000;
  box-shadow: 0 0 15px var(--neon-blue, #00d4ff);
  transform: translateY(-1px);
}

.btn-close {
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
  padding: 0.5rem 0.75rem;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: var(--text-secondary, #a0aec0);
}

.btn-retry:active,
.btn-close:active {
  transform: translateY(0);
}

/* 响应式 */
@media (max-width: 768px) {
  .error-alert {
    flex-direction: column;
    align-items: flex-start;
  }

  .alert-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>