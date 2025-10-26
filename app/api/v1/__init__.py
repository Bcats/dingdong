"""API v1版本路由"""
from fastapi import APIRouter

from app.api.v1 import health, auth, messages, templates, monitoring
from app.api.v1.admin import admin_router


# 创建v1路由器
api_router = APIRouter()

# 注册路由
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(messages.router)
api_router.include_router(templates.router)
api_router.include_router(monitoring.router)
api_router.include_router(admin_router)


__all__ = ["api_router"]
