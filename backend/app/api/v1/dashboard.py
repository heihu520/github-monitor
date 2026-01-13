"""
个人仪表板API路由
实现个人编码仪表板数据聚合API端点
"""
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dashboard import (
    DashboardStatsResponse,
    DashboardOverviewResponse,
    MilestoneAchievement,
    TrendPoint,
    HeatmapData
)
from app.services.dashboard_service import DashboardService
from app.core.database import get_db

router = APIRouter()


@router.get(
    "/overview",
    response_model=DashboardOverviewResponse,
    summary="获取仪表板总览",
    description="获取个人编码仪表板的完整数据，包括统计、成就、趋势和热力图"
)
async def get_dashboard_overview(
    user_id: int = Query(default=1, description="用户ID"),
    db: AsyncSession = Depends(get_db)
) -> DashboardOverviewResponse:
    """
    获取仪表板总览数据
    
    **返回数据包含:**
    - 今日/本周/本月提交统计
    - 代码行数统计
    - 连续编码天数
    - 最活跃编程语言
    - 工作时长估算
    - 里程碑成就列表
    - 最近7天提交趋势
    - 90天编码活跃度热力图
    
    **响应时间要求:** < 2秒
    """
    service = DashboardService(db)
    return await service.get_dashboard_overview(user_id)


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    summary="获取统计数据",
    description="仅获取仪表板统计数据，不包含成就和趋势"
)
async def get_dashboard_stats(
    user_id: int = Query(default=1, description="用户ID"),
    db: AsyncSession = Depends(get_db)
) -> DashboardStatsResponse:
    """
    获取仪表板统计数据
    
    **包含指标:**
    - 今日提交数、代码行数
    - 本周提交数、代码行数
    - 本月提交数、代码行数
    - 连续编码天数
    - 最活跃编程语言
    - 本周工作时长
    - 总仓库数
    """
    service = DashboardService(db)
    return await service.get_dashboard_stats(user_id)


@router.get(
    "/milestones",
    response_model=list[MilestoneAchievement],
    summary="获取里程碑成就",
    description="获取用户的里程碑成就列表和进度"
)
async def get_milestones(
    user_id: int = Query(default=1, description="用户ID"),
    db: AsyncSession = Depends(get_db)
) -> list[MilestoneAchievement]:
    """
    获取里程碑成就列表
    
    **支持的成就类型:**
    - 连续编码天数 (7天、30天、100天、365天)
    - 累计提交数 (100、500、1000、5000)
    - 单日最高代码量 (1000行、5000行、10000行)
    - 精通语言数 (3种、5种、10种)
    
    **返回字段:**
    - 成就名称、描述、图标
    - 当前进度和完成百分比
    - 是否已达成及达成时间
    """
    service = DashboardService(db)
    return await service.get_milestones(user_id)


@router.get(
    "/trend",
    response_model=list[TrendPoint],
    summary="获取提交趋势",
    description="获取指定天数的提交趋势数据"
)
async def get_trend_data(
    user_id: int = Query(default=1, description="用户ID"),
    days: int = Query(default=7, ge=1, le=365, description="天数 (1-365)"),
    db: AsyncSession = Depends(get_db)
) -> list[TrendPoint]:
    """
    获取提交趋势数据
    
    **参数:**
    - days: 查询天数，默认7天,最多365天
    
    **返回数据:**
    - 每日提交数
    - 每日新增代码行数
    - 每日删除代码行数
    
    **用于:** 趋势图表展示
    """
    service = DashboardService(db)
    return await service.get_trend_data(user_id, days)


@router.get(
    "/heatmap",
    response_model=list[HeatmapData],
    summary="获取活跃度热力图",
    description="获取编码活跃度热力图数据（类似GitHub贡献图）"
)
async def get_heatmap_data(
    user_id: int = Query(default=1, description="用户ID"),
    days: int = Query(default=90, ge=7, le=365, description="天数 (7-365)"),
    db: AsyncSession = Depends(get_db)
) -> list[HeatmapData]:
    """
    获取编码活跃度热力图数据
    
    **参数:**
    - days: 查询天数，默认90天，最多365天
    
    **返回数据:**
    - 每日提交数（value）
    - 活跃度等级 0-4（level）
      - 0: 无活动
      - 1: 低活跃 (1-2次提交)
      - 2: 中活跃 (3-5次提交)
      - 3: 高活跃 (6-10次提交)
      - 4: 极度活跃 (11+次提交)
    
    **用于:** 类似GitHub的贡献热力图展示
    """
    service = DashboardService(db)
    return await service.get_heatmap_data(user_id, days)