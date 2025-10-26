"""
邮件发送任务
"""
import asyncio
from typing import List
from celery import Task

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.core.logger import logger
from app.models.message import MessageRecord, MessageStatus
from app.services.email_service import send_email
from app.services.message_service import MessageService
from datetime import datetime, timedelta


class EmailTask(Task):
    """邮件任务基类"""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """任务失败回调"""
        logger.error(f"Task {task_id} failed: {exc}")


@celery_app.task(
    bind=True,
    base=EmailTask,
    max_retries=3,
    default_retry_delay=60,  # 1分钟后重试
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,  # 最大10分钟
    retry_jitter=True
)
def send_email_task(self, message_id: int):
    """
    发送邮件任务
    
    Args:
        message_id: 消息ID
    """
    db = SessionLocal()
    
    try:
        # 获取消息记录
        message = db.query(MessageRecord).get(message_id)
        if not message:
            logger.error(f"Message {message_id} not found")
            return
        
        # 更新状态为发送中
        message_service = MessageService(db)
        message_service.update_message_status(message, MessageStatus.SENDING)
        
        # 解析收件人
        to_list = [email.strip() for email in message.to.split(",")]
        cc_list = [email.strip() for email in message.cc.split(",")] if message.cc else None
        bcc_list = [email.strip() for email in message.bcc.split(",")] if message.bcc else None
        
        # 发送邮件（使用asyncio运行异步函数）
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        success, sender, error = loop.run_until_complete(
            send_email(
                db=db,
                to=to_list,
                subject=message.subject or "No Subject",
                content=message.content,
                cc=cc_list,
                bcc=bcc_list,
                content_type=message.content_type
            )
        )
        
        loop.close()
        
        if success:
            # 发送成功
            message_service.update_message_status(
                message,
                MessageStatus.SUCCESS,
                sender=sender
            )
            logger.info(f"Email sent successfully: message_id={message_id}")
        else:
            # 发送失败，记录重试日志
            retry_count = self.request.retries
            max_retries = self.max_retries
            
            if retry_count < max_retries:
                # 记录重试
                retry_at = datetime.utcnow() + timedelta(seconds=60 * (2 ** retry_count))
                message_service.add_retry_log(message, error, retry_at)
                message_service.update_message_status(
                    message,
                    MessageStatus.RETRYING,
                    error_message=error
                )
                
                # 抛出异常以触发重试
                raise Exception(error)
            else:
                # 达到最大重试次数，标记为失败
                message_service.update_message_status(
                    message,
                    MessageStatus.FAILED,
                    sender=sender,
                    error_code="MAX_RETRIES_EXCEEDED",
                    error_message=error
                )
                logger.error(f"Email send failed after {max_retries} retries: message_id={message_id}")
        
    except Exception as e:
        logger.error(f"Error in send_email_task: {str(e)}")
        
        # 如果还有重试机会，抛出异常
        if self.request.retries < self.max_retries:
            raise
        else:
            # 最后一次失败，更新状态
            try:
                message = db.query(MessageRecord).get(message_id)
                if message:
                    message_service = MessageService(db)
                    message_service.update_message_status(
                        message,
                        MessageStatus.FAILED,
                        error_code="TASK_ERROR",
                        error_message=str(e)
                    )
            except Exception as update_error:
                logger.error(f"Failed to update message status: {update_error}")
    
    finally:
        db.close()


__all__ = ["send_email_task"]

