"""
管理员用户相关的Pydantic模型
"""
from typing import Optional
from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    """管理员登录请求"""
    username: str = Field(..., description="用户名", min_length=3, max_length=50)
    password: str = Field(..., description="密码", min_length=6, max_length=50)


class AdminUserInfo(BaseModel):
    """管理员用户信息"""
    id: int
    username: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    is_superuser: bool = False
    last_login_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class AdminLoginResponse(BaseModel):
    """管理员登录响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")
    user_info: AdminUserInfo = Field(..., description="用户信息")


class AdminUserCreate(BaseModel):
    """创建管理员"""
    username: str = Field(..., description="用户名", min_length=3, max_length=50)
    password: str = Field(..., description="密码", min_length=6, max_length=50)
    nickname: Optional[str] = Field(None, description="昵称", max_length=100)
    email: Optional[str] = Field(None, description="邮箱", max_length=100)
    phone: Optional[str] = Field(None, description="手机号", max_length=20)
    is_superuser: bool = Field(default=False, description="是否超级管理员")


class AdminUserUpdate(BaseModel):
    """更新管理员"""
    nickname: Optional[str] = Field(None, description="昵称", max_length=100)
    email: Optional[str] = Field(None, description="邮箱", max_length=100)
    phone: Optional[str] = Field(None, description="手机号", max_length=20)
    password: Optional[str] = Field(None, description="新密码", min_length=6, max_length=50)
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_superuser: Optional[bool] = Field(None, description="是否超级管理员")


class AdminUserResponse(BaseModel):
    """管理员响应"""
    id: int
    username: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    is_superuser: bool
    login_count: int
    last_login_at: Optional[str] = None
    last_login_ip: Optional[str] = None
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

