"""
数据库模型模块
"""
from app.models.base import Base, BaseModel, TimeStampMixin, SoftDeleteMixin
from app.models.message import MessageRecord, MessageStatus, MessageChannel
from app.models.template import MessageTemplate, MessageTemplateHistory, TemplateType
from app.models.email import EmailAccount, EmailAttachment
from app.models.api_key import APIKey
from app.models.admin_user import AdminUser


__all__ = [
    # 基类
    "Base",
    "BaseModel",
    "TimeStampMixin",
    "SoftDeleteMixin",
    
    # 消息相关
    "MessageRecord",
    "MessageStatus",
    "MessageChannel",
    
    # 模板相关
    "MessageTemplate",
    "MessageTemplateHistory",
    "TemplateType",
    
    # 邮件相关
    "EmailAccount",
    "EmailAttachment",
    
    # API密钥
    "APIKey",
    
    # 管理员
    "AdminUser",
]
