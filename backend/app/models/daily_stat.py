"""
每日统计数据模型 - SQLAlchemy ORM
"""
from sqlalchemy import Column, BigInteger, Date, Integer, String, DECIMAL, TIME, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base


class DailyStat(Base):
    """每日统计数据表"""
    
    __tablename__ = 'daily_stats'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='统计ID')
    
    # 外键
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='用户ID')
    
    # 统计日期
    stat_date = Column(Date, nullable=False, index=True, comment='统计日期')
    
    # 提交统计
    commits = Column(Integer, default=0, comment='提交次数')
    additions = Column(Integer, default=0, comment='新增代码行数')
    deletions = Column(Integer, default=0, comment='删除代码行数')
    
    # 活跃仓库数
    active_repos = Column(Integer, default=0, comment='活跃仓库数')
    
    # 主要语言
    primary_language = Column(String(50), comment='当日主要语言')
    
    # 工作时长
    work_hours = Column(DECIMAL(5, 2), default=0, comment='工作时长（小时）')
    
    # 工作时间
    first_commit_time = Column(TIME, comment='首次提交时间')
    last_commit_time = Column(TIME, comment='最后提交时间')
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='更新时间'
    )
    
    # 关系定义
    user = relationship('User', back_populates='daily_stats')
    
    def __repr__(self):
        return f"<DailyStat(id={self.id}, user_id={self.user_id}, date={self.stat_date})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stat_date': self.stat_date.isoformat() if self.stat_date else None,
            'commits': self.commits,
            'additions': self.additions,
            'deletions': self.deletions,
            'active_repos': self.active_repos,
            'primary_language': self.primary_language,
            'work_hours': float(self.work_hours) if self.work_hours else 0,
            'first_commit_time': self.first_commit_time.isoformat() if self.first_commit_time else None,
            'last_commit_time': self.last_commit_time.isoformat() if self.last_commit_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }