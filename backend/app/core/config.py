"""
应用配置管理
使用Pydantic Settings进行配置验证和环境变量加载
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置类"""
    
    # 项目基本信息
    PROJECT_NAME: str = "GitHub Monitor API"
    API_V1_STR: str = "/api/v1"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite开发服务器
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # 数据库配置（MySQL）
    DATABASE_URL: str = Field(
        default="mysql+aiomysql://hadoop:hadoop@localhost:3306/github_monitor",
        description="MySQL数据库连接URL"
    )
    
    # Redis配置
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis缓存连接URL"
    )
    
    # GitHub API配置
    GITHUB_API_URL: str = "https://api.github.com"
    GITHUB_GRAPHQL_URL: str = "https://api.github.com/graphql"
    GITHUB_TOKEN: str = Field(
        default="",
        description="GitHub Personal Access Token"
    )
    
    # JWT密钥
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT签名密钥"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 应用设置
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # 允许额外字段


settings = Settings()