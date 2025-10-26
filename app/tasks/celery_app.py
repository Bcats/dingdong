"""
Celery应用配置
"""
from celery import Celery
from celery.schedules import crontab

from app.core.config import settings
from app.core.logger import logger


# 创建Celery应用
celery_app = Celery(
    "notification-platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.email_tasks",
        "app.tasks.scheduled_tasks",
    ]
)

# 配置Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.TZ,
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_expires=3600,  # 结果保留1小时
)

# 定时任务配置
celery_app.conf.beat_schedule = {
    # 每天凌晨0点重置邮箱发送计数
    "reset-email-daily-counts": {
        "task": "app.tasks.scheduled_tasks.reset_email_daily_counts",
        "schedule": crontab(hour=0, minute=0),
    },
    # 每小时清理过期附件
    "cleanup-expired-attachments": {
        "task": "app.tasks.scheduled_tasks.cleanup_expired_attachments",
        "schedule": crontab(minute=0),
    },
}

logger.info("Celery application configured")


__all__ = ["celery_app"]

