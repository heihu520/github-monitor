"""
个人仪表板数据聚合服务
实现仪表板统计数据的计算和聚合逻辑
"""
from typing import List
from datetime import datetime, timedelta
from app.models.dashboard import (
    DashboardStatsResponse,
    DashboardOverviewResponse,
    MilestoneAchievement,
    TrendPoint,
    HeatmapData
)


class DashboardService:
    """仪表板数据服务"""
    
    def __init__(self):
        """初始化服务"""
        # TODO: 注入数据库会话和缓存
        pass
    
    async def get_dashboard_stats(self, user_id: str) -> DashboardStatsResponse:
        """
        获取仪表板统计数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            DashboardStatsResponse: 统计数据
        """
        # TODO: 从数据库查询实际数据
        # 当前返回模拟数据
        
        return DashboardStatsResponse(
            today_commits=8,
            today_additions=234,
            today_deletions=89,
            week_commits=42,
            week_additions=1456,
            week_deletions=456,
            month_commits=156,
            month_additions=5678,
            month_deletions=1234,
            streak_days=42,
            active_language="TypeScript",
            work_hours=28.5,
            total_repositories=5,
            code_lines=1234
        )
    
    async def get_milestones(self, user_id: str) -> List[MilestoneAchievement]:
        """
        获取里程碑成就列表
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[MilestoneAchievement]: 成就列表
        """
        # TODO: 从数据库查询用户成就进度
        # 当前返回模拟数据
        
        milestones = [
            MilestoneAchievement(
                id="streak-7",
                name="连续编码7天",
                description="坚持每天编码，已连续7天！",
                icon="🔥",
                category="streak",
                threshold=7,
                current_value=42,
                progress=100.0,
                achieved=True,
                achieved_at=datetime(2026, 1, 5, 10, 0, 0)
            ),
            MilestoneAchievement(
                id="streak-30",
                name="连续编码30天",
                description="30天编码挑战进行中",
                icon="🔥",
                category="streak",
                threshold=30,
                current_value=42,
                progress=100.0,
                achieved=True,
                achieved_at=datetime(2026, 1, 8, 10, 0, 0)
            ),
            MilestoneAchievement(
                id="streak-100",
                name="连续编码100天",
                description="百日编码大师",
                icon="🏆",
                category="streak",
                threshold=100,
                current_value=42,
                progress=42.0,
                achieved=False
            ),
            MilestoneAchievement(
                id="commits-100",
                name="提交100次",
                description="已完成100次代码提交",
                icon="📊",
                category="commits",
                threshold=100,
                current_value=156,
                progress=100.0,
                achieved=True,
                achieved_at=datetime(2025, 12, 15, 14, 30, 0)
            ),
            MilestoneAchievement(
                id="commits-500",
                name="提交500次",
                description="代码提交达人",
                icon="🚀",
                category="commits",
                threshold=500,
                current_value=156,
                progress=31.2,
                achieved=False
            ),
            MilestoneAchievement(
                id="languages-3",
                name="精通3种语言",
                description="掌握3种编程语言",
                icon="💎",
                category="languages",
                threshold=3,
                current_value=4,
                progress=100.0,
                achieved=True,
                achieved_at=datetime(2025, 11, 20, 9, 0, 0)
            )
        ]
        
        return milestones
    
    async def get_trend_data(self, user_id: str, days: int = 7) -> List[TrendPoint]:
        """
        获取趋势数据
        
        Args:
            user_id: 用户ID
            days: 天数，默认7天
            
        Returns:
            List[TrendPoint]: 趋势数据点列表
        """
        # TODO: 从数据库查询实际趋势数据
        # 当前返回模拟数据
        
        trend_data = []
        today = datetime.now().date()
        
        for i in range(days - 1, -1, -1):
            date = today - timedelta(days=i)
            trend_data.append(
                TrendPoint(
                    date=date.isoformat(),
                    commits=5 + (i % 3) * 2,
                    additions=200 + i * 50,
                    deletions=50 + i * 10
                )
            )
        
        return trend_data
    
    async def get_heatmap_data(self, user_id: str, days: int = 90) -> List[HeatmapData]:
        """
        获取编码活跃度热力图数据
        
        Args:
            user_id: 用户ID
            days: 天数，默认90天
            
        Returns:
            List[HeatmapData]: 热力图数据列表
        """
        # TODO: 从数据库查询实际活跃度数据
        # 当前返回模拟数据
        
        heatmap_data = []
        today = datetime.now().date()
        
        for i in range(days - 1, -1, -1):
            date = today - timedelta(days=i)
            commits = (i % 7) + (i % 3)  # 模拟提交数
            
            # 根据提交数计算活跃度等级 0-4
            if commits == 0:
                level = 0
            elif commits <= 2:
                level = 1
            elif commits <= 4:
                level = 2
            elif commits <= 6:
                level = 3
            else:
                level = 4
            
            heatmap_data.append(
                HeatmapData(
                    date=date.isoformat(),
                    value=commits,
                    level=level
                )
            )
        
        return heatmap_data
    
    async def get_dashboard_overview(self, user_id: str) -> DashboardOverviewResponse:
        """
        获取仪表板完整总览数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            DashboardOverviewResponse: 完整仪表板数据
        """
        # 并行获取所有数据
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


# 单例服务实例
dashboard_service = DashboardService()