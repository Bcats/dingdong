"""
日志配置
使用loguru进行日志管理，支持JSON格式输出
"""
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict
from datetime import datetime
from loguru import logger as loguru_logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
    """
    拦截标准logging，转发到loguru
    """
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def serialize(record: Dict[str, Any]) -> str:
    """
    序列化日志记录为JSON格式
    """
    subset = {
        "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "level": record["level"].name,
        "message": record["message"],
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
    }
    
    # 添加额外字段
    if record.get("extra"):
        subset.update(record["extra"])
    
    # 添加异常信息
    if record.get("exception"):
        subset["exception"] = {
            "type": record["exception"].type.__name__,
            "value": str(record["exception"].value),
            "traceback": record["exception"].traceback
        }
    
    return json.dumps(subset, ensure_ascii=False, default=str)


def patching(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    添加自定义字段到日志记录
    """
    record["extra"]["app_name"] = settings.APP_NAME
    record["extra"]["env"] = settings.ENV
    return record


def format_record(record: Dict[str, Any]) -> str:
    """
    格式化日志记录
    生产环境使用JSON格式，开发环境使用可读格式
    """
    if settings.is_production:
        return serialize(record) + "\n"
    else:
        # 开发环境使用彩色格式
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>\n"
        )
        if record.get("exception"):
            format_string += "{exception}\n"
        return format_string


def init_logging():
    """
    初始化日志配置
    """
    # 移除默认的handler
    loguru_logger.remove()
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 控制台输出
    loguru_logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=format_record,
        colorize=not settings.is_production,
        backtrace=True,
        diagnose=settings.is_development,
        enqueue=True,  # 异步日志
    )
    
    # 文件输出 - 所有日志
    loguru_logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        level="DEBUG",
        format=format_record,
        rotation="00:00",  # 每天轮转
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩旧日志
        encoding="utf-8",
        enqueue=True,
        backtrace=True,
        diagnose=settings.is_development,
    )
    
    # 文件输出 - 错误日志
    loguru_logger.add(
        log_dir / "error_{time:YYYY-MM-DD}.log",
        level="ERROR",
        format=format_record,
        rotation="00:00",
        retention="90 days",  # 错误日志保留90天
        compression="zip",
        encoding="utf-8",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )
    
    # 拦截标准库的logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # 拦截uvicorn日志
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"]:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.setLevel(settings.LOG_LEVEL)
    
    loguru_logger.info(f"Logging initialized. Level: {settings.LOG_LEVEL}, Environment: {settings.ENV}")


def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    脱敏敏感数据
    
    Args:
        data: 原始数据
        
    Returns:
        脱敏后的数据
    """
    sensitive_keys = {
        "password", "passwd", "pwd", 
        "secret", "token", "api_key", "api_secret",
        "smtp_password", "encryption_key", "jwt_secret",
    }
    
    masked_data = data.copy()
    for key, value in masked_data.items():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            if isinstance(value, str) and len(value) > 4:
                masked_data[key] = value[:2] + "*" * (len(value) - 4) + value[-2:]
            else:
                masked_data[key] = "***"
        elif isinstance(value, dict):
            masked_data[key] = mask_sensitive_data(value)
    
    return masked_data


# 初始化日志
init_logging()

# 导出logger
logger = loguru_logger

__all__ = ["logger", "mask_sensitive_data"]

