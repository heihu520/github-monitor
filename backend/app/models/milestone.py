"""
里程碑成就模型 - SQLAlchemy ORM
"""
from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Enum, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base


class MilestoneAchievement(Base):
    """里程碑成就表"""
    
    __tablename__ = 'milestone_achievements'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='成就ID')
    
    # 外键
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='用户ID')
    
    # 成就标识
    achievement_id = Column(String(50), nullable=False, comment='成就标识')
    
    # 成就分类
    category = Column(
        Enum('streak', 'commits', 'code', 'languages', 'special', name='achievement_category_enum'),
        nullable=False,
        index=True,
        comment='成就类别'
    )
    
    # 成就信息
    name = Column(String(100), nullable=False, comment='成就名称')
    description = Column(String(500), comment='成就描述')
    icon = Column(String(20), comment='成就图标emoji')
    
    # 进度信息
    threshold = Column(Integer, nullable=False, comment='达成阈值')
    current_value = Column(Integer, default=0, comment='当前值')
    
    # 达成状态
    achieved = Column(Boolean, default=False, index=True, comment='是否已达成')
    achieved_at = Column(TIMESTAMP, nullable=True, comment='达成时间')
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='更新时间'
    )
    
    # 关系定义
    user = relationship('User', back_populates='milestones')
    
    @property
    def progress(self):
        """计算进度百分比"""
        if self.threshold == 0:
            return 0.0
        return min(100.0, (self.current_value / self.threshold) * 100)
    
    def __repr__(self):
        return f"<MilestoneAchievement(id={self.id}, name='{self.name}', achieved={self.achieved})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'achievement_id': self.achievement_id,
            'category': self.category,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'threshold': self.threshold,
            'current_value': self.current_value,
            'progress': self.progress,
            'achieved': self.achieved,
            'achieved_at': self.achieved_at.isoformat() if self.achieved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }