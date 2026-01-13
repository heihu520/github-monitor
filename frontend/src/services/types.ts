/**
 * API类型定义
 * 定义所有后端API的请求和响应类型
 */

/**
 * 仪表板统计数据
 */
export interface DashboardStats {
  // 今日数据
  today_commits: number
  today_additions: number
  today_deletions: number
  
  // 本周数据
  week_commits: number
  week_additions: number
  week_deletions: number
  
  // 本月数据
  month_commits: number
  month_additions: number
  month_deletions: number
  
  // 其他统计
  streak_days: number          // 连续编码天数
  active_language: string       // 最活跃语言
  work_hours: number           // 工作时长（小时）
  total_repositories: number   // 总仓库数
  code_lines: number          // 总代码行数
  last_updated: string        // 最后更新时间
}

/**
 * 里程碑成就
 */
export interface MilestoneAchievement {
  id: string
  name: string
  description: string
  icon: string
  level: 'bronze' | 'silver' | 'gold' | 'diamond' | 'legendary'
  unlocked: boolean
  unlock_date?: string
  progress?: number  // 进度百分比 (0-100)
  target?: number    // 目标值
  current?: number   // 当前值
}

/**
 * 趋势数据点
 */
export interface TrendPoint {
  date: string      // 日期 (YYYY-MM-DD)
  commits: number   // 提交数
  additions: number // 代码增加行数
  deletions: number // 代码删除行数
}

/**
 * 热力图数据
 */
export interface HeatmapData {
  date: string      // 日期 (YYYY-MM-DD)
  count: number     // 活动次数
  level: number     // 活跃级别 (0-4)
}

/**
 * 语言统计
 */
export interface LanguageStat {
  language: string
  lines: number
  percentage: number
  color?: string
}

/**
 * 时段活动数据
 */
export interface HourlyActivity {
  hour: number      // 小时 (0-23)
  commits: number   // 该时段的提交数
  additions: number
  deletions: number
}

/**
 * 仪表板总览数据
 */
export interface DashboardOverview {
  stats: DashboardStats
  milestones: MilestoneAchievement[]
  trend_data: TrendPoint[]
  heatmap_data: HeatmapData[]
  language_stats: LanguageStat[]
  hourly_activity: HourlyActivity[]
}

/**
 * 调度器任务
 */
export interface SchedulerJob {
  id: string
  name: string
  trigger: string          // 触发器类型: cron, interval, date
  next_run_time: string | null
  status: 'running' | 'paused' | 'pending'
}

/**
 * 调度器状态
 */
export interface SchedulerStatus {
  running: boolean
  jobs_count: number
  jobs: SchedulerJob[]
}

/**
 * 创建调度任务请求
 */
export interface CreateJobRequest {
  job_id: string
  name: string
  func: string             // 函数路径
  trigger: 'cron' | 'interval' | 'date'
  trigger_args: Record<string, any>  // 触发器参数
}

/**
 * API错误响应
 */
export interface ApiError {
  detail: string
  status_code?: number
}

/**
 * 同步任务状态
 */
export interface SyncTask {
  task_id: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress: number         // 0-100
  current_step: string
  total_steps: number
  message?: string
  error?: string
  started_at: string
  completed_at?: string
}

/**
 * 同步历史记录
 */
export interface SyncHistory {
  id: number
  user_id: number
  username: string
  started_at: string
  completed_at: string
  status: 'success' | 'failed'
  repos_synced: number
  commits_synced: number
  error_message?: string
}

/**
 * 用户信息
 */
export interface User {
  id: number
  username: string
  github_id: number
  avatar_url: string
  email?: string
  created_at: string
  updated_at: string
}

/**
 * 仓库信息
 */
export interface Repository {
  id: number
  name: string
  full_name: string
  description?: string
  language?: string
  stars: number
  forks: number
  is_fork: boolean
  created_at: string
  updated_at: string
}

/**
 * 提交信息
 */
export interface Commit {
  id: number
  sha: string
  message: string
  author_name: string
  author_email: string
  committed_at: string
  additions: number
  deletions: number
  changed_files: number
}

/**
 * 分页响应
 */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

/**
 * 健康检查响应
 */
export interface HealthCheckResponse {
  status: string
  database: string
  scheduler?: string
}