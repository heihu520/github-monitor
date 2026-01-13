/**
 * 数据同步API服务
 * 封装GitHub数据同步相关的API调用
 */

import apiClient from './api'
import type { SyncRequest, SyncResponse } from './types'

/**
 * 同步服务类
 */
class SyncService {
  /**
   * 同步GitHub数据
   * @param userId 用户ID
   * @param username GitHub用户名
   * @param githubToken GitHub访问令牌（可选）
   * @param syncMode 同步模式（可选）: full / incremental / auto（默认）
   * @returns 同步结果
   */
  async syncGithubData(
    userId: number,
    username: string,
    githubToken?: string,
    syncMode?: 'full' | 'incremental' | 'auto'
  ): Promise<SyncResponse> {
    const request: SyncRequest = {
      user_id: userId,
      username,
      ...(githubToken && { github_token: githubToken }),
      ...(syncMode && { sync_mode: syncMode })
    }
    // 同步操作可能耗时较长，设置120秒超时
    // 注意：响应拦截器已经返回了response.data，所以这里直接得到SyncResponse
    return (await apiClient.post('/api/v1/sync/github', request, {
      timeout: 120000 // 120秒
    })) as SyncResponse
  }
}

/**
 * 导出单例实例
 */
export const syncApi = new SyncService()

/**
 * 默认导出
 */
export default syncApi