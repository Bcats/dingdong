"""
邮箱账户管理API
"""
import time
from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import aiosmtplib
from email.mime.text import MIMEText

from app.core.database import get_db
from app.api.dependencies import get_current_api_key, get_current_user
from app.models.api_key import APIKey
from app.models.admin_user import AdminUser
from app.models.email import EmailAccount
from app.schemas.common import ResponseModel
from app.schemas.email_account import (
    EmailAccountCreate,
    EmailAccountUpdate,
    EmailAccountResponse,
    EmailAccountTestRequest,
    EmailAccountTestResponse,
)
from app.core.logger import logger
from app.core.security import encrypt_password, decrypt_password


router = APIRouter(prefix="/email-accounts", tags=["Email Accounts"])


@router.get("", response_model=ResponseModel[List[EmailAccountResponse]])
async def list_email_accounts(
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """
    获取邮箱账户列表
    
    - is_active: 筛选是否启用
    """
    query = db.query(EmailAccount)
    
    if is_active is not None:
        query = query.filter(EmailAccount.is_active == is_active)
    
    accounts = query.order_by(EmailAccount.priority.desc(), EmailAccount.id).all()
    
    return ResponseModel(
        code=0,
        message="Success",
        data=[EmailAccountResponse.model_validate(acc) for acc in accounts]
    )


@router.get("/{account_id}", response_model=ResponseModel[EmailAccountResponse])
async def get_email_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """获取邮箱账户详情"""
    account = db.query(EmailAccount).filter(
        EmailAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email account not found"
        )
    
    return ResponseModel(
        code=0,
        message="Success",
        data=EmailAccountResponse.model_validate(account)
    )


@router.post("", response_model=ResponseModel[EmailAccountResponse], status_code=status.HTTP_201_CREATED)
async def create_email_account(
    request: EmailAccountCreate,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """
    创建邮箱账户
    
    创建新的SMTP邮箱账户配置
    """
    # 检查邮箱是否已存在
    existing = db.query(EmailAccount).filter(
        EmailAccount.email == request.email
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email account '{request.email}' already exists"
        )
    
    # 加密密码
    encrypted_password = encrypt_password(request.smtp_password)
    
    # 创建账户
    account = EmailAccount(
        email=request.email,
        display_name=request.display_name,
        smtp_host=request.smtp_host,
        smtp_port=request.smtp_port,
        smtp_username=request.smtp_username,
        smtp_password=encrypted_password,
        use_tls=request.use_tls,
        daily_limit=request.daily_limit,
        priority=request.priority,
        is_active=request.is_active,
        remark=request.remark
    )
    
    db.add(account)
    db.commit()
    db.refresh(account)
    
    logger.info(f"Email account created: {account.email} by {api_key.name}")
    
    return ResponseModel(
        code=0,
        message="Email account created successfully",
        data=EmailAccountResponse.model_validate(account)
    )


@router.put("/{account_id}", response_model=ResponseModel[EmailAccountResponse])
async def update_email_account(
    account_id: int,
    request: EmailAccountUpdate,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """
    更新邮箱账户
    
    更新邮箱账户配置，只更新提供的字段
    """
    account = db.query(EmailAccount).filter(
        EmailAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email account not found"
        )
    
    # 更新字段
    update_data = request.model_dump(exclude_unset=True)
    
    # 如果有新密码，加密后存储
    if "smtp_password" in update_data and update_data["smtp_password"]:
        update_data["smtp_password"] = encrypt_password(update_data["smtp_password"])
    
    for field, value in update_data.items():
        setattr(account, field, value)
    
    db.commit()
    db.refresh(account)
    
    logger.info(f"Email account updated: {account.email} by {api_key.name}")
    
    return ResponseModel(
        code=0,
        message="Email account updated successfully",
        data=EmailAccountResponse.model_validate(account)
    )


@router.delete("/{account_id}", response_model=ResponseModel[None])
async def delete_email_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """
    删除邮箱账户
    
    删除邮箱账户（硬删除）
    """
    account = db.query(EmailAccount).filter(
        EmailAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email account not found"
        )
    
    db.delete(account)
    db.commit()
    
    logger.info(f"Email account deleted: {account.email} by {api_key.name}")
    
    return ResponseModel(
        code=0,
        message="Email account deleted successfully",
        data=None
    )


@router.post("/{account_id}/test", response_model=ResponseModel[EmailAccountTestResponse])
async def test_email_account(
    account_id: int,
    request: EmailAccountTestRequest,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """
    测试邮箱连接
    
    测试SMTP连接是否正常，并可选发送测试邮件
    """
    account = db.query(EmailAccount).filter(
        EmailAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email account not found"
        )
    
    # 解密密码
    try:
        smtp_password = decrypt_password(account.smtp_password)
    except Exception as e:
        logger.error(f"Failed to decrypt password for {account.email}: {e}")
        return ResponseModel(
            code=1,
            message="Failed to decrypt password",
            data=EmailAccountTestResponse(
                success=False,
                message="密码解密失败",
                error=str(e)
            )
        )
    
    # 测试连接
    start_time = time.time()
    
    try:
        # 创建SMTP连接
        async with aiosmtplib.SMTP(
            hostname=account.smtp_host,
            port=account.smtp_port,
            use_tls=account.use_tls,
            start_tls=False if account.smtp_port == 465 else True,
            timeout=10
        ) as smtp:
            # 登录
            await smtp.login(account.smtp_username, smtp_password)
            
            # 如果提供了测试邮箱，发送测试邮件
            if request.test_email:
                message = MIMEText(
                    f"这是来自消息通知平台的测试邮件。\n\n"
                    f"邮箱账户：{account.email}\n"
                    f"测试时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"如果您收到此邮件，说明邮箱配置正常！",
                    "plain",
                    "utf-8"
                )
                message["Subject"] = "【测试】邮箱连接测试"
                message["From"] = account.email
                message["To"] = request.test_email
                
                await smtp.sendmail(
                    account.email,
                    [request.test_email],
                    message.as_string()
                )
                
                success_msg = f"SMTP连接成功！测试邮件已发送到 {request.test_email}"
            else:
                success_msg = "SMTP连接成功！"
        
        duration_ms = (time.time() - start_time) * 1000
        
        # 重置失败计数
        if account.failure_count > 0:
            account.reset_failure_count()
            db.commit()
        
        logger.info(f"Email account test successful: {account.email}")
        
        return ResponseModel(
            code=0,
            message="Test successful",
            data=EmailAccountTestResponse(
                success=True,
                message=success_msg,
                duration_ms=round(duration_ms, 2)
            )
        )
        
    except aiosmtplib.SMTPAuthenticationError as e:
        duration_ms = (time.time() - start_time) * 1000
        error_msg = f"SMTP认证失败：{str(e)}"
        logger.error(f"SMTP authentication failed for {account.email}: {e}")
        
        return ResponseModel(
            code=1,
            message="Authentication failed",
            data=EmailAccountTestResponse(
                success=False,
                message="SMTP认证失败，请检查用户名和密码",
                error=error_msg,
                duration_ms=round(duration_ms, 2)
            )
        )
        
    except aiosmtplib.SMTPConnectError as e:
        duration_ms = (time.time() - start_time) * 1000
        error_msg = f"SMTP连接失败：{str(e)}"
        logger.error(f"SMTP connection failed for {account.email}: {e}")
        
        return ResponseModel(
            code=1,
            message="Connection failed",
            data=EmailAccountTestResponse(
                success=False,
                message="SMTP连接失败，请检查服务器地址和端口",
                error=error_msg,
                duration_ms=round(duration_ms, 2)
            )
        )
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        error_msg = f"测试失败：{str(e)}"
        logger.error(f"Email account test failed for {account.email}: {e}")
        
        return ResponseModel(
            code=1,
            message="Test failed",
            data=EmailAccountTestResponse(
                success=False,
                message="测试失败",
                error=error_msg,
                duration_ms=round(duration_ms, 2)
            )
        )


__all__ = ["router"]

