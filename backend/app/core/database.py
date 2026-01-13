"""
数据库连接管理
使用SQLAlchemy异步引擎和会话管理
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
import logging

from .config import settings
from ..models.base import Base

# 配置日志
logger = logging.getLogger(__name__)

# 创建异步数据库引擎
# 使用aiomysql驱动（需要安装: pip install aiomysql）
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # 开发环境打印SQL语句
    pool_pre_ping=True,  # 连接前测试连接是否有效
    pool_recycle=3600,  # 1小时回收连接
    poolclass=NullPool if settings.DEBUG else None,  # 开发环境不使用连接池
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 提交后对象不过期
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话的依赖注入函数
    用于FastAPI路由的Depends()
    
    使用示例:
    @app.get("/users")
    async def get_users(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User))
        return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"数据库会话错误: {e}")
            raise
        finally:
            await session.close()


async def init_db():
    """
    初始化数据库
    创建所有表（仅用于开发环境，生产环境应使用迁移工具）
    """
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表创建成功")


async def close_db():
    """
    关闭数据库连接
    应用关闭时调用
    """
    await engine.dispose()
    logger.info("数据库连接已关闭")


# 数据库健康检查
async def check_db_health() -> bool:
    """
    检查数据库连接是否正常
    返回: True=正常, False=异常
    """
    try:
        async with AsyncSessionLocal() as session:
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))
            return True
    except Exception as e:
        logger.error(f"数据库健康检查失败: {e}")
        return False