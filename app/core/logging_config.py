"""
日志配置增强
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from loguru import logger as loguru_logger
from app.core.config import settings


class LogConfig:
    """日志配置类"""
    
    @staticmethod
    def setup_logging():
        """配置日志系统"""
        
        # 移除默认处理器
        loguru_logger.remove()
        
        # 1. 控制台输出（带颜色）
        loguru_logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=settings.LOG_LEVEL,
            colorize=True
        )
        
        # 2. 应用日志文件（按天轮转）
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        loguru_logger.add(
            log_dir / "app_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            level="INFO",
            rotation="00:00",  # 每天轮转
            retention="30 days",  # 保留30天
            compression="zip",  # 压缩旧日志
            encoding="utf-8"
        )
        
        # 3. 错误日志文件（单独记录）
        loguru_logger.add(
            log_dir / "error_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
            level="ERROR",
            rotation="00:00",
            retention="60 days",  # 错误日志保留更久
            compression="zip",
            encoding="utf-8",
            backtrace=True,
            diagnose=True
        )
        
        # 4. 业务日志文件（关键业务操作）
        loguru_logger.add(
            log_dir / "business_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {extra[event_type]} | {message}",
            level="INFO",
            rotation="00:00",
            retention="90 days",
            filter=lambda record: "event_type" in record["extra"],
            encoding="utf-8"
        )
        
        # 5. 访问日志（API请求）
        loguru_logger.add(
            log_dir / "access_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {extra[method]} {extra[path]} | Status: {extra[status_code]} | Duration: {extra[duration]}ms",
            level="INFO",
            rotation="00:00",
            retention="30 days",
            filter=lambda record: "method" in record["extra"],
            encoding="utf-8"
        )
        
        loguru_logger.info(f"Logging initialized. Level: {settings.LOG_LEVEL}, Environment: {settings.ENVIRONMENT}")
        
        return loguru_logger


# 业务日志记录器
class BusinessLogger:
    """业务日志记录"""
    
    @staticmethod
    def log_email_sent(message_id: int, to: str, status: str):
        """记录邮件发送"""
        loguru_logger.bind(event_type="EMAIL_SENT").info(
            f"message_id={message_id} | to={to} | status={status}"
        )
    
    @staticmethod
    def log_email_failed(message_id: int, to: str, error: str):
        """记录邮件失败"""
        loguru_logger.bind(event_type="EMAIL_FAILED").error(
            f"message_id={message_id} | to={to} | error={error}"
        )
    
    @staticmethod
    def log_api_key_created(api_key: str, name: str):
        """记录API密钥创建"""
        loguru_logger.bind(event_type="API_KEY_CREATED").info(
            f"api_key={api_key[:20]}... | name={name}"
        )
    
    @staticmethod
    def log_template_created(template_id: int, code: str):
        """记录模板创建"""
        loguru_logger.bind(event_type="TEMPLATE_CREATED").info(
            f"template_id={template_id} | code={code}"
        )


# 初始化日志配置
logger = LogConfig.setup_logging()
business_logger = BusinessLogger()


__all__ = ["logger", "business_logger", "LogConfig"]

