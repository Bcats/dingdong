"""
模板相关Schema
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.template import TemplateType


class TemplateCreate(BaseModel):
    """创建模板请求"""
    
    code: str = Field(..., max_length=100, description="模板编码（唯一）")
    name: str = Field(..., max_length=200, description="模板名称")
    type: TemplateType = Field(..., description="模板类型")
    description: Optional[str] = Field(None, description="模板描述")
    subject_template: Optional[str] = Field(None, max_length=500, description="主题模板")
    content_template: str = Field(..., description="内容模板")
    variables: Optional[Dict[str, Any]] = Field(None, description="变量定义")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "welcome_email",
                "name": "欢迎邮件",
                "type": "email",
                "subject_template": "欢迎{{name}}加入我们！",
                "content_template": "<h1>你好，{{name}}！</h1><p>欢迎加入{{company}}。</p>",
                "variables": {
                    "name": {"type": "string", "required": True, "description": "用户名"},
                    "company": {"type": "string", "required": True, "description": "公司名"}
                }
            }
        }


class TemplateUpdate(BaseModel):
    """更新模板请求"""
    
    name: Optional[str] = Field(None, max_length=200, description="模板名称")
    description: Optional[str] = Field(None, description="模板描述")
    subject_template: Optional[str] = Field(None, max_length=500, description="主题模板")
    content_template: Optional[str] = Field(None, description="内容模板")
    variables: Optional[Dict[str, Any]] = Field(None, description="变量定义")
    is_active: Optional[bool] = Field(None, description="是否启用")
    change_reason: Optional[str] = Field(None, max_length=500, description="变更原因")


class TemplateResponse(BaseModel):
    """模板响应"""
    
    id: int
    code: str
    name: str
    type: str
    description: Optional[str]
    subject_template: Optional[str]
    content_template: str
    variables: Optional[Dict[str, Any]]
    version: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TemplatePreviewRequest(BaseModel):
    """模板预览请求"""
    
    subject_template: Optional[str] = Field(None, description="主题模板")
    content_template: str = Field(..., description="内容模板")
    variables: Dict[str, Any] = Field(..., description="模板变量值")
    
    class Config:
        json_schema_extra = {
            "example": {
                "subject_template": "欢迎{{name}}！",
                "content_template": "<h1>你好，{{name}}！</h1>",
                "variables": {"name": "张三"}
            }
        }


class TemplatePreviewResponse(BaseModel):
    """模板预览响应"""
    
    subject: Optional[str] = Field(None, description="渲染后的主题")
    content: str = Field(..., description="渲染后的内容")


class TemplateHistoryResponse(BaseModel):
    """模板历史响应"""
    
    id: int
    version: int
    subject_template: Optional[str]
    content_template: str
    variables: Optional[Dict[str, Any]]
    change_reason: Optional[str]
    changed_by: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class TemplateRollbackRequest(BaseModel):
    """模板回滚请求"""
    
    target_version: int = Field(..., ge=1, description="目标版本号")
    change_reason: Optional[str] = Field(None, max_length=500, description="回滚原因")


__all__ = [
    "TemplateCreate",
    "TemplateUpdate",
    "TemplateResponse",
    "TemplatePreviewRequest",
    "TemplatePreviewResponse",
    "TemplateHistoryResponse",
    "TemplateRollbackRequest",
]

