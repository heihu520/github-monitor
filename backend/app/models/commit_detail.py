"""
提交详情数据模型 - SQLAlchemy ORM
"""
from sqlalchemy import Column, BigInteger, String, Integer, TIMESTAMP, TEXT, ForeignKey, func, SMALLINT
from sqlalchemy.orm import relationship

from .base import Base


class CommitDetail(Base):
    """提交详细信息表"""
    
    __tablename__ = 'commit_details'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='提交ID')
    
    # 外键
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='用户ID')
    repo_id = Column(BigInteger, ForeignKey('repositories.id', ondelete='CASCADE'), nullable=False, index=True, comment='仓库ID')
    
    # 提交信息
    commit_sha = Column(String(40), unique=True, nullable=False, comment='提交SHA值')
    commit_message = Column(TEXT, comment='提交信息')
    commit_date = Column(TIMESTAMP, nullable=False, index=True, comment='提交时间')
    
    # 代码变更统计
    additions = Column(Integer, default=0, comment='新增行数')
    deletions = Column(Integer, default=0, comment='删除行数')
    files_changed = Column(Integer, default=0, comment='修改文件数')
    
    # 语言信息
    primary_language = Column(String(50), comment='主要语言')
    
    # 时间分析字段
    commit_hour = Column(SMALLINT, index=True, comment='提交小时（0-23）')
    commit_weekday = Column(SMALLINT, comment='提交星期（0-6，0=周日）')
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment='创建时间')
    
    # 关系定义
    user = relationship('User', back_populates='commits')
    repository = relationship('Repository', back_populates='commits')
    
    def __repr__(self):
        return f"<CommitDetail(id={self.id}, sha='{self.commit_sha[:7]}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'repo_id': self.repo_id,
            'commit_sha': self.commit_sha,
            'commit_message': self.commit_message,
            'commit_date': self.commit_date.isoformat() if self.commit_date else None,
            'additions': self.additions,
            'deletions': self.deletions,
            'files_changed': self.files_changed,
            'primary_language': self.primary_language,
            'commit_hour': self.commit_hour,
            'commit_weekday': self.commit_weekday,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }