"""
FastAPI 主应用入口
GitHub仓库监控工具 - 个人代码开发洞察系统
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import init_db, close_db, check_db_health
from app.services.scheduler_service import scheduler_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("正在初始化数据库连接...")
    # await init_db()  # 注释掉自动创建表，使用SQL脚本初始化
    
    print("正在启动定时任务调度器...")
    scheduler_service.start()
    
    print("应用启动完成")
    
    yield
    
    # 关闭时
    print("正在关闭定时任务调度器...")
    scheduler_service.shutdown()
    
    print("正在关闭数据库连接...")
    await close_db()
    
    print("应用已关闭")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="个人代码开发洞察和生产力分析系统",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "message": "GitHub Monitor API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """详细健康检查"""
    # 检查数据库连接
    db_status = "ok" if await check_db_health() else "error"
    
    # 检查调度器状态
    scheduler_status = "ok" if scheduler_service.scheduler.running else "stopped"
    
    return {
        "status": "healthy" if db_status == "ok" and scheduler_status == "ok" else "degraded",
        "api_version": "v1",
        "services": {
            "database": db_status,
            "scheduler": scheduler_status,
            "cache": "not_configured"  # Redis待集成
        },
        "scheduler": {
            "running": scheduler_service.scheduler.running,
            "job_count": len(scheduler_service.scheduler.get_jobs())
        }
    }