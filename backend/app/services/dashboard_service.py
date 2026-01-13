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
    HeatmapData,
    LanguageStatResponse,
    HourlyActivityResponse,
    RecentActivityResponse
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
        
        # 计算时间范围（使用UTC时间，因为commit_date存储的是UTC）
        now_utc = datetime.utcnow()
        today = now_utc.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # 今日统计（使用DailyStat表，避免时区问题）
        today_stats_result = await self.db.execute(
            select(
                DailyStat.commits,
                DailyStat.additions,
                DailyStat.deletions
            ).where(
                and_(
                    DailyStat.user_id == user_id,
                    DailyStat.stat_date == today
                )
            )
        )
        today_stats = today_stats_result.first()
        
        # 本周统计（使用DailyStat表）
        week_stats_result = await self.db.execute(
            select(
                func.coalesce(func.sum(DailyStat.commits), 0).label('commits'),
                func.coalesce(func.sum(DailyStat.additions), 0).label('additions'),
                func.coalesce(func.sum(DailyStat.deletions), 0).label('deletions')
            ).where(
                and_(
                    DailyStat.user_id == user_id,
                    DailyStat.stat_date >= week_ago
                )
            )
        )
        week_stats = week_stats_result.first()
        
        # 本月统计（使用DailyStat表）
        month_stats_result = await self.db.execute(
            select(
                func.coalesce(func.sum(DailyStat.commits), 0).label('commits'),
                func.coalesce(func.sum(DailyStat.additions), 0).label('additions'),
                func.coalesce(func.sum(DailyStat.deletions), 0).label('deletions')
            ).where(
                and_(
                    DailyStat.user_id == user_id,
                    DailyStat.stat_date >= month_ago
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
    
    async def get_heatmap_data(self, user_id: int, days: int = 365) -> List[HeatmapData]:
        """
        获取编码活跃度热力图数据（年度视图 - 完整365天）
        
        Args:
            user_id: 用户ID
            days: 天数，默认365天（一整年）
            
        Returns:
            List[HeatmapData]: 热力图数据列表
        """
        # 计算完整一年的日期范围
        today = date.today()
        start_date = today - timedelta(days=days - 1)
        
        # 调整到周边界以填满日历视图
        # 将start_date调整到所在周的周一（weekday=0）
        start_weekday = start_date.weekday()
        start_date = start_date - timedelta(days=start_weekday)
        
        # 将today调整到所在周的周日（weekday=6）
        end_weekday = today.weekday()
        end_date = today
        if end_weekday < 6:  # 如果不是周日
            end_date = today + timedelta(days=6 - end_weekday)
        
        # 查询用户在此日期范围内的统计数据
        result = await self.db.execute(
            select(DailyStat).where(
                and_(
                    DailyStat.user_id == user_id,
                    DailyStat.stat_date >= start_date,
                    DailyStat.stat_date <= end_date
                )
            ).order_by(DailyStat.stat_date)
        )
        daily_stats = result.scalars().all()
        
        # 创建日期到统计数据的映射
        stats_map = {stat.stat_date: stat for stat in daily_stats}
        
        # 生成完整的热力图数据（填充所有日期）
        heatmap_data = []
        current = start_date
        while current <= end_date:
            stat = stats_map.get(current)
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
                    date=current.isoformat(),
                    value=commits,
                    level=level
                )
            )
            
            current += timedelta(days=1)
        
        return heatmap_data
    
    async def get_language_stats(self, user_id: int) -> list[LanguageStatResponse]:
        """获取语言统计"""
        result = await self.db.execute(
            select(
                CommitDetail.primary_language,
                func.sum(CommitDetail.additions + CommitDetail.deletions).label('lines')
            ).where(
                and_(
                    CommitDetail.user_id == user_id,
                    CommitDetail.primary_language.isnot(None),
                    CommitDetail.primary_language != ''
                )
            ).group_by(CommitDetail.primary_language)
        )
        
        lang_data = result.all()
        total_lines = sum(row.lines for row in lang_data)
        
        if total_lines == 0:
            return []
        
        # 语言颜色映射（多样化配色）
        color_map = {
            'Python': '#3776ab',
            'JavaScript': '#f7df1e',
            'TypeScript': '#3178c6',
            'Vue': '#42b883',
            'Java': '#ea2d2e',
            'Go': '#00add8',
            'Rust': '#ce422b',
            'C++': '#00599c',
            'C': '#a8b9cc',
            'HTML': '#e34c26',
            'CSS': '#1572b6',
            'YAML': '#cb171e',
            'Markdown': '#083fa1',
            'JSON': '#292929',
            'React': '#61dafb',
            'SQL': '#e38c00',
            'Shell': '#89e051',
            'Ruby': '#cc342d',
            'PHP': '#777bb4',
            'Swift': '#fa7343',
            'Kotlin': '#7f52ff',
            'Dart': '#00b4ab'
        }
        
        return [
            LanguageStatResponse(
                language=row.primary_language,
                lines=row.lines,
                percentage=round((row.lines / total_lines) * 100, 2),
                color=color_map.get(row.primary_language, '#94a3b8')
            )
            for row in lang_data
        ]
    
    async def get_hourly_activity(self, user_id: int) -> list[HourlyActivityResponse]:
        """获取时段活动统计"""
        result = await self.db.execute(
            select(
                func.extract('hour', CommitDetail.commit_date).label('hour'),
                func.count(CommitDetail.id).label('commits'),
                func.sum(CommitDetail.additions).label('additions'),
                func.sum(CommitDetail.deletions).label('deletions')
            ).where(
                CommitDetail.user_id == user_id
            ).group_by(func.extract('hour', CommitDetail.commit_date))
        )
        
        hourly_data = {int(row.hour): row for row in result.all()}
        
        return [
            HourlyActivityResponse(
                hour=h,
                commits=hourly_data[h].commits if h in hourly_data else 0,
                additions=hourly_data[h].additions if h in hourly_data else 0,
                deletions=hourly_data[h].deletions if h in hourly_data else 0
            )
            for h in range(24)
        ]
    
    async def get_recent_activities(self, user_id: int, limit: int = 10) -> list:
        """获取最近活动"""
        result = await self.db.execute(
            select(CommitDetail)
            .where(CommitDetail.user_id == user_id)
            .order_by(desc(CommitDetail.commit_date))
            .limit(limit)
        )
        
        commits = result.scalars().all()
        
        activities = []
        for commit in commits:
            # 解析提交类型
            message = commit.commit_message.lower()
            if message.startswith('feat'):
                commit_type = 'feat'
                icon = '✨'
                type_label = '功能'
            elif message.startswith('fix'):
                commit_type = 'fix'
                icon = '🐛'
                type_label = '修复'
            elif message.startswith('docs'):
                commit_type = 'docs'
                icon = '📝'
                type_label = '文档'
            elif message.startswith('style'):
                commit_type = 'style'
                icon = '💄'
                type_label = '样式'
            elif message.startswith('refactor'):
                commit_type = 'refactor'
                icon = '♻️'
                type_label = '重构'
            elif message.startswith('perf'):
                commit_type = 'perf'
                icon = '⚡'
                type_label = '性能'
            else:
                commit_type = 'other'
                icon = '📦'
                type_label = '其他'
            
            # 计算相对时间（使用UTC时间，数据库存储的是UTC）
            now = datetime.utcnow()
            commit_time = commit.commit_date.replace(tzinfo=None) if commit.commit_date.tzinfo else commit.commit_date
            delta = now - commit_time
            
            if delta.days > 0:
                time_str = f"{delta.days}天前"
            elif delta.seconds >= 3600:
                time_str = f"{delta.seconds // 3600}小时前"
            elif delta.seconds >= 60:
                time_str = f"{delta.seconds // 60}分钟前"
            else:
                time_str = "刚刚"
            
            activities.append({
                'id': commit.id,
                'icon': icon,
                'title': commit.commit_message.split('\n')[0][:100],  # 只取第一行，最多100字符
                'time': time_str,
                'type': commit_type,
                'typeLabel': type_label,
                'timestamp': int(commit.commit_date.timestamp())
            })
        
        return activities
    
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
        heatmap_data = await self.get_heatmap_data(user_id, days=365)
        language_stats = await self.get_language_stats(user_id)
        hourly_activity = await self.get_hourly_activity(user_id)
        recent_activities_data = await self.get_recent_activities(user_id, limit=10)
        
        # 转换为响应模型
        recent_activities = [
            RecentActivityResponse(**activity)
            for activity in recent_activities_data
        ]
        
        return DashboardOverviewResponse(
            stats=stats,
            milestones=milestones,
            trend_data=trend_data,
            heatmap_data=heatmap_data,
            language_stats=language_stats,
            hourly_activity=hourly_activity,
            recent_activities=recent_activities
        )