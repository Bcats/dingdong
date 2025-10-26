"""
定时任务
"""
from datetime import datetime, timedelta

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.core.logger import logger
from app.services.email_service import EmailPoolManager
from app.models.email import EmailAttachment


@celery_app.task(name="app.tasks.scheduled_tasks.reset_email_daily_counts")
def reset_email_daily_counts():
    """
    重置邮箱每日发送计数
    每天凌晨0点执行
    """
    db = SessionLocal()
    
    try:
        pool_manager = EmailPoolManager(db)
        count = pool_manager.reset_daily_counts()
        logger.info(f"Reset daily counts for {count} email accounts")
        return {"status": "success", "count": count}
    except Exception as e:
        logger.error(f"Error resetting email daily counts: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@celery_app.task(name="app.tasks.scheduled_tasks.cleanup_expired_attachments")
def cleanup_expired_attachments():
    """
    清理过期附件
    每小时执行一次
    """
    db = SessionLocal()
    
    try:
        # 查询过期的附件
        expired_attachments = (
            db.query(EmailAttachment)
            .filter(
                EmailAttachment.expires_at != None,
                EmailAttachment.expires_at < datetime.utcnow()
            )
            .all()
        )
        
        count = 0
        for attachment in expired_attachments:
            try:
                # 删除物理文件
                import os
                if os.path.exists(attachment.file_path):
                    os.remove(attachment.file_path)
                
                # 删除数据库记录
                db.delete(attachment)
                count += 1
            except Exception as e:
                logger.error(f"Error deleting attachment {attachment.id}: {str(e)}")
        
        db.commit()
        logger.info(f"Cleaned up {count} expired attachments")
        return {"status": "success", "count": count}
        
    except Exception as e:
        logger.error(f"Error cleaning up expired attachments: {str(e)}")
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


__all__ = ["reset_email_daily_counts", "cleanup_expired_attachments"]

