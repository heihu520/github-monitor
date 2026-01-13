"""
数据同步API路由
实现GitHub数据同步功能
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
import logging
import sys
import os

# 添加scripts目录到路径以导入统计脚本
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts'))

from app.core.database import get_db
from app.core.config import settings
from app.services.data_sync_service import DataSyncService
from app.services.github_client import GitHubClient

# 导入统计更新函数
try:
    from scripts.update_user_stats import update_user_statistics
    from scripts.update_daily_stats import update_daily_stats
except ImportError:
    # 如果导入失败，定义空函数
    async def update_user_statistics(user_id: int):
        logger.warning("update_user_statistics not available")
    
    async def update_daily_stats(user_id: int):
        logger.warning("update_daily_stats not available")

logger = logging.getLogger(__name__)

router = APIRouter()


class SyncRequest(BaseModel):
    """同步请求模型"""
    user_id: int = Field(..., description="用户ID", ge=1)
    username: str = Field(..., description="GitHub用户名", min_length=1)
    github_token: str | None = Field(None, description="GitHub个人访问令牌（可选）")
    sync_mode: str | None = Field(None, description="同步模式: full(全量) / incremental(增量) / auto(自动，默认)")


class SyncResponse(BaseModel):
    """同步响应模型"""
    success: bool = Field(..., description="同步是否成功")
    message: str = Field(..., description="响应消息")
    username: str = Field(..., description="GitHub用户名")
    user_id: int = Field(..., description="用户ID")
    repos_synced: int = Field(..., description="同步的仓库数量")
    commits_synced: int = Field(..., description="同步的提交数量")
    total_additions: int = Field(default=0, description="总新增代码行数")
    total_deletions: int = Field(default=0, description="总删除代码行数")
    sync_mode: str = Field(..., description="实际执行的同步模式: full / incremental")
    since: str | None = Field(None, description="增量同步起始时间")


@router.post(
    "/github",
    response_model=SyncResponse,
    summary="一键同步GitHub数据",
    description="触发完整的GitHub数据同步流程，包括用户信息、仓库列表和提交历史"
)
async def sync_github_data(
    request: SyncRequest,
    db: AsyncSession = Depends(get_db)
) -> SyncResponse:
    """
    一键同步GitHub数据
    
    **功能:**
    - 同步用户基本信息
    - 同步所有仓库列表
    - 同步最近的提交记录
    - 自动更新用户统计数据
    
    **参数:**
    - user_id: 用户ID
    - username: GitHub用户名
    
    **返回:**
    - 同步结果统计信息
    
    **注意:**
    - 同步过程可能需要较长时间（取决于仓库数量）
    - 受GitHub API速率限制约束
    """
    try:
        logger.info(f"开始同步GitHub数据: user_id={request.user_id}, username={request.username}")
        
        # 使用请求中的token或配置文件中的默认token
        token = request.github_token or settings.GITHUB_TOKEN
        if request.github_token:
            logger.info("使用用户提供的GitHub Token")
        else:
            logger.info("使用系统配置的GitHub Token")
        
        # 创建GitHub客户端
        github_client = GitHubClient(token)
        
        # 创建数据同步服务
        sync_service = DataSyncService(db, github_client)
        
        # 确定同步模式
        sync_mode = request.sync_mode or "auto"
        
        if sync_mode == "full":
            incremental = False
            logger.info("用户指定全量同步模式")
        elif sync_mode == "incremental":
            incremental = True
            logger.info("用户指定增量同步模式")
        else:  # auto
            incremental = True  # 默认自动增量
            logger.info("自动同步模式（默认增量）")
        
        # 执行数据同步
        sync_result = await sync_service.sync_user_data(
            username=request.username,
            max_commits_per_repo=100,  # 每个仓库最多同步100个提交
            incremental=incremental
        )
        
        logger.info(f"GitHub数据同步完成: {sync_result}")
        
        # 同步完成后自动更新统计数据
        # 单用户应用：始终使用请求中的user_id（固定为1）进行统计更新
        # 而不是sync_result中的user_id（可能是数据库自动分配的2等其他值）
        user_id = request.user_id
        
        try:
            logger.info(f"开始更新用户 {user_id} 的统计数据...")
            
            # 更新用户统计
            await update_user_statistics(user_id)
            logger.info(f"用户统计数据更新完成")
            
            # 更新每日统计
            await update_daily_stats(user_id)
            logger.info(f"每日统计数据更新完成")
            
        except Exception as stats_error:
            # 统计更新失败不影响同步结果
            logger.error(f"统计数据更新失败: {stats_error}", exc_info=True)
        
        return SyncResponse(
            success=True,
            message="数据同步成功",
            username=sync_result['username'],
            user_id=sync_result['user_id'],
            repos_synced=sync_result['total_repos_synced'],
            commits_synced=sync_result['total_commits_synced'],
            total_additions=sync_result.get('total_additions', 0),
            total_deletions=sync_result.get('total_deletions', 0),
            sync_mode=sync_result.get('sync_mode', 'unknown'),
            since=sync_result.get('since')
        )
        
    except Exception as e:
        logger.error(f"同步GitHub数据失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"同步失败: {str(e)}"
        )