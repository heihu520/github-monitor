<template>
  <button
    class="tech-button"
    :class="[
      `tech-button--${type}`,
      `tech-button--${size}`,
      {
        'is-loading': loading,
        'is-disabled': disabled,
        'is-block': block
      }
    ]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="icon && !loading" class="button-icon">{{ icon }}</span>
    <span v-if="loading" class="button-loader"></span>
    <span class="button-text"><slot></slot></span>
  </button>
</template>

<script setup lang="ts">
interface Props {
  type?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'ghost'
  size?: 'small' | 'medium' | 'large'
  icon?: string
  loading?: boolean
  disabled?: boolean
  block?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'primary',
  size: 'medium',
  icon: '',
  loading: false,
  disabled: false,
  block: false
})

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const handleClick = (event: MouseEvent) => {
  if (!props.loading && !props.disabled) {
    emit('click', event)
  }
}
</script>

<style scoped>
.tech-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #fff;
  background: var(--gradient-primary);
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
}

.tech-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.4s;
}

.tech-button:hover:not(.is-disabled):not(.is-loading)::before {
  left: 100%;
}

.tech-button:hover:not(.is-disabled):not(.is-loading) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow-blue);
}

.tech-button:active:not(.is-disabled):not(.is-loading) {
  transform: translateY(0);
}

/* 按钮类型 */
.tech-button--primary {
  background: var(--gradient-primary);
}

.tech-button--secondary {
  background: linear-gradient(135deg, #6B7280 0%, #4B5563 100%);
}

.tech-button--success {
  background: var(--gradient-success);
}

.tech-button--warning {
  background: var(--gradient-warning);
}

.tech-button--danger {
  background: var(--gradient-danger);
}

.tech-button--ghost {
  background: transparent;
  border: 1px solid var(--primary-blue);
  color: var(--primary-blue);
}

.tech-button--ghost:hover:not(.is-disabled):not(.is-loading) {
  background: rgba(74, 144, 226, 0.1);
  border-color: var(--primary-purple);
  color: var(--primary-purple);
}

/* 按钮尺寸 */
.tech-button--small {
  padding: 6px 12px;
  font-size: 0.75rem;
}

.tech-button--medium {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: 0.875rem;
}

.tech-button--large {
  padding: 12px 24px;
  font-size: 1rem;
}

/* 按钮状态 */
.tech-button.is-loading,
.tech-button.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.tech-button.is-block {
  width: 100%;
}

/* 图标 */
.button-icon {
  font-size: 1.125rem;
  line-height: 1;
}

/* 加载器 */
.button-loader {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .tech-button {
    font-size: 0.75rem;
  }

  .tech-button--large {
    padding: 10px 20px;
    font-size: 0.875rem;
  }
}
</style>