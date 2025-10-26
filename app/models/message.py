"""
消息记录模型
"""
from sqlalchemy import Column, Integer, String, Text, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class MessageStatus(str, enum.Enum):
    """消息状态"""
    PENDING = "pending"  # 待发送
    SENDING = "sending"  # 发送中
    SUCCESS = "success"  # 成功
    FAILED = "failed"    # 失败
    RETRYING = "retrying"  # 重试中


class MessageChannel(str, enum.Enum):
    """消息渠道"""
    EMAIL = "email"  # 邮件
    SMS = "sms"      # 短信
    WECHAT = "wechat"  # 微信
    WECHAT_OFFICIAL = "wechat_official"  # 微信公众号


class MessageRecord(BaseModel):
    """消息记录表"""
    
    __tablename__ = "message_records"
    __table_args__ = {'comment': '消息记录表'}
    
    # 基本信息
    channel = Column(
        SQLEnum(MessageChannel),
        nullable=False,
        index=True,
        comment="发送渠道: email/sms/wechat/wechat_official"
    )
    
    status = Column(
        SQLEnum(MessageStatus),
        default=MessageStatus.PENDING,
        nullable=False,
        index=True,
        comment="状态"
    )
    
    # 接收者信息
    to = Column(String(500), nullable=False, comment="接收者（邮箱/手机号/微信ID）")
    cc = Column(String(1000), nullable=True, comment="抄送（仅邮件）")
    bcc = Column(String(1000), nullable=True, comment="密送（仅邮件）")
    
    # 消息内容
    subject = Column(String(500), nullable=True, comment="主题/标题")
    content = Column(Text, nullable=False, comment="消息内容")
    content_type = Column(
        String(50),
        default="html",
        nullable=False,
        comment="内容类型: html/text/markdown"
    )
    
    # 模板信息
    template_id = Column(
        Integer,
        ForeignKey("message_templates.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="模板ID"
    )
    template_version = Column(Integer, nullable=True, comment="模板版本号")
    template_variables = Column(JSON, nullable=True, comment="模板变量")
    
    # 发送信息
    sender = Column(String(200), nullable=True, comment="发送者（邮箱/短信签名）")
    sent_at = Column(String(50), nullable=True, comment="实际发送时间")
    
    # 重试信息
    retry_count = Column(Integer, default=0, nullable=False, comment="重试次数")
    max_retry = Column(Integer, default=3, nullable=False, comment="最大重试次数")
    retry_logs = Column(JSON, nullable=True, comment="重试日志")
    
    # 错误信息
    error_code = Column(String(50), nullable=True, comment="错误码")
    error_message = Column(Text, nullable=True, comment="错误信息")
    
    # 去重和追踪
    idempotency_key = Column(
        String(100),
        nullable=True,
        unique=True,
        index=True,
        comment="幂等性键（防重复）"
    )
    request_id = Column(
        String(100),
        nullable=True,
        index=True,
        comment="请求ID（追踪）"
    )
    
    # 附加信息
    extra_data = Column(JSON, nullable=True, comment="附加元数据")
    
    # 关联关系
    template = relationship("MessageTemplate", back_populates="messages", foreign_keys=[template_id])
    
    def __repr__(self):
        return f"<MessageRecord(id={self.id}, channel={self.channel}, status={self.status}, to={self.to})>"


__all__ = ["MessageRecord", "MessageStatus", "MessageChannel"]

