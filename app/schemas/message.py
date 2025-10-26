"""
消息相关Schema
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, validator

from app.models.message import MessageStatus, MessageChannel


class EmailSendRequest(BaseModel):
    """邮件发送请求"""
    
    # 模式1：直接指定内容
    to: List[EmailStr] = Field(..., min_items=1, description="收件人列表")
    subject: Optional[str] = Field(None, description="邮件主题")
    content: Optional[str] = Field(None, description="邮件内容(HTML)")
    cc: Optional[List[EmailStr]] = Field(None, description="抄送列表")
    bcc: Optional[List[EmailStr]] = Field(None, description="密送列表")
    
    # 模式2：使用模板
    template_code: Optional[str] = Field(None, description="模板编码")
    template_variables: Optional[Dict[str, Any]] = Field(None, description="模板变量")
    
    # 附件和其他
    attachment_ids: Optional[List[int]] = Field(None, description="附件ID列表")
    idempotency_key: Optional[str] = Field(None, max_length=100, description="幂等性键(防重复)")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="附加元数据")
    
    @validator("to", "cc", "bcc", pre=True)
    def convert_to_list(cls, v):
        """将单个邮箱转换为列表"""
        if isinstance(v, str):
            return [v]
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "to": ["user@example.com"],
                "subject": "测试邮件",
                "content": "<h1>Hello</h1><p>This is a test email.</p>",
                "idempotency_key": "unique-key-123"
            }
        }


class EmailSendResponse(BaseModel):
    """邮件发送响应"""
    
    message_id: int = Field(..., description="消息ID")
    status: str = Field(..., description="状态")
    request_id: str = Field(..., description="请求ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message_id": 12345,
                "status": "pending",
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class MessageQuery(BaseModel):
    """消息查询参数"""
    
    channel: Optional[MessageChannel] = Field(None, description="渠道")
    status: Optional[MessageStatus] = Field(None, description="状态")
    to: Optional[str] = Field(None, description="接收者(模糊查询)")
    request_id: Optional[str] = Field(None, description="请求ID")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class MessageResponse(BaseModel):
    """消息响应"""
    
    id: int
    channel: str
    status: str
    to: str
    subject: Optional[str]
    content: Optional[str]
    sender: Optional[str]
    retry_count: int
    max_retry: int
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[str]
    error_message: Optional[str]
    request_id: Optional[str]
    
    class Config:
        from_attributes = True


class BatchQueryRequest(BaseModel):
    """批量查询请求"""
    
    message_ids: List[int] = Field(..., min_items=1, max_items=100, description="消息ID列表")


__all__ = [
    "EmailSendRequest",
    "EmailSendResponse",
    "MessageQuery",
    "MessageResponse",
    "BatchQueryRequest",
]

