/**
 * Pinia Stores 统一导出
 * 便于在组件中导入使用
 */

export { useUserStore } from './user'
export { useStatsStore } from './stats'
export { useThemeStore } from './theme'

// 类型导出
export type { DashboardStats, Activity, LanguageStat, TrendData } from './stats'
export type { ThemeColor, ThemeMode, ThemeConfig } from './theme'