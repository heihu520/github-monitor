<template>
  <div class="trends-view">
    <AppNav />
    
    <div class="container">
      <div class="trends-content">
        <div class="page-header">
          <h1 class="page-title">📈 趋势分析</h1>
          <p class="page-subtitle">深入了解你的编码趋势和模式</p>
        </div>

        <TechCard title="即将推出" icon="🚀">
          <div class="coming-soon">
            <p class="coming-soon-text">趋势分析功能正在开发中...</p>
            <p class="coming-soon-hint">敬请期待更详细的数据分析和可视化</p>
          </div>
        </TechCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppNav from '@/components/AppNav.vue'
import TechCard from '@/components/TechCard.vue'
</script>

<style scoped>
.trends-view {
  min-height: 100vh;
  background: var(--bg-primary);
}

.trends-content {
  padding: var(--spacing-2xl) 0;
}

.page-header {
  margin-bottom: var(--spacing-2xl);
  text-align: center;
}

.page-title {
  margin-bottom: var(--spacing-sm);
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
}

.coming-soon {
  padding: var(--spacing-2xl);
  text-align: center;
}

.coming-soon-text {
  font-size: 1.25rem;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.coming-soon-hint {
  color: var(--text-tertiary);
}
</style>