<template>
  <div class="app">
    <!-- 赛博朋克背景效果 -->
    <div class="cyber-bg">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
    </div>

    <!-- 主内容区 -->
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup lang="ts">
// App根组件 - 赛博朋克风格个人代码追踪系统
</script>

<style scoped>
.app {
  position: relative;
  width: 100%;
  min-height: 100vh;
}

/* 赛博朋克背景 */
.cyber-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(var(--grid-line) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
  background-size: 50px 50px;
  opacity: 0.5;
}

/* 扫描线动画 */
.scan-line {
  position: absolute;
  top: -100%;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--primary-blue),
    transparent
  );
  box-shadow: 0 0 20px var(--primary-blue);
  animation: scan 8s linear infinite;
}

@keyframes scan {
  0% {
    top: -100%;
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    top: 100%;
    opacity: 0;
  }
}

/* 路由过渡动画 - 简单淡入淡出避免抖动 */
.fade-enter-active {
  transition: opacity 0.15s ease-in;
}

.fade-leave-active {
  transition: opacity 0.15s ease-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .scan-line {
    display: none;
  }
  
  .grid-overlay {
    opacity: 0.3;
    background-size: 30px 30px;
  }
}
</style>