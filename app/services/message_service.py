"""
消息服务
处理消息的创建、查询、状态更新等
"""
import hashlib
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.message import MessageRecord, MessageStatus, MessageChannel
from app.core.logger import logger
from app.core.security import generate_request_id
from app.utils.redis_client import RedisClient


class MessageService:
    """消息服务"""
    
    def __init__(self, db: Session, redis_client: Optional[RedisClient] = None):
        self.db = db
        self.redis = redis_client
    
    def create_message(
        self,
        channel: MessageChannel,
        to: str,
        content: str,
        subject: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        content_type: str = "html",
        template_id: Optional[int] = None,
        template_version: Optional[int] = None,
        template_variables: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
        request_id: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> MessageRecord:
        """
        创建消息记录
        
        Args:
            channel: 发送渠道
            to: 接收者
            content: 内容
            subject: 主题
            cc: 抄送
            bcc: 密送
            content_type: 内容类型
            template_id: 模板ID
            template_version: 模板版本
            template_variables: 模板变量
            idempotency_key: 幂等性键
            request_id: 请求ID
            extra_data: 元数据
            
        Returns:
            MessageRecord: 消息记录
        """
        message = MessageRecord(
            channel=channel,
            status=MessageStatus.PENDING,
            to=to,
            cc=cc,
            bcc=bcc,
            subject=subject,
            content=content,
            content_type=content_type,
            template_id=template_id,
            template_version=template_version,
            template_variables=template_variables,
            idempotency_key=idempotency_key,
            request_id=request_id or generate_request_id(),
            extra_data=extra_data
        )
        
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        logger.info(f"Created message record: id={message.id}, channel={channel}, to={to}")
        return message
    
    def update_message_status(
        self,
        message: MessageRecord,
        status: MessageStatus,
        sender: Optional[str] = None,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> MessageRecord:
        """
        更新消息状态
        
        Args:
            message: 消息记录
            status: 新状态
            sender: 发送者
            error_code: 错误码
            error_message: 错误信息
            
        Returns:
            MessageRecord: 更新后的消息记录
        """
        message.status = status
        
        if sender:
            message.sender = sender
        
        if status == MessageStatus.SUCCESS:
            message.sent_at = datetime.utcnow().isoformat()
        
        if error_code:
            message.error_code = error_code
        
        if error_message:
            message.error_message = error_message
        
        self.db.commit()
        
        logger.info(f"Updated message {message.id} status to {status}")
        return message
    
    def add_retry_log(
        self,
        message: MessageRecord,
        error: str,
        retry_at: Optional[datetime] = None
    ) -> MessageRecord:
        """
        添加重试日志
        
        Args:
            message: 消息记录
            error: 错误信息
            retry_at: 重试时间
            
        Returns:
            MessageRecord: 更新后的消息记录
        """
        message.retry_count += 1
        
        # 初始化重试日志
        if message.retry_logs is None:
            message.retry_logs = []
        
        # 添加重试记录
        retry_log = {
            "attempt": message.retry_count,
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
            "retry_at": retry_at.isoformat() if retry_at else None
        }
        message.retry_logs.append(retry_log)
        
        self.db.commit()
        
        logger.info(f"Added retry log for message {message.id}, attempt {message.retry_count}")
        return message
    
    def check_duplicate(
        self,
        idempotency_key: Optional[str] = None,
        channel: Optional[MessageChannel] = None,
        to: Optional[str] = None,
        content: Optional[str] = None,
        ttl: int = 3600
    ) -> Optional[MessageRecord]:
        """
        检查消息是否重复
        
        Args:
            idempotency_key: 幂等性键（优先使用）
            channel: 渠道
            to: 接收者
            content: 内容
            ttl: 去重TTL（秒）
            
        Returns:
            Optional[MessageRecord]: 如果存在重复消息，返回该消息，否则返回None
        """
        # 方式1：使用幂等性键（如果提供）
        if idempotency_key:
            existing = (
                self.db.query(MessageRecord)
                .filter(MessageRecord.idempotency_key == idempotency_key)
                .first()
            )
            
            if existing:
                logger.warning(f"Duplicate message detected by idempotency_key: {idempotency_key}")
                return existing
        
        # 方式2：使用内容指纹（Redis）
        if self.redis and channel and to and content:
            fingerprint = self._generate_content_fingerprint(channel, to, content)
            
            # 检查Redis中是否存在
            if self.redis.exists(f"msg:fingerprint:{fingerprint}"):
                logger.warning(f"Duplicate message detected by content fingerprint: {fingerprint}")
                
                # 尝试从数据库获取原始消息
                message_id = self.redis.get(f"msg:fingerprint:{fingerprint}")
                if message_id:
                    existing = self.db.query(MessageRecord).get(int(message_id))
                    return existing
            else:
                # 记录指纹到Redis
                self.redis.setex(f"msg:fingerprint:{fingerprint}", ttl, "1")
        
        return None
    
    def _generate_content_fingerprint(
        self,
        channel: MessageChannel,
        to: str,
        content: str
    ) -> str:
        """
        生成内容指纹（SHA256）
        
        Args:
            channel: 渠道
            to: 接收者
            content: 内容
            
        Returns:
            str: 指纹字符串
        """
        data = f"{channel.value}:{to}:{content}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_message(self, message_id: int) -> Optional[MessageRecord]:
        """
        根据ID获取消息
        
        Args:
            message_id: 消息ID
            
        Returns:
            Optional[MessageRecord]: 消息记录
        """
        return self.db.query(MessageRecord).get(message_id)
    
    def list_messages(
        self,
        channel: Optional[MessageChannel] = None,
        status: Optional[MessageStatus] = None,
        to: Optional[str] = None,
        request_id: Optional[str] = None,
        api_key_id: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[MessageRecord], int]:
        """
        查询消息列表
        
        Args:
            channel: 渠道
            status: 状态
            to: 接收者
            request_id: 请求ID
            api_key_id: API Key ID（用于权限过滤，None表示不过滤）
            start_time: 开始时间
            end_time: 结束时间
            page: 页码
            page_size: 每页数量
            
        Returns:
            tuple: (消息列表, 总数)
        """
        query = self.db.query(MessageRecord)
        
        if channel:
            query = query.filter(MessageRecord.channel == channel)
        if status:
            query = query.filter(MessageRecord.status == status)
        if to:
            query = query.filter(MessageRecord.to.like(f"%{to}%"))
        if request_id:
            query = query.filter(MessageRecord.request_id == request_id)
        if api_key_id is not None:
            query = query.filter(MessageRecord.api_key_id == api_key_id)
        if start_time:
            query = query.filter(MessageRecord.created_at >= start_time)
        if end_time:
            query = query.filter(MessageRecord.created_at <= end_time)
        
        total = query.count()
        
        messages = (
            query.order_by(desc(MessageRecord.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        
        return messages, total


__all__ = ["MessageService"]

