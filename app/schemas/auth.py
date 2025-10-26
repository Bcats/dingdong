"""
认证相关Schema
"""
from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    """Token请求"""
    
    api_key: str = Field(..., description="API Key")
    api_secret: str = Field(..., description="API Secret")
    
    class Config:
        json_schema_extra = {
            "example": {
                "api_key": "noti_abc123def456",
                "api_secret": "secret_xyz789"
            }
        }


class TokenResponse(BaseModel):
    """Token响应"""
    
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


__all__ = ["TokenRequest", "TokenResponse"]

