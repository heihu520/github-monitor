"""
SQLAlchemy Base声明基类
"""
from sqlalchemy.ext.declarative import declarative_base

# 创建基类
Base = declarative_base()

# 所有模型都将继承此Base类