"""
API v1 路由聚合
"""
from fastapi import APIRouter
from app.api.v1 import dashboard

api_router = APIRouter()

# 注册仪表板路由
api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["个人仪表板"]
)