"""
通用Schema定义
"""
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field


DataT = TypeVar("DataT")


class ResponseModel(BaseModel, Generic[DataT]):
    """统一响应模型"""
    
    code: int = Field(..., description="状态码: 0-成功, 其他-失败")
    message: str = Field(..., description="响应消息")
    data: Optional[DataT] = Field(None, description="响应数据")
    request_id: Optional[str] = Field(None, description="请求ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "Success",
                "data": None,
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class PaginationModel(BaseModel):
    """分页模型"""
    
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=10000, description="每页数量")
    total: int = Field(0, ge=0, description="总数")
    total_pages: int = Field(0, ge=0, description="总页数")
    
    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "page_size": 20,
                "total": 100,
                "total_pages": 5
            }
        }


class PagedResponse(BaseModel, Generic[DataT]):
    """分页响应模型"""
    
    items: list[DataT] = Field(default_factory=list, description="数据列表")
    pagination: PaginationModel = Field(..., description="分页信息")


class HealthResponse(BaseModel):
    """健康检查响应"""
    
    status: str = Field(..., description="状态: healthy/unhealthy")
    version: str = Field(..., description="版本号")
    timestamp: str = Field(..., description="时间戳")
    checks: Optional[dict[str, Any]] = Field(None, description="详细检查结果")


__all__ = [
    "ResponseModel",
    "PaginationModel",
    "PagedResponse",
    "HealthResponse",
]

