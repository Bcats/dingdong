"""
API密钥模型
"""
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from datetime import datetime

from app.models.base import BaseModel, SoftDeleteMixin


class APIKey(BaseModel, SoftDeleteMixin):
    """API密钥表"""
    
    __tablename__ = "api_keys"
    __table_args__ = {'comment': 'API密钥表'}
    
    # API密钥信息
    api_key = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="API Key（公开）"
    )
    
    api_secret_hash = Column(
        String(255),
        nullable=False,
        comment="API Secret哈希值（bcrypt）"
    )
    
    # 密钥名称和描述
    name = Column(String(100), nullable=False, comment="密钥名称")
    description = Column(String(500), nullable=True, comment="密钥描述")
    
    # 状态
    is_active = Column(Boolean, default=True, nullable=False, index=True, comment="是否启用")
    
    # 使用统计
    last_used_at = Column(DateTime, nullable=True, comment="最后使用时间")
    usage_count = Column(Integer, default=0, nullable=False, comment="使用次数")
    
    # 过期时间
    expires_at = Column(DateTime, nullable=True, comment="过期时间（NULL表示永不过期）")
    
    # 权限范围（预留字段，后期扩展）
    # scopes = Column(JSON, nullable=True, comment="权限范围")
    
    # 创建者
    created_by = Column(String(100), nullable=True, comment="创建人")
    
    def __repr__(self):
        return f"<APIKey(id={self.id}, name={self.name}, api_key={self.api_key[:20]}...)>"
    
    @property
    def is_expired(self) -> bool:
        """是否已过期"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """是否有效"""
        return self.is_active and not self.is_expired and not self.is_deleted
    
    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()


__all__ = ["APIKey"]

