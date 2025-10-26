"""
邮件相关模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseModel


class EmailAccount(BaseModel):
    """邮箱账户表"""
    
    __tablename__ = "email_accounts"
    __table_args__ = {'comment': '邮箱账户表'}
    
    # 邮箱信息
    email = Column(String(255), unique=True, nullable=False, index=True, comment="邮箱地址")
    display_name = Column(String(100), nullable=True, comment="显示名称")
    
    # SMTP配置
    smtp_host = Column(String(255), nullable=False, comment="SMTP服务器地址")
    smtp_port = Column(Integer, nullable=False, default=465, comment="SMTP端口")
    smtp_username = Column(String(255), nullable=False, comment="SMTP用户名")
    smtp_password = Column(String(500), nullable=False, comment="SMTP密码（加密存储）")
    use_tls = Column(Boolean, default=True, nullable=False, comment="是否使用TLS")
    
    # 配额管理
    daily_limit = Column(Integer, default=500, nullable=False, comment="每日发送限额")
    daily_sent_count = Column(Integer, default=0, nullable=False, comment="今日已发送数量")
    last_reset_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="最后重置时间")
    
    # 优先级和状态
    priority = Column(Integer, default=10, nullable=False, comment="优先级（数字越大优先级越高）")
    is_active = Column(Boolean, default=True, nullable=False, index=True, comment="是否启用")
    
    # 失败计数
    failure_count = Column(Integer, default=0, nullable=False, comment="连续失败次数")
    last_failure_at = Column(DateTime, nullable=True, comment="最后失败时间")
    
    # 备注
    remark = Column(String(500), nullable=True, comment="备注")
    
    def __repr__(self):
        return f"<EmailAccount(id={self.id}, email={self.email}, daily_sent={self.daily_sent_count}/{self.daily_limit})>"
    
    @property
    def is_available(self) -> bool:
        """是否可用"""
        return (
            self.is_active and 
            self.daily_sent_count < self.daily_limit and
            self.failure_count < 5  # 连续失败5次后暂停使用
        )
    
    def reset_daily_count(self):
        """重置每日计数"""
        self.daily_sent_count = 0
        self.last_reset_at = datetime.utcnow()
    
    def increment_sent_count(self):
        """增加发送计数"""
        self.daily_sent_count += 1
    
    def record_failure(self):
        """记录失败"""
        self.failure_count += 1
        self.last_failure_at = datetime.utcnow()
    
    def reset_failure_count(self):
        """重置失败计数"""
        self.failure_count = 0
        self.last_failure_at = None


class EmailAttachment(BaseModel):
    """邮件附件表"""
    
    __tablename__ = "email_attachments"
    __table_args__ = {'comment': '邮件附件表'}
    
    # 文件信息
    filename = Column(String(255), nullable=False, comment="文件名")
    original_filename = Column(String(255), nullable=False, comment="原始文件名")
    file_path = Column(String(500), nullable=False, comment="文件存储路径")
    file_size = Column(Integer, nullable=False, comment="文件大小（字节）")
    mime_type = Column(String(100), nullable=False, comment="MIME类型")
    
    # 关联信息
    message_id = Column(
        Integer,
        ForeignKey("message_records.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="关联的消息ID"
    )
    
    # 上传者
    uploaded_by = Column(String(100), nullable=True, comment="上传者")
    
    # 过期时间
    expires_at = Column(DateTime, nullable=True, comment="过期时间")
    
    # 状态
    is_uploaded = Column(Boolean, default=True, nullable=False, comment="是否已上传")
    
    def __repr__(self):
        return f"<EmailAttachment(id={self.id}, filename={self.filename}, size={self.file_size})>"
    
    @property
    def is_expired(self) -> bool:
        """是否已过期"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def size_kb(self) -> float:
        """文件大小（KB）"""
        return round(self.file_size / 1024, 2)
    
    @property
    def size_mb(self) -> float:
        """文件大小（MB）"""
        return round(self.file_size / (1024 * 1024), 2)


__all__ = ["EmailAccount", "EmailAttachment"]

