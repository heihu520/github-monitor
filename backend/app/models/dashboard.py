"""
个人仪表板数据模型
定义仪表板相关的Pydantic模型
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DashboardStatsResponse(BaseModel):
    """仪表板统计数据响应模型"""
    
    # 今日统计
    today_commits: int = Field(description="今日提交数")
    today_additions: int = Field(description="今日新增代码行数")
    today_deletions: int = Field(description="今日删除代码行数")
    
    # 本周统计
    week_commits: int = Field(description="本周提交数")
    week_additions: int = Field(description="本周新增代码行数")
    week_deletions: int = Field(description="本周删除代码行数")
    
    # 本月统计
    month_commits: int = Field(description="本月提交数")
    month_additions: int = Field(description="本月新增代码行数")
    month_deletions: int = Field(description="本月删除代码行数")
    
    # 其他关键指标
    streak_days: int = Field(description="连续编码天数")
    active_language: str = Field(description="最活跃的编程语言")
    work_hours: float = Field(description="本周工作时长（小时）")
    total_repositories: int = Field(description="总仓库数")
    
    # 代码总量
    code_lines: int = Field(description="总代码行数（今日+本周+本月）")
    
    # 时间戳
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class MilestoneAchievement(BaseModel):
    """里程碑成就模型"""
    
    id: str = Field(description="成就ID")
    name: str = Field(description="成就名称")
    description: str = Field(description="成就描述")
    icon: str = Field(description="成就图标emoji")
    category: str = Field(description="成就类别: streak|commits|code|languages")
    threshold: int = Field(description="达成阈值")
    current_value: int = Field(description="当前值")
    progress: float = Field(description="完成进度百分比 0-100")
    achieved: bool = Field(description="是否已达成")
    achieved_at: Optional[datetime] = Field(None, description="达成时间")


class TrendPoint(BaseModel):
    """趋势数据点"""
    
    date: str = Field(description="日期 YYYY-MM-DD")
    commits: int = Field(description="提交数")
    additions: int = Field(description="新增行数")
    deletions: int = Field(description="删除行数")


class HeatmapData(BaseModel):
    """热力图数据"""
    
    date: str = Field(description="日期")
    value: int = Field(description="活跃度值（提交数）")
    level: int = Field(description="活跃度等级 0-4")


class DashboardOverviewResponse(BaseModel):
    """仪表板总览响应 - 完整数据"""
    
    stats: DashboardStatsResponse = Field(description="统计数据")
    milestones: List[MilestoneAchievement] = Field(description="里程碑成就列表")
    trend_data: List[TrendPoint] = Field(description="最近7天趋势数据")
    heatmap_data: List[HeatmapData] = Field(description="编码活跃度热力图数据")
    
    class Config:
        json_schema_extra = {
            "example": {
                "stats": {
                    "today_commits": 8,
                    "today_additions": 234,
                    "today_deletions": 89,
                    "week_commits": 42,
                    "week_additions": 1456,
                    "week_deletions": 456,
                    "month_commits": 156,
                    "month_additions": 5678,
                    "month_deletions": 1234,
                    "streak_days": 42,
                    "active_language": "TypeScript",
                    "work_hours": 28.5,
                    "total_repositories": 5,
                    "code_lines": 1234,
                    "last_updated": "2026-01-12T16:00:00Z"
                },
                "milestones": [
                    {
                        "id": "streak-7",
                        "name": "连续编码7天",
                        "description": "坚持每天编码，已连续7天！",
                        "icon": "🔥",
                        "category": "streak",
                        "threshold": 7,
                        "current_value": 42,
                        "progress": 100.0,
                        "achieved": True,
                        "achieved_at": "2026-01-05T10:00:00Z"
                    }
                ],
                "trend_data": [
                    {
                        "date": "2026-01-06",
                        "commits": 5,
                        "additions": 234,
                        "deletions": 89
                    }
                ],
                "heatmap_data": [
                    {
                        "date": "2026-01-06",
                        "value": 5,
                        "level": 2
                    }
                ]
            }
        }