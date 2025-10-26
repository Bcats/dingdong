"""
认证API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.models.api_key import APIKey
from app.schemas import TokenRequest, TokenResponse, ResponseModel
from app.core.logger import logger


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=ResponseModel[TokenResponse])
async def get_token(
    request: TokenRequest,
    db: Session = Depends(get_db)
):
    """
    获取访问令牌
    
    使用API Key和API Secret换取JWT Token
    """
    # 查询API Key
    api_key = (
        db.query(APIKey)
        .filter(
            APIKey.api_key == request.api_key,
            APIKey.is_active == True,
            APIKey.deleted_at == None
        )
        .first()
    )
    
    if not api_key:
        logger.warning(f"API Key not found: {request.api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API credentials"
        )
    
    # 检查是否过期
    if api_key.is_expired:
        logger.warning(f"API Key expired: {request.api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key expired"
        )
    
    # 验证API Secret
    if not verify_password(request.api_secret, api_key.api_secret_hash):
        logger.warning(f"Invalid API Secret for key: {request.api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API credentials"
        )
    
    # 创建Token
    token_data = {
        "api_key": api_key.api_key,
        "name": api_key.name
    }
    access_token = create_access_token(token_data)
    
    # 更新使用统计
    api_key.increment_usage()
    db.commit()
    
    logger.info(f"Token issued for API Key: {api_key.name}")
    
    return ResponseModel(
        code=0,
        message="Success",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRE_MINUTES * 60
        )
    )


__all__ = ["router"]

