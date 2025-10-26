"""
健康检查API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db, check_db_connection
from app.core.config import settings
from app.schemas import HealthResponse
from app.utils.redis_client import redis_client


router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """基本健康检查"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/health/ready", response_model=HealthResponse)
async def readiness_check(db: Session = Depends(get_db)):
    """就绪检查（检查所有依赖服务）"""
    checks = {}
    overall_status = "healthy"
    
    # 检查数据库
    try:
        db_ok = check_db_connection()
        checks["database"] = "healthy" if db_ok else "unhealthy"
        if not db_ok:
            overall_status = "unhealthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        overall_status = "unhealthy"
    
    # 检查Redis
    try:
        redis_ok = redis_client.ping()
        checks["redis"] = "healthy" if redis_ok else "unhealthy"
        if not redis_ok:
            overall_status = "unhealthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
        overall_status = "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow().isoformat(),
        checks=checks
    )


@router.get("/health/live", response_model=HealthResponse)
async def liveness_check():
    """存活检查（简单检查应用是否运行）"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow().isoformat()
    )


__all__ = ["router"]

