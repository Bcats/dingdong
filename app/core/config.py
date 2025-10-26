"""
应用配置管理
使用Pydantic Settings进行配置管理和验证
"""
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ==================== 环境配置 ====================
    ENV: str = Field(default="development", description="环境: development/staging/production")
    DEBUG: bool = Field(default=False, description="调试模式")
    LOG_LEVEL: str = Field(default="INFO", description="日志级别")
    TZ: str = Field(default="Asia/Shanghai", description="时区")
    
    # ==================== 应用配置 ====================
    APP_NAME: str = Field(default="notification-platform", description="应用名称")
    APP_VERSION: str = Field(default="1.0.0", description="应用版本")
    SECRET_KEY: str = Field(..., description="应用密钥")
    ALLOWED_HOSTS: str = Field(default="*", description="允许的主机")
    
    # ==================== 数据库配置 ====================
    DATABASE_URL: str = Field(..., description="数据库连接URL")
    DB_POOL_SIZE: int = Field(default=5, description="连接池大小")
    DB_MAX_OVERFLOW: int = Field(default=15, description="最大溢出连接数")
    DB_POOL_TIMEOUT: int = Field(default=30, description="连接超时(秒)")
    DB_POOL_RECYCLE: int = Field(default=3600, description="连接回收时间(秒)")
    DB_ECHO: bool = Field(default=False, description="是否打印SQL")
    
    # ==================== Redis配置 ====================
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis连接URL")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis密码")
    REDIS_MAX_CONNECTIONS: int = Field(default=50, description="最大连接数")
    REDIS_SOCKET_TIMEOUT: int = Field(default=5, description="Socket超时(秒)")
    REDIS_SOCKET_CONNECT_TIMEOUT: int = Field(default=5, description="连接超时(秒)")
    
    # ==================== RabbitMQ配置 ====================
    RABBITMQ_URL: str = Field(..., description="RabbitMQ连接URL")
    RABBITMQ_PREFETCH_COUNT: int = Field(default=10, description="消费者预取数量")
    RABBITMQ_HEARTBEAT: int = Field(default=60, description="心跳间隔(秒)")
    
    # ==================== JWT配置 ====================
    JWT_SECRET_KEY: str = Field(..., description="JWT密钥")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT算法")
    JWT_EXPIRE_MINUTES: int = Field(default=60, description="Token有效期(分钟)")
    JWT_REFRESH_EXPIRE_DAYS: int = Field(default=7, description="刷新Token有效期(天)")
    
    # ==================== 加密配置 ====================
    ENCRYPTION_KEY: str = Field(..., description="数据加密密钥(Fernet)")
    
    # ==================== SMTP配置 ====================
    EMAIL_TIMEOUT: int = Field(default=30, description="SMTP超时(秒)")
    EMAIL_MAX_SIZE: int = Field(default=20971520, description="邮件最大大小(字节,20MB)")
    EMAIL_USE_TLS: bool = Field(default=True, description="是否使用TLS")
    
    # ==================== 附件配置 ====================
    ATTACHMENT_STORAGE_PATH: str = Field(default="/data/attachments", description="附件存储路径")
    ATTACHMENT_MAX_SIZE: int = Field(default=10485760, description="单个附件最大大小(字节,10MB)")
    ATTACHMENT_EXPIRE_DAYS: int = Field(default=7, description="附件保留天数")
    
    # ==================== Celery配置 ====================
    CELERY_BROKER_URL: str = Field(..., description="Celery Broker URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/1", description="Celery结果后端")
    CELERY_WORKER_CONCURRENCY: int = Field(default=4, description="Worker并发数")
    CELERY_TASK_TIME_LIMIT: int = Field(default=300, description="任务超时(秒)")
    CELERY_TASK_SOFT_TIME_LIMIT: int = Field(default=270, description="任务软超时(秒)")
    
    # ==================== 监控配置 ====================
    PROMETHEUS_ENABLED: bool = Field(default=True, description="是否启用Prometheus")
    METRICS_PORT: int = Field(default=9090, description="监控指标端口")
    
    # ==================== 限流配置 ====================
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="是否启用限流")
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, description="每分钟请求限制")
    
    # ==================== API配置 ====================
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1前缀")
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="CORS允许的源"
    )
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """解析CORS配置"""
        if isinstance(v, str):
            # 支持从环境变量中解析JSON数组
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # 支持逗号分隔的字符串
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    @validator("DEBUG", pre=True)
    def parse_debug(cls, v):
        """解析DEBUG配置"""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return v
    
    @validator("DB_ECHO", "EMAIL_USE_TLS", "PROMETHEUS_ENABLED", "RATE_LIMIT_ENABLED", pre=True)
    def parse_bool(cls, v):
        """解析布尔配置"""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return v
    
    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.ENV == "production"
    
    @property
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.ENV == "development"
    
    @property
    def database_url_async(self) -> str:
        """异步数据库连接URL"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


# 创建全局配置实例
settings = Settings()


# 导出配置
__all__ = ["settings", "Settings"]

