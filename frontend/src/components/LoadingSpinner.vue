<template>
  <div class="loading-spinner" :class="sizeClass">
    <div class="spinner-ring"></div>
    <div class="spinner-ring"></div>
    <div class="spinner-ring"></div>
    <div class="loading-text" v-if="text">{{ text }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'small' | 'medium' | 'large'
  text?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'medium',
  text: ''
})

const sizeClass = computed(() => `spinner-${props.size}`)
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

/* 旋转动画容器 */
.loading-spinner {
  position: relative;
}

/* 霓虹蓝环 */
.spinner-ring {
  position: absolute;
  border-radius: 50%;
  border: 3px solid transparent;
  border-top-color: var(--neon-blue, #00d4ff);
  animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
}

.spinner-ring:nth-child(1) {
  border-top-color: var(--neon-blue, #00d4ff);
  box-shadow: 0 0 20px var(--neon-blue, #00d4ff);
}

.spinner-ring:nth-child(2) {
  border-top-color: var(--neon-purple, #b24bf3);
  box-shadow: 0 0 20px var(--neon-purple, #b24bf3);
  animation-delay: 0.2s;
}

.spinner-ring:nth-child(3) {
  border-top-color: var(--neon-cyan, #00f5ff);
  box-shadow: 0 0 20px var(--neon-cyan, #00f5ff);
  animation-delay: 0.4s;
}

/* 小尺寸 */
.spinner-small {
  width: 30px;
  height: 30px;
}

.spinner-small .spinner-ring {
  width: 30px;
  height: 30px;
  border-width: 2px;
}

.spinner-small .spinner-ring:nth-child(2) {
  width: 24px;
  height: 24px;
  top: 3px;
  left: 3px;
}

.spinner-small .spinner-ring:nth-child(3) {
  width: 18px;
  height: 18px;
  top: 6px;
  left: 6px;
}

/* 中等尺寸 */
.spinner-medium {
  width: 50px;
  height: 50px;
}

.spinner-medium .spinner-ring {
  width: 50px;
  height: 50px;
  border-width: 3px;
}

.spinner-medium .spinner-ring:nth-child(2) {
  width: 40px;
  height: 40px;
  top: 5px;
  left: 5px;
}

.spinner-medium .spinner-ring:nth-child(3) {
  width: 30px;
  height: 30px;
  top: 10px;
  left: 10px;
}

/* 大尺寸 */
.spinner-large {
  width: 80px;
  height: 80px;
}

.spinner-large .spinner-ring {
  width: 80px;
  height: 80px;
  border-width: 4px;
}

.spinner-large .spinner-ring:nth-child(2) {
  width: 64px;
  height: 64px;
  top: 8px;
  left: 8px;
}

.spinner-large .spinner-ring:nth-child(3) {
  width: 48px;
  height: 48px;
  top: 16px;
  left: 16px;
}

/* 旋转动画 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 加载文本 */
.loading-text {
  margin-top: 3rem;
  font-size: 14px;
  color: var(--text-secondary, #a0aec0);
  text-align: center;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

/* 科技风格增强 */
.loading-spinner::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(0, 212, 255, 0.1) 0%,
    transparent 70%
  );
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    transform: scale(0.95);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
}
</style>