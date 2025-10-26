"""Admin API模块"""
from fastapi import APIRouter

from app.api.v1.admin import auth, email_accounts


# 创建admin路由器
admin_router = APIRouter(prefix="/admin", tags=["Admin"])

# 注册路由
admin_router.include_router(auth.router)
admin_router.include_router(email_accounts.router)


__all__ = ["admin_router"]

