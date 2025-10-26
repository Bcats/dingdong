"""
消息模板模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Enum as SQLEnum, JSON, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel, SoftDeleteMixin


class TemplateType(str, enum.Enum):
    """模板类型"""
    EMAIL = "email"  # 邮件模板
    SMS = "sms"      # 短信模板
    WECHAT = "wechat"  # 微信模板
    WECHAT_OFFICIAL = "wechat_official"  # 微信公众号模板


class MessageTemplate(BaseModel, SoftDeleteMixin):
    """消息模板表"""
    
    __tablename__ = "message_templates"
    __table_args__ = {'comment': '消息模板表'}
    
    # 基本信息
    code = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="模板编码（唯一标识）"
    )
    
    name = Column(String(200), nullable=False, comment="模板名称")
    
    type = Column(
        SQLEnum(TemplateType),
        nullable=False,
        index=True,
        comment="模板类型"
    )
    
    description = Column(Text, nullable=True, comment="模板描述")
    
    # 模板内容
    subject_template = Column(String(500), nullable=True, comment="主题模板（Jinja2语法）")
    content_template = Column(Text, nullable=False, comment="内容模板（Jinja2语法）")
    
    # 模板变量
    variables = Column(
        JSON,
        nullable=True,
        comment="模板变量定义 {\"name\": {\"type\": \"string\", \"required\": true, \"description\": \"用户名\"}}"
    )
    
    # 版本信息
    version = Column(Integer, default=1, nullable=False, comment="当前版本号")
    
    # 状态
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    
    # 创建者信息
    created_by = Column(String(100), nullable=True, comment="创建人")
    updated_by = Column(String(100), nullable=True, comment="更新人")
    
    # 关联关系
    messages = relationship("MessageRecord", back_populates="template", foreign_keys="MessageRecord.template_id")
    history = relationship("MessageTemplateHistory", back_populates="template", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MessageTemplate(id={self.id}, code={self.code}, name={self.name}, version={self.version})>"


class MessageTemplateHistory(BaseModel):
    """消息模板历史表"""
    
    __tablename__ = "message_template_history"
    __table_args__ = {'comment': '消息模板历史表'}
    
    # 关联的模板ID
    template_id = Column(
        Integer,
        ForeignKey("message_templates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="模板ID"
    )
    
    # 版本信息
    version = Column(Integer, nullable=False, comment="版本号")
    
    # 模板内容快照
    subject_template = Column(String(500), nullable=True, comment="主题模板快照")
    content_template = Column(Text, nullable=False, comment="内容模板快照")
    variables = Column(JSON, nullable=True, comment="变量定义快照")
    
    # 变更信息
    change_reason = Column(String(500), nullable=True, comment="变更原因")
    changed_by = Column(String(100), nullable=True, comment="变更人")
    
    # 关联关系
    template = relationship("MessageTemplate", back_populates="history")
    
    def __repr__(self):
        return f"<MessageTemplateHistory(id={self.id}, template_id={self.template_id}, version={self.version})>"


__all__ = ["MessageTemplate", "MessageTemplateHistory", "TemplateType"]

