"""
仓库数据模型 - SQLAlchemy ORM
"""
from sqlalchemy import Column, BigInteger, String, Integer, Boolean, TEXT, TIMESTAMP, ForeignKey, JSON, func
from sqlalchemy.orm import relationship

from .base import Base


class Repository(Base):
    """仓库信息表"""
    
    __tablename__ = 'repositories'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='仓库ID')
    
    # 外键
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='用户ID')
    
    # GitHub信息
    github_repo_id = Column(BigInteger, nullable=False, comment='GitHub仓库ID')
    repo_name = Column(String(255), nullable=False, index=True, comment='仓库名称（owner/repo）')
    description = Column(TEXT, comment='仓库描述')
    language = Column(String(50), comment='主要编程语言')
    
    # 统计数据
    stars = Column(Integer, default=0, comment='Star数')
    forks = Column(Integer, default=0, comment='Fork数')
    
    # 属性
    is_private = Column(Boolean, default=False, comment='是否私有仓库')
    category_tags = Column(JSON, comment='分类标签数组')
    
    # 时间戳
    last_commit_at = Column(TIMESTAMP, nullable=True, index=True, comment='最后提交时间')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='更新时间'
    )
    
    # 关系定义
    user = relationship('User', back_populates='repositories')
    commits = relationship('CommitDetail', back_populates='repository', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Repository(id={self.id}, repo_name='{self.repo_name}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'github_repo_id': self.github_repo_id,
            'repo_name': self.repo_name,
            'description': self.description,
            'language': self.language,
            'stars': self.stars,
            'forks': self.forks,
            'is_private': self.is_private,
            'category_tags': self.category_tags,
            'last_commit_at': self.last_commit_at.isoformat() if self.last_commit_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }