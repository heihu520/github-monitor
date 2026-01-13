"""
编码目标模型 - SQLAlchemy ORM
"""
from sqlalchemy import Column, BigInteger, String, Integer, Date, Enum, TIMESTAMP, TEXT, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base


class CodingGoal(Base):
    """编码目标表"""
    
    __tablename__ = 'coding_goals'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='目标ID')
    
    # 外键
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='用户ID')
    
    # 目标类型
    goal_type = Column(
        Enum('daily_commits', 'code_volume', 'skill_learning', 'streak', 'custom', name='goal_type_enum'),
        nullable=False,
        index=True,
        comment='目标类型'
    )
    
    # 目标信息
    title = Column(String(200), nullable=False, comment='目标标题')
    description = Column(TEXT, comment='目标描述')
    
    # 目标值
    target_value = Column(Integer, nullable=False, comment='目标值')
    current_value = Column(Integer, default=0, comment='当前值')
    unit = Column(String(20), default='count', comment='单位（count/lines/hours等）')
    
    # 时间范围
    start_date = Column(Date, nullable=False, comment='开始日期')
    end_date = Column(Date, nullable=False, index=True, comment='结束日期')
    
    # 状态
    status = Column(
        Enum('active', 'completed', 'failed', 'cancelled', name='goal_status_enum'),
        default='active',
        index=True,
        comment='目标状态'
    )
    
    # 完成时间
    completed_at = Column(TIMESTAMP, nullable=True, comment='完成时间')
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='更新时间'
    )
    
    # 关系定义
    user = relationship('User', back_populates='goals')
    
    @property
    def progress(self):
        """计算进度百分比"""
        if self.target_value == 0:
            return 0.0
        return min(100.0, (self.current_value / self.target_value) * 100)
    
    def __repr__(self):
        return f"<CodingGoal(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'goal_type': self.goal_type,
            'title': self.title,
            'description': self.description,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'progress': self.progress,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }