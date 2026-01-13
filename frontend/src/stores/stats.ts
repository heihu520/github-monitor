import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { dashboardApi } from '@/services/dashboard'
import type {
  DashboardOverview,
  DashboardStats as ApiDashboardStats,
  MilestoneAchievement as ApiMilestone
} from '@/services/types'

/**
 * 统计数据类型定义（本地使用，兼容旧格式）
 */
export interface DashboardStats {
  todayCommits: number
  weekCommits: number
  monthCommits: number
  codeLines: number
  streakDays: number
  workHours: number
  activeLanguage: string
  totalRepositories: number
}

export interface Activity {
  id: number
  icon: string
  title: string
  time: string
  type: string
  typeLabel: string
  timestamp: number
}

export interface LanguageStat {
  name: string
  percentage: number
  commits: number
  lines: number
  color: string
}

export interface TrendData {
  date: string
  commits: number
  additions: number
  deletions: number
}

export interface Milestone {
  id: string
  title: string
  description: string
  icon: string
  level: 'bronze' | 'silver' | 'gold' | 'diamond' | 'legendary'
  unlocked: boolean
  unlockedAt?: Date
  progress?: number
  target?: number
  category: 'coding' | 'streak' | 'language' | 'special'
}

// API数据格式转换辅助函数
function convertApiMilestone(apiMilestone: ApiMilestone): Milestone {
  return {
    id: apiMilestone.id,
    title: apiMilestone.name,
    description: apiMilestone.description,
    icon: apiMilestone.icon,
    level: apiMilestone.level,
    unlocked: apiMilestone.unlocked,
    unlockedAt: apiMilestone.unlock_date ? new Date(apiMilestone.unlock_date) : undefined,
    progress: apiMilestone.current,
    target: apiMilestone.target,
    category: 'coding' // 默认分类，后端可扩展
  }
}

export interface HeatmapData {
  date: string // YYYY-MM-DD格式
  commits: number
  level: number // 0-4，用于颜色映射
}

/**
 * 统计数据管理 Store
 * 管理仪表盘统计数据、活动记录、语言分布等
 */
export const useStatsStore = defineStore('stats', () => {
  // 仪表盘统计数据
  const dashboardStats = ref<DashboardStats>({
    todayCommits: 0,
    weekCommits: 0,
    monthCommits: 0,
    codeLines: 0,
    streakDays: 0,
    workHours: 0,
    activeLanguage: 'TypeScript',
    totalRepositories: 0
  })

  // 最近活动列表
  const recentActivities = ref<Activity[]>([])

  // 语言统计数据
  const languageStats = ref<LanguageStat[]>([])

  // 趋势数据
  const trendData = ref<TrendData[]>([])

  // 成就里程碑数据
  const milestones = ref<Milestone[]>([])

  // 年度活跃度热力图数据
  const heatmapData = ref<HeatmapData[]>([])

  // 加载和错误状态
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const lastUpdated = ref<Date | null>(null)

  // 计算属性：今日趋势（与昨日对比）
  const todayTrend = computed(() => {
    // 这里应该基于历史数据计算
    // 暂时返回模拟值
    return 15
  })

  // 计算属性：本周趋势（与上周对比）
  const weekTrend = computed(() => {
    return 8
  })

  // 计算属性：总提交数
  const totalCommits = computed(() => {
    return dashboardStats.value.todayCommits + 
           dashboardStats.value.weekCommits + 
           dashboardStats.value.monthCommits
  })

  /**
   * 更新仪表盘统计数据
   */
  function updateDashboardStats(stats: Partial<DashboardStats>) {
    dashboardStats.value = { ...dashboardStats.value, ...stats }
    lastUpdated.value = new Date()
  }

  /**
   * 添加活动记录
   */
  function addActivity(activity: Omit<Activity, 'id' | 'timestamp'>) {
    const newActivity: Activity = {
      ...activity,
      id: Date.now(),
      timestamp: Date.now()
    }
    recentActivities.value.unshift(newActivity)
    
    // 最多保留20条记录
    if (recentActivities.value.length > 20) {
      recentActivities.value = recentActivities.value.slice(0, 20)
    }
  }

  /**
   * 设置最近活动列表
   */
  function setRecentActivities(activities: Activity[]) {
    recentActivities.value = activities
  }

  /**
   * 更新语言统计数据
   */
  function updateLanguageStats(stats: LanguageStat[]) {
    languageStats.value = stats
  }

  /**
   * 更新趋势数据
   */
  function updateTrendData(data: TrendData[]) {
    trendData.value = data
  }

  /**
   * 从API获取仪表板总览数据（真实API）
   */
  async function fetchDashboardData(userId: number = 1) {
    isLoading.value = true
    error.value = null
    
    try {
      const overview = await dashboardApi.getOverview(userId)
      
      // 转换API数据格式到本地格式
      updateDashboardStats({
        todayCommits: overview.stats.today_commits,
        weekCommits: overview.stats.week_commits,
        monthCommits: overview.stats.month_commits,
        codeLines: overview.stats.code_lines,
        streakDays: overview.stats.streak_days,
        workHours: overview.stats.work_hours,
        activeLanguage: overview.stats.active_language,
        totalRepositories: overview.stats.total_repositories
      })
      
      // 更新里程碑数据（检查是否存在）
      if (overview.milestones && Array.isArray(overview.milestones)) {
        milestones.value = overview.milestones.map(convertApiMilestone)
      }
      
      // 更新趋势数据（检查是否存在）
      if (overview.trend_data && Array.isArray(overview.trend_data)) {
        trendData.value = overview.trend_data.map(point => ({
          date: point.date,
          commits: point.commits,
          additions: point.additions,
          deletions: point.deletions
        }))
      }
      
      // 更新热力图数据（检查是否存在）
      if (overview.heatmap_data && Array.isArray(overview.heatmap_data)) {
        heatmapData.value = overview.heatmap_data.map(point => ({
          date: point.date,
          commits: point.count,
          level: point.level
        }))
      }
      
      // 更新语言统计（检查是否存在）
      if (overview.language_stats && Array.isArray(overview.language_stats)) {
        languageStats.value = overview.language_stats.map(lang => ({
          name: lang.language,
          percentage: lang.percentage,
          commits: 0, // 后端可扩展
          lines: lang.lines,
          color: lang.color || '#3178c6'
        }))
      }
      
      lastUpdated.value = new Date()
    } catch (err: any) {
      error.value = err.message || '获取数据失败'
      console.error('Failed to fetch dashboard data:', err)
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 从API获取统计数据（单独获取）
   */
  async function fetchDashboardStats(userId: number = 1) {
    isLoading.value = true
    error.value = null
    
    try {
      const stats = await dashboardApi.getStats(userId)
      
      updateDashboardStats({
        todayCommits: stats.today_commits,
        weekCommits: stats.week_commits,
        monthCommits: stats.month_commits,
        codeLines: stats.code_lines,
        streakDays: stats.streak_days,
        workHours: stats.work_hours,
        activeLanguage: stats.active_language,
        totalRepositories: stats.total_repositories
      })
      
      lastUpdated.value = new Date()
    } catch (err: any) {
      error.value = err.message || '获取统计数据失败'
      console.error('Failed to fetch dashboard stats:', err)
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 从API获取最近活动
   */
  async function fetchRecentActivities() {
    try {
      // TODO: 实际API调用
      // const response = await api.getRecentActivities()
      // setRecentActivities(response.data)
      
      // 暂时使用模拟数据
      setRecentActivities([
        {
          id: 1,
          icon: '✨',
          title: 'feat: 添加用户认证功能',
          time: '2分钟前',
          type: 'feat',
          typeLabel: '功能',
          timestamp: Date.now() - 2 * 60 * 1000
        },
        {
          id: 2,
          icon: '🐛',
          title: 'fix: 修复登录页面样式问题',
          time: '15分钟前',
          type: 'fix',
          typeLabel: '修复',
          timestamp: Date.now() - 15 * 60 * 1000
        },
        {
          id: 3,
          icon: '📝',
          title: 'docs: 更新API文档',
          time: '1小时前',
          type: 'docs',
          typeLabel: '文档',
          timestamp: Date.now() - 60 * 60 * 1000
        }
      ])
    } catch (error) {
      console.error('Failed to fetch recent activities:', error)
    }
  }

  /**
   * 从API获取语言统计
   */
  async function fetchLanguageStats() {
    try {
      // TODO: 实际API调用
      // const response = await api.getLanguageStats()
      // updateLanguageStats(response.data)
      
      // 暂时使用模拟数据 - 更多编程语言
      updateLanguageStats([
        { name: 'TypeScript', percentage: 28, commits: 95, lines: 4200, color: '#3178c6' },
        { name: 'Python', percentage: 22, commits: 75, lines: 3500, color: '#3776ab' },
        { name: 'JavaScript', percentage: 18, commits: 60, lines: 2800, color: '#f7df1e' },
        { name: 'Vue', percentage: 12, commits: 40, lines: 1800, color: '#42b883' },
        { name: 'Go', percentage: 8, commits: 28, lines: 1200, color: '#00add8' },
        { name: 'Rust', percentage: 6, commits: 20, lines: 900, color: '#ce422b' },
        { name: 'Java', percentage: 4, commits: 15, lines: 600, color: '#ea2d2e' },
        { name: 'C++', percentage: 2, commits: 7, lines: 300, color: '#00599c' }
      ])
    } catch (error) {
      console.error('Failed to fetch language stats:', error)
    }
  }

  /**
   * 从API获取趋势数据
   */
  async function fetchTrendData(days: number = 7) {
    try {
      // TODO: 实际API调用
      // const response = await api.getTrendData(days)
      // updateTrendData(response.data)
      
      // 暂时使用模拟数据
      const data: TrendData[] = []
      const now = new Date()
      for (let i = days - 1; i >= 0; i--) {
        const date = new Date(now)
        date.setDate(date.getDate() - i)
        data.push({
          date: date.toISOString().split('T')[0],
          commits: Math.floor(Math.random() * 15) + 5,
          additions: Math.floor(Math.random() * 500) + 100,
          deletions: Math.floor(Math.random() * 200) + 50
        })
      }
      updateTrendData(data)
    } catch (error) {
      console.error('Failed to fetch trend data:', error)
    }
  }

  /**
   * 从API获取成就里程碑数据（真实API）
   */
  async function fetchMilestones(userId: number = 1) {
    try {
      const apiMilestones = await dashboardApi.getMilestones(userId)
      milestones.value = apiMilestones.map(convertApiMilestone)
    } catch (err: any) {
      console.error('Failed to fetch milestones:', err)
      // 失败时使用模拟数据
      milestones.value = [
        {
          id: 'first-commit',
          title: '初次提交',
          description: '完成第一次代码提交',
          icon: '🎉',
          level: 'bronze',
          unlocked: true,
          unlockedAt: new Date('2024-01-01'),
          category: 'coding'
        },
        {
          id: 'streak-7',
          title: '七日连击',
          description: '连续编码7天',
          icon: '🔥',
          level: 'silver',
          unlocked: true,
          unlockedAt: new Date('2024-01-08'),
          category: 'streak'
        },
        {
          id: 'commits-100',
          title: '百次提交',
          description: '累计完成100次提交',
          icon: '💯',
          level: 'gold',
          unlocked: true,
          unlockedAt: new Date('2024-02-15'),
          category: 'coding'
        },
        {
          id: 'streak-30',
          title: '月度坚持',
          description: '连续编码30天',
          icon: '🏆',
          level: 'diamond',
          unlocked: false,
          progress: 42,
          target: 30,
          category: 'streak'
        },
        {
          id: 'polyglot',
          title: '语言大师',
          description: '掌握5种编程语言',
          icon: '🌟',
          level: 'legendary',
          unlocked: false,
          progress: 8,
          target: 5,
          category: 'language'
        },
        {
          id: 'night-owl',
          title: '夜猫子',
          description: '凌晨2点后提交代码50次',
          icon: '🦉',
          level: 'silver',
          unlocked: true,
          unlockedAt: new Date('2024-03-01'),
          category: 'special'
        }
      ]
    }
  }

  /**
   * 生成年度活跃度热力图数据
   */
  function generateHeatmapData(): HeatmapData[] {
    const data: HeatmapData[] = []
    const now = new Date()
    const oneYearAgo = new Date(now)
    oneYearAgo.setFullYear(now.getFullYear() - 1)
    
    // 生成过去365天的数据
    for (let d = new Date(oneYearAgo); d <= now; d.setDate(d.getDate() + 1)) {
      const dateStr = d.toISOString().split('T')[0]
      const commits = Math.floor(Math.random() * 20) // 0-19次提交
      
      // 计算颜色等级 (0-4)
      let level = 0
      if (commits === 0) level = 0
      else if (commits <= 3) level = 1
      else if (commits <= 6) level = 2
      else if (commits <= 10) level = 3
      else level = 4
      
      data.push({
        date: dateStr,
        commits,
        level
      })
    }
    
    return data
  }

  /**
   * 从API获取年度活跃度数据
   */
  async function fetchHeatmapData() {
    try {
      // TODO: 实际API调用
      // const response = await api.getHeatmapData()
      // heatmapData.value = response.data
      
      // 暂时使用模拟数据
      heatmapData.value = generateHeatmapData()
    } catch (error) {
      console.error('Failed to fetch heatmap data:', error)
    }
  }

  /**
   * 刷新所有数据（使用真实API）
   */
  async function refreshAllData(userId: number = 1) {
    // 使用总览API一次性获取所有数据
    await fetchDashboardData(userId)
  }

  /**
   * 重置所有数据
   */
  function reset() {
    dashboardStats.value = {
      todayCommits: 0,
      weekCommits: 0,
      monthCommits: 0,
      codeLines: 0,
      streakDays: 0,
      workHours: 0,
      activeLanguage: 'TypeScript',
      totalRepositories: 0
    }
    recentActivities.value = []
    languageStats.value = []
    trendData.value = []
    milestones.value = []
    heatmapData.value = []
    lastUpdated.value = null
  }

  return {
    // State
    dashboardStats,
    recentActivities,
    languageStats,
    trendData,
    milestones,
    heatmapData,
    isLoading,
    error,
    lastUpdated,
    
    // Computed
    todayTrend,
    weekTrend,
    totalCommits,
    
    // Actions
    updateDashboardStats,
    addActivity,
    setRecentActivities,
    updateLanguageStats,
    updateTrendData,
    fetchDashboardData,      // 新增：获取总览数据
    fetchDashboardStats,     // 更新：使用真实API
    fetchRecentActivities,
    fetchLanguageStats,
    fetchTrendData,
    fetchMilestones,        // 更新：使用真实API
    fetchHeatmapData,
    refreshAllData,         // 更新：使用真实API
    reset
  }
})