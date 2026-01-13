"""
数据同步API路由
实现GitHub数据同步功能
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
import logging

from app.core.database import get_db
from app.core.config import settings
from app.services.data_sync_service import DataSyncService
from app.services.github_client import GitHubClient

logger = logging.getLogger(__name__)

router = APIRouter()


class SyncRequest(BaseModel):
    """同步请求模型"""
    user_id: int = Field(..., description="用户ID", ge=1)
    username: str = Field(..., description="GitHub用户名", min_length=1)


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
        
        # 创建GitHub客户端
        github_client = GitHubClient(settings.GITHUB_TOKEN)
        
        # 创建数据同步服务
        sync_service = DataSyncService(db, github_client)
        
        # 执行完整数据同步
        sync_result = await sync_service.sync_user_data(
            username=request.username,
            max_commits_per_repo=100  # 每个仓库最多同步100个提交
        )
        
        logger.info(f"GitHub数据同步完成: {sync_result}")
        
        return SyncResponse(
            success=True,
            message="数据同步成功",
            username=sync_result['username'],
            user_id=sync_result['user_id'],
            repos_synced=sync_result['total_repos_synced'],
            commits_synced=sync_result['total_commits_synced'],
            total_additions=sync_result.get('total_additions', 0),
            total_deletions=sync_result.get('total_deletions', 0)
        )
        
    except Exception as e:
        logger.error(f"同步GitHub数据失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"同步失败: {str(e)}"
        )