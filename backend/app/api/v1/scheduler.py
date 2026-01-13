"""
定时任务管理API路由
提供定时任务的创建、查询、删除接口
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.services.scheduler_service import scheduler_service

router = APIRouter()


class JobCreate(BaseModel):
    """创建任务请求"""
    username: str
    schedule_type: str = "daily"  # daily, hourly
    hour: Optional[int] = 2  # 仅用于daily
    minute: Optional[int] = 0  # 仅用于daily


class JobResponse(BaseModel):
    """任务响应"""
    id: str
    name: str
    next_run_time: Optional[str]
    trigger: str


@router.post("/jobs", response_model=dict)
async def create_job(job: JobCreate):
    """
    创建定时同步任务
    
    **参数:**
    - username: GitHub用户名
    - schedule_type: 调度类型 (daily/hourly)
    - hour: 执行时间（小时，仅daily模式）
    - minute: 执行时间（分钟，仅daily模式）
    """
    try:
        if job.schedule_type == "daily":
            scheduler_service.add_daily_sync_job(
                username=job.username,
                hour=job.hour,
                minute=job.minute
            )
            return {
                "message": f"已创建每日同步任务: {job.username}",
                "schedule": f"每天 {job.hour:02d}:{job.minute:02d}"
            }
        elif job.schedule_type == "hourly":
            scheduler_service.add_hourly_sync_job(username=job.username)
            return {
                "message": f"已创建每小时同步任务: {job.username}",
                "schedule": "每小时一次"
            }
        else:
            raise HTTPException(status_code=400, detail="无效的调度类型")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs", response_model=List[JobResponse])
async def list_jobs():
    """
    获取所有定时任务列表
    
    **返回:**
    - 任务ID
    - 任务名称
    - 下次执行时间
    - 触发器配置
    """
    jobs = scheduler_service.get_jobs()
    return jobs


@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    """
    删除定时任务
    
    **参数:**
    - job_id: 任务ID
    """
    try:
        scheduler_service.remove_job(job_id)
        return {"message": f"已删除任务: {job_id}"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"任务不存在: {job_id}")


@router.post("/jobs/{job_id}/trigger")
async def trigger_job(job_id: str):
    """
    立即触发任务执行
    
    **参数:**
    - job_id: 任务ID
    """
    try:
        # 获取任务
        job = scheduler_service.scheduler.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail=f"任务不存在: {job_id}")
        
        # 立即执行
        job.modify(next_run_time=None)
        
        return {"message": f"已触发任务执行: {job_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_scheduler_status():
    """
    获取调度器状态
    
    **返回:**
    - 运行状态
    - 任务数量
    """
    return {
        "running": scheduler_service.scheduler.running,
        "job_count": len(scheduler_service.scheduler.get_jobs()),
        "jobs": scheduler_service.get_jobs()
    }