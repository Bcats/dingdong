"""
消息API
"""
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_api_key, get_current_user, get_request_id
from app.models.api_key import APIKey
from app.models.admin_user import AdminUser
from app.models.message import MessageChannel, MessageStatus
from app.schemas import (
    EmailSendRequest,
    EmailSendResponse,
    MessageQuery,
    MessageResponse,
    BatchQueryRequest,
    ResponseModel,
    PagedResponse,
    PaginationModel,
)
from app.services.message_service import MessageService
from app.services.template_service import TemplateService
from app.tasks.email_tasks import send_email_task
from app.core.logger import logger
from app.utils.redis_client import redis_client


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/email/send", response_model=ResponseModel[EmailSendResponse])
async def send_email(
    request: EmailSendRequest,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_current_api_key),
    request_id: str = Depends(get_request_id)
):
    """
    发送邮件
    
    支持两种模式：
    1. 直接指定内容：提供 subject + content
    2. 使用模板：提供 template_code + template_variables
    """
    message_service = MessageService(db, redis_client)
    
    # 模式判断
    if request.template_code:
        # 模板模式
        template_service = TemplateService(db)
        success, subject, content, error, version = template_service.render_message_template(
            request.template_code,
            request.template_variables or {}
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )
        
        template_id = template_service.get_template(request.template_code).id if template_service.get_template(request.template_code) else None
        template_version = version
    else:
        # 直接内容模式
        if not request.content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either template_code or content must be provided"
            )
        subject = request.subject
        content = request.content
        template_id = None
        template_version = None
    
    # 去重检查
    if request.idempotency_key or content:
        duplicate = message_service.check_duplicate(
            idempotency_key=request.idempotency_key,
            channel=MessageChannel.EMAIL,
            to=",".join(request.to),
            content=content
        )
        
        if duplicate:
            logger.warning(f"Duplicate message detected: {duplicate.id}")
            return ResponseModel(
                code=0,
                message="Duplicate message, returning existing record",
                data=EmailSendResponse(
                    message_id=duplicate.id,
                    status=duplicate.status.value,
                    request_id=duplicate.request_id
                ),
                request_id=request_id
            )
    
    # 创建消息记录
    message = message_service.create_message(
        channel=MessageChannel.EMAIL,
        to=",".join(request.to),
        cc=",".join(request.cc) if request.cc else None,
        bcc=",".join(request.bcc) if request.bcc else None,
        subject=subject,
        content=content,
        content_type="html",
        template_id=template_id,
        template_version=template_version,
        template_variables=request.template_variables,
        idempotency_key=request.idempotency_key,
        request_id=request_id,
        extra_data=request.extra_data
    )
    
    # 异步发送（通过Celery）
    send_email_task.delay(message.id)
    
    logger.info(f"Email message created: {message.id}")
    
    return ResponseModel(
        code=0,
        message="Message queued for sending",
        data=EmailSendResponse(
            message_id=message.id,
            status=message.status.value,
            request_id=message.request_id
        ),
        request_id=request_id
    )


@router.get("", response_model=ResponseModel[PagedResponse[MessageResponse]])
async def list_messages(
    channel: str = None,
    status: str = None,
    to: str = None,
    request_id: str = None,
    start_time: str = None,
    end_time: str = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """查询消息列表（支持管理员和API Key）"""
    message_service = MessageService(db)
    
    # 转换枚举
    channel_enum = MessageChannel(channel) if channel else None
    status_enum = MessageStatus(status) if status else None
    
    # 如果是API Key用户，只返回该API Key的消息；管理员可以看所有消息
    api_key_id = None if isinstance(current_user, AdminUser) else current_user.id
    
    # 限制导出数量
    if page_size > 10000:
        page_size = 10000
        logger.warning(f"Page size limited to 10000")
    
    messages, total = message_service.list_messages(
        channel=channel_enum,
        status=status_enum,
        to=to,
        request_id=request_id,
        api_key_id=api_key_id,
        start_time=start_time,
        end_time=end_time,
        page=page,
        page_size=page_size
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return ResponseModel(
        code=0,
        message="Success",
        data=PagedResponse(
            items=[MessageResponse.model_validate(msg) for msg in messages],
            pagination=PaginationModel(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages
            )
        )
    )


@router.get("/{message_id}", response_model=ResponseModel[MessageResponse])
async def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """获取消息详情（支持管理员和API Key）"""
    message_service = MessageService(db)
    message = message_service.get_message(message_id)
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # 如果是API Key用户，检查权限
    if isinstance(current_user, APIKey) and message.api_key_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this message"
        )
    
    return ResponseModel(
        code=0,
        message="Success",
        data=MessageResponse.model_validate(message)
    )


@router.post("/batch/query", response_model=ResponseModel[list[MessageResponse]])
async def batch_query_messages(
    request: BatchQueryRequest,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_current_api_key)
):
    """批量查询消息状态"""
    message_service = MessageService(db)
    
    messages = []
    for message_id in request.message_ids:
        message = message_service.get_message(message_id)
        if message:
            messages.append(MessageResponse.model_validate(message))
    
    return ResponseModel(
        code=0,
        message="Success",
        data=messages
    )


@router.post("/{message_id}/retry", response_model=ResponseModel[None])
async def retry_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """重试失败的消息（仅管理员）"""
    # 只有管理员可以重试
    if not isinstance(current_user, AdminUser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅管理员可以重试消息"
        )
    
    message_service = MessageService(db)
    message = message_service.get_message(message_id)
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )
    
    # 检查消息状态，只有失败的消息可以重试
    if message.status not in [MessageStatus.FAILED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"只能重试失败的消息，当前状态：{message.status.value}"
        )
    
    # 检查重试次数（如果已达上限，重置计数器）
    if message.retry_count >= message.max_retry:
        logger.warning(f"消息 {message_id} 已达最大重试次数，重置计数器")
        message.retry_count = 0  # 重置重试次数
    
    # 重置消息状态为待发送
    message.status = MessageStatus.PENDING
    message.error_code = None
    message.error_message = None
    db.commit()
    
    # 重新加入发送队列
    send_email_task.delay(message.id)
    
    logger.info(f"消息 {message_id} 由管理员 {current_user.username} 请求重试")
    
    return ResponseModel(
        code=0,
        message="消息已加入重试队列",
        data=None
    )


@router.delete("/{message_id}", response_model=ResponseModel[None])
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """删除消息（仅管理员）"""
    # 只有管理员可以删除
    if not isinstance(current_user, AdminUser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅管理员可以删除消息"
        )
    
    message_service = MessageService(db)
    message = message_service.get_message(message_id)
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )
    
    # 删除消息（硬删除）
    db.delete(message)
    db.commit()
    
    logger.info(f"消息 {message_id} 由管理员 {current_user.username} 删除")
    
    return ResponseModel(
        code=0,
        message="消息删除成功",
        data=None
    )


__all__ = ["router"]

