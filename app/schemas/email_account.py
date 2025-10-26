"""
邮箱账户Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class EmailAccountBase(BaseModel):
    """邮箱账户基础模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    display_name: Optional[str] = Field(None, description="显示名称")
    smtp_host: str = Field(..., description="SMTP服务器地址")
    smtp_port: int = Field(465, description="SMTP端口")
    smtp_username: str = Field(..., description="SMTP用户名")
    use_tls: bool = Field(True, description="是否使用TLS")
    daily_limit: int = Field(500, description="每日发送限额")
    priority: int = Field(10, description="优先级（数字越大优先级越高）")
    is_active: bool = Field(True, description="是否启用")
    remark: Optional[str] = Field(None, description="备注")


class EmailAccountCreate(EmailAccountBase):
    """创建邮箱账户"""
    smtp_password: str = Field(..., description="SMTP密码")


class EmailAccountUpdate(BaseModel):
    """更新邮箱账户"""
    display_name: Optional[str] = Field(None, description="显示名称")
    smtp_host: Optional[str] = Field(None, description="SMTP服务器地址")
    smtp_port: Optional[int] = Field(None, description="SMTP端口")
    smtp_username: Optional[str] = Field(None, description="SMTP用户名")
    smtp_password: Optional[str] = Field(None, description="SMTP密码（如需修改）")
    use_tls: Optional[bool] = Field(None, description="是否使用TLS")
    daily_limit: Optional[int] = Field(None, description="每日发送限额")
    priority: Optional[int] = Field(None, description="优先级")
    is_active: Optional[bool] = Field(None, description="是否启用")
    remark: Optional[str] = Field(None, description="备注")


class EmailAccountResponse(BaseModel):
    """邮箱账户响应"""
    id: int
    email: str
    display_name: Optional[str]
    smtp_host: str
    smtp_port: int
    smtp_username: str
    use_tls: bool
    daily_limit: int
    daily_sent_count: int
    last_reset_at: datetime
    priority: int
    is_active: bool
    failure_count: int
    last_failure_at: Optional[datetime]
    remark: Optional[str]
    is_available: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class EmailAccountTestRequest(BaseModel):
    """测试邮箱连接请求"""
    test_email: Optional[EmailStr] = Field(None, description="测试接收邮箱（可选，默认发送到账户自己）")


class EmailAccountTestResponse(BaseModel):
    """测试邮箱连接响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="测试结果消息")
    error: Optional[str] = Field(None, description="错误信息")
    duration_ms: Optional[float] = Field(None, description="连接耗时（毫秒）")


__all__ = [
    "EmailAccountCreate",
    "EmailAccountUpdate",
    "EmailAccountResponse",
    "EmailAccountTestRequest",
    "EmailAccountTestResponse",
]

