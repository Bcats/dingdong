"""
监控相关API端点
"""
from datetime import datetime, timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, Integer

from app.core.database import get_db
from app.models.message import MessageRecord, MessageStatus, MessageChannel
from app.models.email import EmailAccount
from app.utils.redis_client import redis_client
from app.schemas.common import ResponseModel

router = APIRouter(prefix="/monitoring", tags=["监控"])


@router.get("/metrics", response_model=ResponseModel[Dict[str, Any]], summary="获取系统指标")
async def get_system_metrics(
    hours: int = 24,
    date: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """
    获取系统关键指标
    
    Args:
        hours: 统计时间范围（小时）
        date: 指定单个日期（YYYY-MM-DD格式）
        start_date: 开始日期（YYYY-MM-DD格式）
        end_date: 结束日期（YYYY-MM-DD格式）
        
    Returns:
        系统指标数据
    """
    now = datetime.now()
    
    # 优先使用日期范围
    if start_date and end_date:
        try:
            since = datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
            until = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            since = now - timedelta(hours=hours)
            until = now
    # 其次使用单个日期
    elif date:
        try:
            query_date = datetime.strptime(date, "%Y-%m-%d")
            since = query_date.replace(hour=0, minute=0, second=0, microsecond=0)
            until = query_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            since = now - timedelta(hours=hours)
            until = now
    # 默认使用小时数
    else:
        since = now - timedelta(hours=hours)
        until = now
    
    # 1. 消息发送统计
    # 总消息数
    time_filter = and_(MessageRecord.created_at >= since, MessageRecord.created_at <= until)
    
    total_result = db.execute(
        select(func.count(MessageRecord.id))
        .where(time_filter)
    )
    total_messages = total_result.scalar() or 0
    
    # 按状态统计
    status_result = db.execute(
        select(
            MessageRecord.status,
            func.count(MessageRecord.id).label('count')
        )
        .where(time_filter)
        .group_by(MessageRecord.status)
    )
    status_stats = {row.status.value: row.count for row in status_result}
    
    # 成功率
    success_count = status_stats.get('success', 0)
    failed_count = status_stats.get('failed', 0)
    success_rate = (success_count / total_messages * 100) if total_messages > 0 else 0
    
    # 按渠道统计
    channel_result = db.execute(
        select(
            MessageRecord.channel,
            func.count(MessageRecord.id).label('count')
        )
        .where(time_filter)
        .group_by(MessageRecord.channel)
    )
    channel_stats = {row.channel.value: row.count for row in channel_result}
    
    # 2. 邮箱账户状态
    email_accounts_result = db.execute(
        select(
            func.count(EmailAccount.id).label('total'),
            func.sum(func.cast(EmailAccount.is_active, Integer)).label('active'),
            func.sum(EmailAccount.daily_sent_count).label('daily_sent'),
            func.sum(EmailAccount.daily_limit).label('daily_limit')
        )
    )
    email_stats = email_accounts_result.first()
    
    # 3. 队列信息（从Redis获取）
    try:
        # 尝试获取队列长度（这需要Celery Inspect API）
        queue_length = 0  # 默认值，实际需要通过Celery API获取
    except Exception:
        queue_length = 0
    
    # 4. 失败原因统计（top 5）
    error_result = db.execute(
        select(
            MessageRecord.error_message,
            func.count(MessageRecord.id).label('count')
        )
        .where(
            and_(
                time_filter,
                MessageRecord.error_message.isnot(None),
                MessageRecord.error_message != ''
            )
        )
        .group_by(MessageRecord.error_message)
        .order_by(func.count(MessageRecord.id).desc())
        .limit(5)
    )
    error_stats = [
        {"error": row.error_message[:100], "count": row.count}
        for row in error_result
    ]
    
    # 获取每小时统计（用于图表）
    hourly_result = db.execute(
        select(
            func.date_trunc('hour', MessageRecord.created_at).label('hour'),
            func.count(MessageRecord.id).label('total'),
            func.sum(
                func.cast(MessageRecord.status == MessageStatus.SUCCESS, Integer)
            ).label('success'),
            func.sum(
                func.cast(MessageRecord.status == MessageStatus.FAILED, Integer)
            ).label('failed')
        )
        .where(time_filter)
        .group_by('hour')
        .order_by('hour')
    )
    
    hourly_stats = []
    for row in hourly_result:
        hourly_stats.append({
            "hour": row.hour.strftime("%Y-%m-%d %H:00"),
            "total": row.total,
            "success": row.success or 0,
            "failed": row.failed or 0
        })
    
    # 返回前端期望的数据结构（用ResponseModel包装）
    return ResponseModel(
        code=0,
        message="success",
        data={
            "total_messages": total_messages,
            "success_messages": success_count,
            "failed_messages": failed_count,
            "success_rate": success_rate / 100,  # 前端期望0-1之间的小数
            "pending_messages": status_stats.get('pending', 0),
            "hourly_stats": hourly_stats,
            # 保留详细信息供将来使用
            "_detailed": {
                "time_range_hours": hours,
                "generated_at": now.isoformat(),
                "by_status": status_stats,
                "by_channel": channel_stats,
                "email_accounts": {
                    "total": email_stats.total or 0,
                    "active": email_stats.active or 0,
                    "daily_sent": email_stats.daily_sent or 0,
                    "daily_limit": email_stats.daily_limit or 0,
                    "usage_rate": round((email_stats.daily_sent / email_stats.daily_limit * 100) if email_stats.daily_limit else 0, 2)
                },
                "queue": {
                    "pending_tasks": queue_length
                },
                "top_errors": error_stats
            }
        }
    )


@router.get("/health/detailed", summary="详细健康检查")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    详细的系统健康检查
    
    Returns:
        各组件的健康状态
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {}
    }
    
    # 1. 数据库检查
    try:
        db.execute(select(1))
        health_status["components"]["database"] = {
            "status": "healthy",
            "message": "Database connection OK"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["components"]["database"] = {
            "status": "unhealthy",
            "message": f"Database error: {str(e)}"
        }
    
    # 2. Redis检查
    try:
        redis_client.ping()
        health_status["components"]["redis"] = {
            "status": "healthy",
            "message": "Redis connection OK"
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["components"]["redis"] = {
            "status": "unhealthy",
            "message": f"Redis error: {str(e)}"
        }
    
    # 3. 邮箱账户检查
    try:
        result = db.execute(
            select(func.count(EmailAccount.id))
            .where(EmailAccount.is_active == True)
        )
        active_accounts = result.scalar() or 0
        
        if active_accounts > 0:
            health_status["components"]["email_accounts"] = {
                "status": "healthy",
                "message": f"{active_accounts} active email account(s)"
            }
        else:
            health_status["status"] = "degraded"
            health_status["components"]["email_accounts"] = {
                "status": "warning",
                "message": "No active email accounts"
            }
    except Exception as e:
        health_status["components"]["email_accounts"] = {
            "status": "unknown",
            "message": f"Check failed: {str(e)}"
        }
    
    return health_status


@router.get("/stats/hourly", summary="每小时统计")
async def get_hourly_stats(
    hours: int = 24,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取每小时的消息发送统计
    
    Args:
        hours: 统计时间范围（小时）
        
    Returns:
        每小时统计数据
    """
    now = datetime.now()
    since = now - timedelta(hours=hours)
    
    # 按小时分组统计
    result = db.execute(
        select(
            func.date_trunc('hour', MessageRecord.created_at).label('hour'),
            func.count(MessageRecord.id).label('total'),
            func.sum(
                func.cast(MessageRecord.status == MessageStatus.SUCCESS, Integer)
            ).label('success'),
            func.sum(
                func.cast(MessageRecord.status == MessageStatus.FAILED, Integer)
            ).label('failed')
        )
        .where(MessageRecord.created_at >= since)
        .group_by('hour')
        .order_by('hour')
    )
    
    hourly_data = []
    for row in result:
        hourly_data.append({
            "hour": row.hour.isoformat(),
            "total": row.total,
            "success": row.success or 0,
            "failed": row.failed or 0,
            "success_rate": round((row.success / row.total * 100) if row.total > 0 else 0, 2)
        })
    
    return {
        "time_range_hours": hours,
        "data_points": len(hourly_data),
        "data": hourly_data
    }


