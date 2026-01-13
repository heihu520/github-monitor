"""
编程语言统计模型 - SQLAlchemy ORM
"""
from sqlalchemy import Column, BigInteger, String, Integer, Enum, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base


class LanguageStat(Base):
    """编程语言统计表"""
    
    __tablename__ = 'language_stats'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='统计ID')
    
    # 外键
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='用户ID')
    
    # 语言信息
    language = Column(String(50), nullable=False, index=True, comment='编程语言')
    
    # 统计数据
    total_commits = Column(Integer, default=0, comment='总提交次数')
    total_additions = Column(BigInteger, default=0, comment='总新增行数')
    total_deletions = Column(BigInteger, default=0, comment='总删除行数')
    total_files = Column(Integer, default=0, comment='总文件数')
    
    # 熟练度等级
    proficiency_level = Column(
        Enum('beginner', 'intermediate', 'proficient', 'expert', name='proficiency_enum'),
        default='beginner',
        comment='熟练度等级'
    )
    
    # 使用时间
    first_used_at = Column(TIMESTAMP, nullable=True, comment='首次使用时间')
    last_used_at = Column(TIMESTAMP, nullable=True, comment='最近使用时间')
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='更新时间'
    )
    
    # 关系定义
    user = relationship('User', back_populates='language_stats')
    
    def __repr__(self):
        return f"<LanguageStat(id={self.id}, language='{self.language}', level='{self.proficiency_level}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'language': self.language,
            'total_commits': self.total_commits,
            'total_additions': self.total_additions,
            'total_deletions': self.total_deletions,
            'total_files': self.total_files,
            'proficiency_level': self.proficiency_level,
            'first_used_at': self.first_used_at.isoformat() if self.first_used_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }