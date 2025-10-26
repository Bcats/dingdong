"""
API依赖项
"""
from typing import Optional, Union
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.api_key import APIKey
from app.models.admin_user import AdminUser
from app.core.logger import logger


# HTTP Bearer Token安全方案
security = HTTPBearer()
# 可选的Bearer Token（不强制要求）
optional_security = HTTPBearer(auto_error=False)


async def get_current_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> APIKey:
    """
    获取当前API Key（通过JWT Token）
    
    Args:
        credentials: 认证凭证
        db: 数据库会话
        
    Returns:
        APIKey: API Key对象
        
    Raises:
        HTTPException: 认证失败
    """
    token = credentials.credentials
    
    # 解码Token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查Token类型
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取API Key
    api_key_str = payload.get("api_key")
    if not api_key_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 查询API Key
    api_key = (
        db.query(APIKey)
        .filter(
            APIKey.api_key == api_key_str,
            APIKey.is_active == True,
            APIKey.deleted_at == None
        )
        .first()
    )
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查是否过期
    if api_key.is_expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 更新使用统计
    api_key.increment_usage()
    db.commit()
    
    logger.debug(f"API Key authenticated: {api_key.name}")
    return api_key


async def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AdminUser:
    """
    获取当前管理员用户（通过JWT Token）
    
    Args:
        credentials: 认证凭证
        db: 数据库会话
        
    Returns:
        AdminUser: 管理员用户对象
        
    Raises:
        HTTPException: 认证失败
    """
    token = credentials.credentials
    
    # 解码Token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查Token类型
    if payload.get("type") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 查询管理员用户
    admin_user = (
        db.query(AdminUser)
        .filter(
            AdminUser.id == int(user_id),
            AdminUser.is_active == True
        )
        .first()
    )
    
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.debug(f"Admin user authenticated: {admin_user.username}")
    return admin_user


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security),
    db: Session = Depends(get_db)
) -> Union[AdminUser, APIKey]:
    """
    获取当前用户（管理员或API Key）
    
    同时支持管理员Token和API Key Token
    
    Args:
        credentials: 认证凭证
        db: 数据库会话
        
    Returns:
        Union[AdminUser, APIKey]: 管理员用户或API Key对象
        
    Raises:
        HTTPException: 认证失败
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # 解码Token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_type = payload.get("type")
    
    # 根据token类型返回不同的用户对象
    if token_type == "admin":
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        admin_user = (
            db.query(AdminUser)
            .filter(
                AdminUser.id == int(user_id),
                AdminUser.is_active == True
            )
            .first()
        )
        
        if not admin_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin user not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return admin_user
    
    elif token_type == "access":
        api_key_str = payload.get("api_key")
        if not api_key_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        api_key = (
            db.query(APIKey)
            .filter(
                APIKey.api_key == api_key_str,
                APIKey.is_active == True,
                APIKey.deleted_at == None
            )
            .first()
        )
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if api_key.is_expired:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 更新使用统计
        api_key.increment_usage()
        db.commit()
        
        return api_key
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_request_id(
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID")
) -> Optional[str]:
    """
    获取请求ID
    
    Args:
        x_request_id: 请求ID头
        
    Returns:
        Optional[str]: 请求ID
    """
    return x_request_id


__all__ = [
    "get_current_api_key",
    "get_current_admin_user", 
    "get_current_user",
    "get_request_id",
    "security",
    "optional_security"
]

