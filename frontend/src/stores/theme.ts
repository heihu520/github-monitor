import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

/**
 * 主题配色方案类型
 */
export type ThemeColor = 
  | 'classic-blue-purple'  // 经典蓝紫（默认）
  | 'neon-pink-green'      // 霓虹粉绿（活力）
  | 'orange-yellow-cyber'  // 橙黄赛博（温暖）
  | 'ice-blue-white'       // 冰蓝白（清冷）
  | 'red-black-hacker'     // 红黑骇客（Matrix风）

/**
 * 主题模式类型
 */
export type ThemeMode = 'dark' | 'light' | 'high-contrast'

/**
 * 主题配置接口
 */
export interface ThemeConfig {
  colorScheme: ThemeColor
  mode: ThemeMode
  glowIntensity: number      // 发光强度 0-100
  animationSpeed: number     // 动画速度 0.5-2
  backgroundEffect: boolean  // 背景效果开关
  reducedMotion: boolean     // 减弱动画（无障碍）
  fontSize: number           // 基础字体大小 14-18
}

/**
 * 配色方案定义
 */
const colorSchemes: Record<ThemeColor, {
  primary: string
  secondary: string
  accent: string
  success: string
}> = {
  'classic-blue-purple': {
    primary: '#4A90E2',
    secondary: '#7C5CDB',
    accent: '#5EC4E8',
    success: '#52C41A'
  },
  'neon-pink-green': {
    primary: '#FF006E',
    secondary: '#B300FF',
    accent: '#39FF14',
    success: '#00FF9F'
  },
  'orange-yellow-cyber': {
    primary: '#FF6B00',
    secondary: '#FAAD14',
    accent: '#FFD700',
    success: '#52C41A'
  },
  'ice-blue-white': {
    primary: '#00F0FF',
    secondary: '#8AB4F8',
    accent: '#E8F4FF',
    success: '#00E5A0'
  },
  'red-black-hacker': {
    primary: '#FF0000',
    secondary: '#DC143C',
    accent: '#00FF00',
    success: '#00FF00'
  }
}

/**
 * 主题配置管理 Store
 * 管理主题颜色、模式、动画效果等个性化设置
 */
export const useThemeStore = defineStore('theme', () => {
  // 主题配置
  const config = ref<ThemeConfig>({
    colorScheme: 'classic-blue-purple',
    mode: 'dark',
    glowIntensity: 70,
    animationSpeed: 1,
    backgroundEffect: true,
    reducedMotion: false,
    fontSize: 16
  })

  // 是否正在应用主题
  const isApplying = ref<boolean>(false)

  /**
   * 设置配色方案
   */
  function setColorScheme(scheme: ThemeColor) {
    config.value.colorScheme = scheme
    applyTheme()
  }

  /**
   * 设置主题模式
   */
  function setThemeMode(mode: ThemeMode) {
    config.value.mode = mode
    applyTheme()
  }

  /**
   * 设置发光强度
   */
  function setGlowIntensity(intensity: number) {
    config.value.glowIntensity = Math.max(0, Math.min(100, intensity))
    applyTheme()
  }

  /**
   * 设置动画速度
   */
  function setAnimationSpeed(speed: number) {
    config.value.animationSpeed = Math.max(0.5, Math.min(2, speed))
    applyTheme()
  }

  /**
   * 切换背景效果
   */
  function toggleBackgroundEffect() {
    config.value.backgroundEffect = !config.value.backgroundEffect
    applyTheme()
  }

  /**
   * 切换减弱动画模式
   */
  function toggleReducedMotion() {
    config.value.reducedMotion = !config.value.reducedMotion
    applyTheme()
  }

  /**
   * 设置基础字体大小
   */
  function setFontSize(size: number) {
    config.value.fontSize = Math.max(14, Math.min(18, size))
    applyTheme()
  }

  /**
   * 应用主题到DOM
   */
  function applyTheme() {
    isApplying.value = true
    
    try {
      const root = document.documentElement
      const scheme = colorSchemes[config.value.colorScheme]
      
      // 应用配色方案
      root.style.setProperty('--primary-blue', scheme.primary)
      root.style.setProperty('--primary-purple', scheme.secondary)
      root.style.setProperty('--primary-cyan', scheme.accent)
      root.style.setProperty('--primary-green', scheme.success)
      
      // 应用发光强度
      const glowOpacity = config.value.glowIntensity / 100
      root.style.setProperty('--glow-opacity', glowOpacity.toString())
      
      // 应用动画速度
      root.style.setProperty('--animation-speed', config.value.animationSpeed.toString())
      
      // 应用字体大小
      root.style.fontSize = `${config.value.fontSize}px`
      
      // 应用背景效果
      if (config.value.backgroundEffect) {
        root.classList.remove('no-background')
      } else {
        root.classList.add('no-background')
      }
      
      // 应用减弱动画
      if (config.value.reducedMotion) {
        root.classList.add('reduced-motion')
      } else {
        root.classList.remove('reduced-motion')
      }
      
      // 应用主题模式
      root.setAttribute('data-theme', config.value.mode)
      
      // 保存配置
      saveConfig()
    } catch (error) {
      console.error('Failed to apply theme:', error)
    } finally {
      isApplying.value = false
    }
  }

  /**
   * 保存配置到localStorage
   */
  function saveConfig() {
    try {
      localStorage.setItem('themeConfig', JSON.stringify(config.value))
    } catch (error) {
      console.error('Failed to save theme config:', error)
    }
  }

  /**
   * 从localStorage恢复配置
   */
  function restoreConfig() {
    try {
      const saved = localStorage.getItem('themeConfig')
      if (saved) {
        const savedConfig = JSON.parse(saved)
        config.value = { ...config.value, ...savedConfig }
        applyTheme()
      }
    } catch (error) {
      console.error('Failed to restore theme config:', error)
    }
  }

  /**
   * 导出主题配置为JSON
   */
  function exportConfig(): string {
    return JSON.stringify(config.value, null, 2)
  }

  /**
   * 导入主题配置从JSON
   */
  function importConfig(jsonStr: string): boolean {
    try {
      const imported = JSON.parse(jsonStr) as ThemeConfig
      config.value = imported
      applyTheme()
      return true
    } catch (error) {
      console.error('Failed to import theme config:', error)
      return false
    }
  }

  /**
   * 重置为默认主题
   */
  function resetToDefault() {
    config.value = {
      colorScheme: 'classic-blue-purple',
      mode: 'dark',
      glowIntensity: 70,
      animationSpeed: 1,
      backgroundEffect: true,
      reducedMotion: false,
      fontSize: 16
    }
    applyTheme()
  }

  /**
   * 检测系统主题偏好
   */
  function detectSystemPreference() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    
    if (prefersDark) {
      config.value.mode = 'dark'
    } else {
      config.value.mode = 'light'
    }
    
    if (prefersReducedMotion) {
      config.value.reducedMotion = true
    }
    
    applyTheme()
  }

  // 监听配置变化自动保存
  watch(config, () => {
    saveConfig()
  }, { deep: true })

  // 初始化时应用主题
  applyTheme()

  return {
    // State
    config,
    isApplying,
    
    // Getters
    colorSchemes,
    
    // Actions
    setColorScheme,
    setThemeMode,
    setGlowIntensity,
    setAnimationSpeed,
    toggleBackgroundEffect,
    toggleReducedMotion,
    setFontSize,
    applyTheme,
    saveConfig,
    restoreConfig,
    exportConfig,
    importConfig,
    resetToDefault,
    detectSystemPreference
  }
})