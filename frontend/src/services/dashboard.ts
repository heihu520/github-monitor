/**
 * 仪表板API服务
 * 封装所有仪表板相关的API调用
 */

import { get } from './api'
import type {
  DashboardOverview,
  DashboardStats,
  MilestoneAchievement,
  TrendPoint,
  HeatmapData,
  LanguageStat,
  HourlyActivity,
} from './types'

/**
 * 仪表板API服务类
 */
class DashboardService {
  /**
   * 获取仪表板总览数据
   * @param userId 用户ID
   * @returns 仪表板总览数据
   */
  async getOverview(userId: number): Promise<DashboardOverview> {
    return get<DashboardOverview>(`/api/v1/dashboard/overview`, { user_id: userId })
  }

  /**
   * 获取仪表板统计数据
   * @param userId 用户ID
   * @returns 统计数据
   */
  async getStats(userId: number): Promise<DashboardStats> {
    return get<DashboardStats>(`/api/v1/dashboard/stats`, { user_id: userId })
  }

  /**
   * 获取里程碑成就列表
   * @param userId 用户ID
   * @returns 成就列表
   */
  async getMilestones(userId: number): Promise<MilestoneAchievement[]> {
    return get<MilestoneAchievement[]>(`/api/v1/dashboard/milestones`, { user_id: userId })
  }

  /**
   * 获取趋势数据
   * @param userId 用户ID
   * @param days 天数 (默认30天)
   * @returns 趋势数据点列表
   */
  async getTrendData(userId: number, days: number = 30): Promise<TrendPoint[]> {
    return get<TrendPoint[]>(`/api/v1/dashboard/trend`, { 
      user_id: userId,
      days 
    })
  }

  /**
   * 获取热力图数据
   * @param userId 用户ID
   * @param startDate 开始日期 (YYYY-MM-DD)
   * @param endDate 结束日期 (YYYY-MM-DD)
   * @returns 热力图数据点列表
   */
  async getHeatmapData(
    userId: number, 
    startDate?: string, 
    endDate?: string
  ): Promise<HeatmapData[]> {
    const params: any = { user_id: userId }
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    
    return get<HeatmapData[]>(`/api/v1/dashboard/heatmap`, params)
  }

  /**
   * 获取编程语言统计
   * @param userId 用户ID
   * @returns 语言统计列表
   */
  async getLanguageStats(userId: number): Promise<LanguageStat[]> {
    return get<LanguageStat[]>(`/api/v1/analytics/languages`, { user_id: userId })
  }

  /**
   * 获取时段活动数据
   * @param userId 用户ID
   * @param days 天数 (默认7天)
   * @returns 时段活动数据
   */
  async getHourlyActivity(userId: number, days: number = 7): Promise<HourlyActivity[]> {
    return get<HourlyActivity[]>(`/api/v1/analytics/hourly`, { 
      user_id: userId,
      days 
    })
  }
}

/**
 * 导出单例实例
 */
export const dashboardApi = new DashboardService()

/**
 * 默认导出
 */
export default dashboardApi