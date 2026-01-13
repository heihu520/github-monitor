"""
后台定时任务调度服务
使用APScheduler实现定期数据同步
"""
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.services.github_client import GitHubClient
from app.services.data_sync_service import DataSyncService

logger = logging.getLogger(__name__)


class SchedulerService:
    """定时任务调度服务"""
    
    def __init__(self):
        """初始化调度器"""
        self.scheduler = AsyncIOScheduler()
        self.github_client = None
        
    async def sync_user_data_job(self, username: str):
        """
        数据同步任务
        
        Args:
            username: GitHub用户名
        """
        logger.info(f"开始定时同步任务: {username}")
        
        try:
            # 创建GitHub客户端
            if not self.github_client:
                self.github_client = GitHubClient(settings.GITHUB_TOKEN)
            
            async with AsyncSessionLocal() as db:
                sync_service = DataSyncService(db, self.github_client)
                
                # 执行增量同步（最近30天数据）
                result = await sync_service.sync_user_data(
                    username=username,
                    max_commits_per_repo=100
                )
                
                logger.info(f"定时同步完成: {result}")
                
        except Exception as e:
            logger.error(f"定时同步失败: {e}", exc_info=True)
    
    def add_daily_sync_job(self, username: str, hour: int = 2, minute: int = 0):
        """
        添加每日同步任务
        
        Args:
            username: GitHub用户名
            hour: 执行时间（小时，0-23）
            minute: 执行时间（分钟，0-59）
        """
        self.scheduler.add_job(
            self.sync_user_data_job,
            trigger=CronTrigger(hour=hour, minute=minute),
            args=[username],
            id=f"daily_sync_{username}",
            name=f"每日同步 - {username}",
            replace_existing=True
        )
        logger.info(f"已添加每日同步任务: {username} (每天 {hour:02d}:{minute:02d})")
    
    def add_hourly_sync_job(self, username: str):
        """
        添加每小时同步任务
        
        Args:
            username: GitHub用户名
        """
        self.scheduler.add_job(
            self.sync_user_data_job,
            trigger=IntervalTrigger(hours=1),
            args=[username],
            id=f"hourly_sync_{username}",
            name=f"每小时同步 - {username}",
            replace_existing=True
        )
        logger.info(f"已添加每小时同步任务: {username}")
    
    def remove_job(self, job_id: str):
        """
        移除定时任务
        
        Args:
            job_id: 任务ID
        """
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"已移除任务: {job_id}")
        except Exception as e:
            logger.error(f"移除任务失败: {e}")
    
    def start(self):
        """启动调度器"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("定时任务调度器已启动")
    
    def shutdown(self):
        """关闭调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("定时任务调度器已关闭")
    
    def get_jobs(self):
        """获取所有任务列表"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        return jobs


# 全局调度器实例
scheduler_service = SchedulerService()