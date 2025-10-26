"""
FastAPI应用入口
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

from app.core.config import settings
from app.core.logger import logger
from app.core.database import check_db_connection
from app.api.v1 import api_router


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="消息通知平台服务 - Message Notification Platform",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None,
)


# ==================== 中间件配置 ====================

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip压缩中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)


# ==================== Prometheus监控指标 ====================

if settings.PROMETHEUS_ENABLED:
    # 请求计数器
    REQUEST_COUNT = Counter(
        "http_requests_total",
        "Total HTTP requests",
        ["method", "endpoint", "status"]
    )
    
    # 请求延迟直方图
    REQUEST_LATENCY = Histogram(
        "http_request_duration_seconds",
        "HTTP request latency",
        ["method", "endpoint"]
    )
    
    # 消息发送计数器
    MESSAGE_SENT = Counter(
        "messages_sent_total",
        "Total messages sent",
        ["channel", "status"]
    )
    
    # 邮件发送计数器
    EMAIL_SENT = Counter(
        "emails_sent_total",
        "Total emails sent",
        ["status"]
    )


# ==================== 请求/响应中间件 ====================

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间和请求ID"""
    from app.core.security import generate_request_id
    
    # 生成或获取请求ID
    request_id = request.headers.get("X-Request-ID", generate_request_id())
    
    # 记录请求开始
    start_time = time.time()
    
    # 处理请求
    try:
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 添加响应头
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        
        # 记录Prometheus指标
        if settings.PROMETHEUS_ENABLED:
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(process_time)
        
        # 记录访问日志
        logger.info(
            f"{request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": f"{process_time:.4f}s",
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(
            f"Request error: {str(e)}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
            }
        )
        raise


# ==================== 异常处理器 ====================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "Internal server error",
            "data": None
        }
    )


# ==================== 启动/关闭事件 ====================

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENV}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # 检查数据库连接
    if check_db_connection():
        logger.info("Database connection successful")
    else:
        logger.error("Database connection failed")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info(f"Shutting down {settings.APP_NAME}")


# ==================== 路由注册 ====================

# 注册API v1路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# ==================== Prometheus指标端点 ====================

if settings.PROMETHEUS_ENABLED:
    @app.get("/metrics", include_in_schema=False)
    async def metrics():
        """Prometheus指标端点"""
        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )


# ==================== 根路径 ====================

@app.get("/", include_in_schema=False)
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENV,
        "docs": "/docs" if settings.is_development else "disabled",
    }


# ==================== 健康检查 ====================

@app.get("/health", include_in_schema=False)
async def health():
    """健康检查（顶层端点，方便外部监控）"""
    from datetime import datetime
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== 版本信息 ====================

@app.get("/version", include_in_schema=False)
async def version():
    """版本信息"""
    return {
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
        "environment": settings.ENV,
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_level=settings.LOG_LEVEL.lower(),
    )

