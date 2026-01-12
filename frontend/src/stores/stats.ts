import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 统计数据类型定义
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

  // 加载状态
  const isLoading = ref<boolean>(false)
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
   * 从API获取统计数据
   */
  async function fetchDashboardStats() {
    isLoading.value = true
    try {
      // TODO: 实际API调用
      // const response = await api.getDashboardStats()
      // updateDashboardStats(response.data)
      
      // 暂时使用模拟数据
      updateDashboardStats({
        todayCommits: 8,
        weekCommits: 42,
        monthCommits: 156,
        codeLines: 1234,
        streakDays: 42,
        workHours: 4.5,
        activeLanguage: 'TypeScript',
        totalRepositories: 5
      })
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error)
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
      
      // 暂时使用模拟数据
      updateLanguageStats([
        { name: 'TypeScript', percentage: 45, commits: 120, lines: 5400, color: '#3178c6' },
        { name: 'Python', percentage: 30, commits: 80, lines: 3600, color: '#3776ab' },
        { name: 'JavaScript', percentage: 15, commits: 40, lines: 1800, color: '#f7df1e' },
        { name: 'Vue', percentage: 10, commits: 25, lines: 1200, color: '#42b883' }
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
   * 刷新所有数据
   */
  async function refreshAllData() {
    await Promise.all([
      fetchDashboardStats(),
      fetchRecentActivities(),
      fetchLanguageStats(),
      fetchTrendData()
    ])
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
    lastUpdated.value = null
  }

  return {
    // State
    dashboardStats,
    recentActivities,
    languageStats,
    trendData,
    isLoading,
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
    fetchDashboardStats,
    fetchRecentActivities,
    fetchLanguageStats,
    fetchTrendData,
    refreshAllData,
    reset
  }
})