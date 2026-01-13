"""
用户数据模型 - SQLAlchemy ORM
"""
from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class User(Base):
    """用户信息表"""
    
    __tablename__ = 'users'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    
    # 基本信息
    username = Column(String(100), unique=True, nullable=False, index=True, comment='GitHub用户名')
    email = Column(String(255), comment='邮箱')
    github_token = Column(String(255), comment='GitHub访问令牌（加密存储）')
    avatar_url = Column(String(500), comment='头像URL')
    
    # 统计数据
    total_repos = Column(Integer, default=0, comment='总仓库数')
    total_commits = Column(Integer, default=0, comment='总提交数')
    total_additions = Column(BigInteger, default=0, comment='总新增代码行数')
    total_deletions = Column(BigInteger, default=0, comment='总删除代码行数')
    
    # 连续编码统计
    streak_days = Column(Integer, default=0, comment='当前连续编码天数')
    max_streak_days = Column(Integer, default=0, comment='历史最大连续天数')
    
    # 活跃语言
    active_language = Column(String(50), comment='最活跃编程语言')
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(
        TIMESTAMP, 
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='更新时间'
    )
    
    # 关系定义
    repositories = relationship('Repository', back_populates='user', cascade='all, delete-orphan')
    daily_stats = relationship('DailyStat', back_populates='user', cascade='all, delete-orphan')
    commits = relationship('CommitDetail', back_populates='user', cascade='all, delete-orphan')
    language_stats = relationship('LanguageStat', back_populates='user', cascade='all, delete-orphan')
    milestones = relationship('MilestoneAchievement', back_populates='user', cascade='all, delete-orphan')
    goals = relationship('CodingGoal', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'total_repos': self.total_repos,
            'total_commits': self.total_commits,
            'total_additions': self.total_additions,
            'total_deletions': self.total_deletions,
            'streak_days': self.streak_days,
            'max_streak_days': self.max_streak_days,
            'active_language': self.active_language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }