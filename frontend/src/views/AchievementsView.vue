<template>
  <div class="achievements-view">
    <AppNav />
    
    <div class="container">
      <div class="achievements-content">
        <div class="page-header">
          <h1 class="page-title">🏆 成就系统</h1>
          <p class="page-subtitle">追踪你的编码里程碑和成就</p>
        </div>

        <TechCard title="即将推出" icon="🎮">
          <div class="coming-soon">
            <p class="coming-soon-text">成就系统正在开发中...</p>
            <p class="coming-soon-hint">即将推出徽章、等级和挑战系统</p>
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
.achievements-view {
  min-height: 100vh;
  background: var(--bg-primary);
}

.achievements-content {
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