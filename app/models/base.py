"""
数据库模型基类
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr

from app.core.database import Base


class TimeStampMixin:
    """时间戳混入类"""
    
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    
    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=datetime.now,
            onupdate=datetime.now,
            nullable=False,
            comment="更新时间"
        )


class SoftDeleteMixin:
    """软删除混入类"""
    
    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True, comment="删除时间")
    
    @property
    def is_deleted(self) -> bool:
        """是否已删除"""
        return self.deleted_at is not None
    
    def soft_delete(self):
        """软删除"""
        self.deleted_at = datetime.now()
    
    def restore(self):
        """恢复"""
        self.deleted_at = None


class BaseModel(Base, TimeStampMixin):
    """基础模型类"""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    
    def to_dict(self):
        """转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self):
        """字符串表示"""
        return f"<{self.__class__.__name__}(id={self.id})>"


__all__ = ["Base", "BaseModel", "TimeStampMixin", "SoftDeleteMixin"]

