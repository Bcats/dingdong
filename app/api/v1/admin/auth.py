"""
管理员认证API
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.admin_user import AdminUser
from app.schemas.admin_user import AdminLoginRequest, AdminLoginResponse, AdminUserInfo
from app.schemas.common import ResponseModel
from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["管理员认证"])


@router.post("/login", response_model=ResponseModel[AdminLoginResponse], summary="管理员登录")
async def admin_login(
    request: Request,
    login_data: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """
    管理员登录接口
    
    - **username**: 用户名
    - **password**: 密码
    """
    # 查找用户
    admin_user = db.query(AdminUser).filter(
        AdminUser.username == login_data.username
    ).first()
    
    if not admin_user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 验证密码
    if not verify_password(login_data.password, admin_user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 检查是否激活
    if not admin_user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")
    
    # 更新登录信息
    admin_user.login_count += 1
    admin_user.last_login_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    admin_user.last_login_ip = request.client.host if request.client else None
    db.commit()
    
    # 生成JWT Token
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(admin_user.id),
            "username": admin_user.username,
            "type": "admin"  # 标记为管理员token
        },
        expires_delta=access_token_expires
    )
    
    # 返回响应
    return ResponseModel(
        code=0,
        message="登录成功",
        data=AdminLoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRE_MINUTES * 60,
            user_info=AdminUserInfo(
                id=admin_user.id,
                username=admin_user.username,
                nickname=admin_user.nickname,
                email=admin_user.email,
                is_superuser=admin_user.is_superuser,
                last_login_at=admin_user.last_login_at
            )
        )
    )


@router.get("/userinfo", response_model=AdminUserInfo, summary="获取当前用户信息")
async def get_current_user_info(
    # TODO: 添加JWT token验证依赖
    db: Session = Depends(get_db)
):
    """
    获取当前登录用户信息
    """
    # 这里需要从JWT token中获取用户ID
    # 暂时返回默认管理员信息
    raise HTTPException(status_code=501, detail="待实现")

