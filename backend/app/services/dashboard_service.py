"""
个人仪表板数据聚合服务
实现仪表板统计数据的计算和聚合逻辑
"""
from typing import List
from datetime import datetime, timedelta, date
from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dashboard import (
    DashboardStatsResponse,
    DashboardOverviewResponse,
    MilestoneAchievement,
    TrendPoint,
    HeatmapData
)
from app.models.user import User
from app.models.repository import Repository
from app.models.commit_detail import CommitDetail
from app.models.daily_stat import DailyStat


class DashboardService:
    """仪表板数据服务"""
    
    def __init__(self, db: AsyncSession):
        """
        初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    async def get_dashboard_stats(self, user_id: int) -> DashboardStatsResponse:
        """
        获取仪表板统计数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            DashboardStatsResponse: 统计数据
        """
        # 获取用户基本信息
        user_result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            # 返回空数据
            return DashboardStatsResponse(
                today_commits=0,
                today_additions=0,
                today_deletions=0,
                week_commits=0,
                week_additions=0,
                week_deletions=0,
                month_commits=0,
                month_additions=0,
                month_deletions=0,
                streak_days=0,
                active_language="",
                work_hours=0.0,
                total_repositories=0,
                code_lines=0
            )
        
        # 计算时间范围
        today = date.today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # 今日统计
        today_stats_result = await self.db.execute(
            select(
                func.count(CommitDetail.id).label('commits'),
                func.coalesce(func.sum(CommitDetail.additions), 0).label('additions'),
                func.coalesce(func.sum(CommitDetail.deletions), 0).label('deletions')
            ).where(
                and_(
                    CommitDetail.user_id == user_id,
                    func.date(CommitDetail.commit_date) == today
                )
            )
        )
        today_stats = today_stats_result.first()
        
        # 本周统计
        week_stats_result = await self.db.execute(
            select(
                func.count(CommitDetail.id).label('commits'),
                func.coalesce(func.sum(CommitDetail.additions), 0).label('additions'),
                func.coalesce(func.sum(CommitDetail.deletions), 0).label('deletions')
            ).where(
                and_(
                    CommitDetail.user_id == user_id,
                    func.date(CommitDetail.commit_date) >= week_ago
                )
            )
        )
        week_stats = week_stats_result.first()
        
        # 本月统计
        month_stats_result = await self.db.execute(
            select(
                func.count(CommitDetail.id).label('commits'),
                func.coalesce(func.sum(CommitDetail.additions), 0).label('additions'),
                func.coalesce(func.sum(CommitDetail.deletions), 0).label('deletions')
            ).where(
                and_(
                    CommitDetail.user_id == user_id,
                    func.date(CommitDetail.commit_date) >= month_ago
                )
            )
        )
        month_stats = month_stats_result.first()
        
        # 本周工作时长（从daily_stats表）
        work_hours_result = await self.db.execute(
            select(func.coalesce(func.sum(DailyStat.work_hours), 0)).where(
                and_(
                    DailyStat.user_id == user_id,
                    DailyStat.stat_date >= week_ago
                )
            )
        )
        work_hours = work_hours_result.scalar() or 0.0
        
        # 总代码行数
        total_lines = (user.total_additions or 0) - (user.total_deletions or 0)
        
        return DashboardStatsResponse(
            today_commits=today_stats.commits if today_stats else 0,
            today_additions=today_stats.additions if today_stats else 0,
            today_deletions=today_stats.deletions if today_stats else 0,
            week_commits=week_stats.commits if week_stats else 0,
            week_additions=week_stats.additions if week_stats else 0,
            week_deletions=week_stats.deletions if week_stats else 0,
            month_commits=month_stats.commits if month_stats else 0,
            month_additions=month_stats.additions if month_stats else 0,
            month_deletions=month_stats.deletions if month_stats else 0,
            streak_days=user.streak_days or 0,
            active_language=user.active_language or "",
            work_hours=float(work_hours),
            total_repositories=user.total_repos or 0,
            code_lines=total_lines
        )
    
    async def get_milestones(self, user_id: int) -> List[MilestoneAchievement]:
        """
        获取里程碑成就列表
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[MilestoneAchievement]: 成就列表
        """
        # 获取用户信息
        user_result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            return []
        
        # 获取语言统计数量
        lang_count_result = await self.db.execute(
            select(func.count(func.distinct(CommitDetail.primary_language))).where(
                and_(
                    CommitDetail.user_id == user_id,
                    CommitDetail.primary_language.isnot(None),
                    CommitDetail.primary_language != ''
                )
            )
        )
        lang_count = lang_count_result.scalar() or 0
        
        # 定义里程碑配置
        milestones = []
        
        # 连续编码里程碑
        streak_milestones = [
            (7, "连续编码7天", "坚持每天编码，已连续7天！", "🔥"),
            (30, "连续编码30天", "30天编码挑战进行中", "🔥"),
            (100, "连续编码100天", "百日编码大师", "🏆"),
        ]
        
        current_streak = user.streak_days or 0
        for threshold, name, desc, icon in streak_milestones:
            progress = min(100.0, (current_streak / threshold) * 100)
            achieved = current_streak >= threshold
            milestones.append(
                MilestoneAchievement(
                    id=f"streak-{threshold}",
                    name=name,
                    description=desc,
                    icon=icon,
                    category="streak",
                    threshold=threshold,
                    current_value=current_streak,
                    progress=progress,
                    achieved=achieved,
                    achieved_at=None  # 需要从milestone表查询
                )
            )
        
        # 提交次数里程碑
        commit_milestones = [
            (100, "提交100次", "已完成100次代码提交", "📊"),
            (500, "提交500次", "代码提交达人", "🚀"),
            (1000, "提交1000次", "提交大师", "🏅"),
        ]
        
        total_commits = user.total_commits or 0
        for threshold, name, desc, icon in commit_milestones:
            progress = min(100.0, (total_commits / threshold) * 100)
            achieved = total_commits >= threshold
            milestones.append(
                MilestoneAchievement(
                    id=f"commits-{threshold}",
                    name=name,
                    description=desc,
                    icon=icon,
                    category="commits",
                    threshold=threshold,
                    current_value=total_commits,
                    progress=progress,
                    achieved=achieved,
                    achieved_at=None
                )
            )
        
        # 编程语言里程碑
        lang_milestones = [
            (3, "精通3种语言", "掌握3种编程语言", "💎"),
            (5, "精通5种语言", "多语言开发者", "🌟"),
        ]
        
        for threshold, name, desc, icon in lang_milestones:
            progress = min(100.0, (lang_count / threshold) * 100)
            achieved = lang_count >= threshold
            milestones.append(
                MilestoneAchievement(
                    id=f"languages-{threshold}",
                    name=name,
                    description=desc,
                    icon=icon,
                    category="languages",
                    threshold=threshold,
                    current_value=lang_count,
                    progress=progress,
                    achieved=achieved,
                    achieved_at=None
                )
            )
        
        return milestones
    
    async def get_trend_data(self, user_id: int, days: int = 7) -> List[TrendPoint]:
        """
        获取趋势数据
        
        Args:
            user_id: 用户ID
            days: 天数，默认7天
            
        Returns:
            List[TrendPoint]: 趋势数据点列表
        """
        # 计算日期范围
        today = date.today()
        start_date = today - timedelta(days=days - 1)
        
        # 查询每日统计数据
        result = await self.db.execute(
            select(DailyStat).where(
                and_(
                    DailyStat.user_id == user_id,
                    DailyStat.stat_date >= start_date,
                    DailyStat.stat_date <= today
                )
            ).order_by(DailyStat.stat_date)
        )
        daily_stats = result.scalars().all()
        
        # 创建日期到统计数据的映射
        stats_map = {stat.stat_date: stat for stat in daily_stats}
        
        # 生成完整的趋势数据（填充缺失的日期）
        trend_data = []
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            stat = stats_map.get(current_date)
            
            trend_data.append(
                TrendPoint(
                    date=current_date.isoformat(),
                    commits=stat.commits if stat else 0,
                    additions=stat.additions if stat else 0,
                    deletions=stat.deletions if stat else 0
                )
            )
        
        return trend_data
    
    async def get_heatmap_data(self, user_id: int, days: int = 90) -> List[HeatmapData]:
        """
        获取编码活跃度热力图数据
        
        Args:
            user_id: 用户ID
            days: 天数，默认90天
            
        Returns:
            List[HeatmapData]: 热力图数据列表
        """
        # 计算日期范围
        today = date.today()
        start_date = today - timedelta(days=days - 1)
        
        # 查询每日统计数据
        result = await self.db.execute(
            select(DailyStat).where(
                and_(
                    DailyStat.user_id == user_id,
                    DailyStat.stat_date >= start_date,
                    DailyStat.stat_date <= today
                )
            ).order_by(DailyStat.stat_date)
        )
        daily_stats = result.scalars().all()
        
        # 创建日期到统计数据的映射
        stats_map = {stat.stat_date: stat for stat in daily_stats}
        
        # 生成完整的热力图数据
        heatmap_data = []
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            stat = stats_map.get(current_date)
            commits = stat.commits if stat else 0
            
            # 根据提交数计算活跃度等级 0-4
            if commits == 0:
                level = 0
            elif commits <= 2:
                level = 1
            elif commits <= 5:
                level = 2
            elif commits <= 10:
                level = 3
            else:
                level = 4
            
            heatmap_data.append(
                HeatmapData(
                    date=current_date.isoformat(),
                    value=commits,
                    level=level
                )
            )
        
        return heatmap_data
    
    async def get_dashboard_overview(self, user_id: int) -> DashboardOverviewResponse:
        """
        获取仪表板完整总览数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            DashboardOverviewResponse: 完整仪表板数据
        """
        # 获取所有数据
        stats = await self.get_dashboard_stats(user_id)
        milestones = await self.get_milestones(user_id)
        trend_data = await self.get_trend_data(user_id, days=7)
        heatmap_data = await self.get_heatmap_data(user_id, days=90)
        
        return DashboardOverviewResponse(
            stats=stats,
            milestones=milestones,
            trend_data=trend_data,
            heatmap_data=heatmap_data
        )