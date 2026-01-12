<template>
  <nav class="app-nav">
    <div class="container">
      <div class="nav-content">
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
          <TechButton size="small" type="ghost" icon="⚙️">设置</TechButton>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TechButton from './TechButton.vue'

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
  display: flex;
  align-items: center;
  height: 64px;
  gap: var(--spacing-2xl);
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
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 1px;
}

.nav-logo:hover .logo-icon {
  filter: drop-shadow(0 0 12px rgba(74, 144, 226, 0.8));
  transform: scale(1.1);
}

/* 菜单 */
.nav-menu {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
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