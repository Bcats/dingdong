"""
邮件发送服务
管理邮箱池，实现邮件发送逻辑
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.email import EmailAccount
from app.core.logger import logger
from app.core.security import decrypt_data
from app.core.config import settings


class EmailPoolManager:
    """邮箱池管理器"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_available_account(self) -> Optional[EmailAccount]:
        """
        获取可用的邮箱账户
        按照优先级和可用性选择
        
        Returns:
            Optional[EmailAccount]: 可用的邮箱账户，如果没有返回None
        """
        # 查询可用的邮箱账户
        accounts = (
            self.db.query(EmailAccount)
            .filter(
                EmailAccount.is_active == True,
                EmailAccount.daily_sent_count < EmailAccount.daily_limit,
                EmailAccount.failure_count < 5
            )
            .order_by(EmailAccount.priority.desc(), EmailAccount.daily_sent_count.asc())
            .all()
        )
        
        if not accounts:
            logger.warning("No available email accounts")
            return None
        
        return accounts[0]
    
    def reset_daily_counts(self) -> int:
        """
        重置所有邮箱的每日计数
        通常由定时任务在每天0点调用
        
        Returns:
            int: 重置的邮箱数量
        """
        count = (
            self.db.query(EmailAccount)
            .filter(EmailAccount.is_active == True)
            .update({
                "daily_sent_count": 0,
                "last_reset_at": datetime.utcnow()
            })
        )
        self.db.commit()
        logger.info(f"Reset daily counts for {count} email accounts")
        return count
    
    def record_success(self, account: EmailAccount) -> None:
        """
        记录发送成功
        
        Args:
            account: 邮箱账户
        """
        account.increment_sent_count()
        account.reset_failure_count()
        self.db.commit()
        logger.debug(f"Email sent successfully from {account.email}, count: {account.daily_sent_count}/{account.daily_limit}")
    
    def record_failure(self, account: EmailAccount, error: str) -> None:
        """
        记录发送失败
        
        Args:
            account: 邮箱账户
            error: 错误信息
        """
        account.record_failure()
        self.db.commit()
        logger.warning(f"Email send failed from {account.email}, failure count: {account.failure_count}, error: {error}")


class EmailSender:
    """邮件发送器"""
    
    def __init__(self, account: EmailAccount):
        self.account = account
        self._password = None
    
    @property
    def smtp_password(self) -> str:
        """解密SMTP密码"""
        if self._password is None:
            try:
                self._password = decrypt_data(self.account.smtp_password)
            except Exception as e:
                logger.error(f"Failed to decrypt SMTP password for {self.account.email}: {str(e)}")
                raise ValueError("Invalid SMTP password encryption")
        return self._password
    
    async def send(
        self,
        to: List[str],
        subject: str,
        content: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        content_type: str = "html",
        attachments: Optional[List[dict]] = None
    ) -> bool:
        """
        发送邮件
        
        Args:
            to: 收件人列表
            subject: 主题
            content: 内容
            cc: 抄送列表
            bcc: 密送列表
            content_type: 内容类型 (html/plain)
            attachments: 附件列表 [{"filename": "xx", "content": bytes}]
            
        Returns:
            bool: 是否发送成功
        """
        try:
            # 创建邮件对象
            if attachments:
                message = MIMEMultipart()
            else:
                message = MIMEText(content, content_type, "utf-8")
            
            # 设置邮件头
            # QQ邮箱对From字段格式要求严格，简化为只使用邮箱地址
            message["From"] = self.account.email
            message["To"] = ", ".join(to)
            message["Subject"] = subject
            
            if cc:
                message["Cc"] = ", ".join(cc)
            if bcc:
                message["Bcc"] = ", ".join(bcc)
            
            # 如果有附件，需要添加正文部分
            if attachments:
                text_part = MIMEText(content, content_type, "utf-8")
                message.attach(text_part)
                
                # 添加附件
                for attachment in attachments:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment["content"])
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{attachment["filename"]}"'
                    )
                    message.attach(part)
            
            # 准备收件人列表（包含to, cc, bcc）
            recipients = to.copy()
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            # 发送邮件
            async with aiosmtplib.SMTP(
                hostname=self.account.smtp_host,
                port=self.account.smtp_port,
                use_tls=self.account.use_tls,
                start_tls=False,  # 465端口使用implicit SSL，不需要STARTTLS
                timeout=settings.EMAIL_TIMEOUT
            ) as smtp:
                await smtp.login(self.account.smtp_username, self.smtp_password)
                # 使用sendmail方法，显式指定发件人和收件人列表
                await smtp.sendmail(
                    self.account.email,
                    recipients,
                    message.as_string()
                )
            
            logger.info(f"Email sent successfully to {to} from {self.account.email}")
            return True
            
        except aiosmtplib.SMTPException as e:
            logger.error(f"SMTP error when sending email from {self.account.email}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error when sending email from {self.account.email}: {str(e)}")
            raise


async def send_email(
    db: Session,
    to: List[str],
    subject: str,
    content: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    content_type: str = "html",
    attachments: Optional[List[dict]] = None
) -> tuple[bool, Optional[str], Optional[str]]:
    """
    发送邮件（高级接口）
    自动选择可用邮箱账户
    
    Args:
        db: 数据库会话
        to: 收件人列表
        subject: 主题
        content: 内容
        cc: 抄送列表
        bcc: 密送列表
        content_type: 内容类型
        attachments: 附件列表
        
    Returns:
        tuple: (是否成功, 发送者邮箱, 错误信息)
    """
    pool_manager = EmailPoolManager(db)
    account = pool_manager.get_available_account()
    
    if not account:
        error_msg = "No available email account"
        logger.error(error_msg)
        return False, None, error_msg
    
    sender = EmailSender(account)
    
    try:
        success = await sender.send(
            to=to,
            subject=subject,
            content=content,
            cc=cc,
            bcc=bcc,
            content_type=content_type,
            attachments=attachments
        )
        
        if success:
            pool_manager.record_success(account)
            return True, account.email, None
        else:
            error_msg = "Send failed with unknown reason"
            pool_manager.record_failure(account, error_msg)
            return False, account.email, error_msg
            
    except Exception as e:
        error_msg = str(e)
        pool_manager.record_failure(account, error_msg)
        return False, account.email, error_msg


__all__ = ["EmailPoolManager", "EmailSender", "send_email"]

