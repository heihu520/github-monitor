<template>
  <nav class="app-nav">
    <div class="nav-wrapper">
      <div class="container nav-content">
        <!-- Logo -->
        <router-link to="/" class="nav-logo">
          <span class="logo-icon">💻</span>
          <span class="logo-text">CODE TRACKER</span>
        </router-link>

        <!-- 导航菜单 -->
        <div class="nav-menu">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
          >
            <span class="item-icon">{{ item.icon }}</span>
            <span class="item-text">{{ item.label }}</span>
          </router-link>
        </div>

        <!-- 用户区域 -->
        <div class="nav-user">
          <TechButton
            size="medium"
            type="primary"
            icon="🔄"
            :loading="isSyncing"
            @click="handleSync"
          >
            {{ isSyncing ? '同步中...' : '同步数据' }}
          </TechButton>
          <TechButton size="medium" type="ghost" icon="⚙️">设置</TechButton>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TechButton from './TechButton.vue'
import { syncApi } from '@/services/sync'
import { useUserStore } from '@/stores/user'
import { useStatsStore } from '@/stores/stats'

interface MenuItem {
  path: string
  label: string
  icon: string
}

const menuItems = ref<MenuItem[]>([
  { path: '/dashboard', label: '仪表盘', icon: '📊' },
  { path: '/trends', label: '趋势', icon: '📈' },
  { path: '/achievements', label: '成就', icon: '🏆' }
])

const userStore = useUserStore()
const statsStore = useStatsStore()

// 同步状态
const isSyncing = ref(false)

// 同步处理函数
const handleSync = async () => {
  if (isSyncing.value) return
  
  isSyncing.value = true
  try {
    // 单用户应用，固定配置
    const userId = 1
    const username = 'heihu520'  // GitHub用户名
    const githubToken = userStore.githubToken || undefined
    
    console.log(`[同步] 用户ID: ${userId}, 用户名: ${username}`)
    
    // 使用auto模式，后端自动判断全量/增量
    const result = await syncApi.syncGithubData(userId, username, githubToken, 'auto')
    
    console.log('同步成功:', result)
    console.log(`同步模式: ${result.sync_mode}`)
    if (result.since) {
      console.log(`增量同步起始时间: ${result.since}`)
    }
    
    alert(`同步成功！模式: ${result.sync_mode === 'full' ? '全量' : '增量'}\n仓库: ${result.repos_synced} 个\n提交: ${result.commits_synced} 个`)
    
    // 同步完成后自动刷新仪表盘数据
    console.log('开始刷新仪表盘数据...')
    await statsStore.refreshAllData(userId)
    console.log('仪表盘数据刷新完成')
  } catch (error: any) {
    console.error('同步失败:', error)
    alert(`同步失败: ${error.message || '未知错误'}`)
  } finally {
    isSyncing.value = false
  }
}
</script>

<style scoped>
.app-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-overlay);
  border-bottom: 1px solid var(--border-subtle);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.nav-content {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  height: 64px;
  gap: var(--spacing-xl);
}

/* Logo */
.nav-logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  text-decoration: none;
  transition: all 0.3s ease;
}

.logo-icon {
  font-size: 1.75rem;
  line-height: 1;
  filter: drop-shadow(0 0 8px rgba(74, 144, 226, 0.5));
}

.logo-text {
  font-family: var(--font-title);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-blue);
  letter-spacing: 1px;
}

.nav-logo:hover .logo-icon {
  filter: drop-shadow(0 0 12px rgba(74, 144, 226, 0.8));
  transform: scale(1.1);
}

/* 菜单 */
.nav-menu {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-lg);
  margin-left: -125px;  /* 负值向左移，可调整大小 */
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: all 0.3s ease;
  position: relative;
}

.nav-item::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: var(--primary-blue);
  transition: width 0.3s ease;
}

.nav-item:hover {
  color: var(--text-primary);
  background: rgba(74, 144, 226, 0.1);
}

.nav-item:hover::after {
  width: 80%;
}

.nav-item.router-link-active {
  color: var(--primary-blue);
  background: rgba(74, 144, 226, 0.15);
}

.nav-item.router-link-active::after {
  width: 80%;
}

.item-icon {
  font-size: 1.25rem;
  line-height: 1;
}

.item-text {
  font-weight: 500;
  font-size: 0.875rem;
}

/* 用户区域 */
.nav-user {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

/* 响应式 */
@media (max-width: 768px) {
  .nav-content {
    height: 56px;
  }

  .logo-text {
    display: none;
  }

  .nav-menu {
    gap: 4px;
  }

  .nav-item {
    padding: 6px 10px;
  }

  .item-text {
    display: none;
  }

  .item-icon {
    font-size: 1.5rem;
  }
}
</style>