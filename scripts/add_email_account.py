#!/usr/bin/env python3
"""
添加邮箱账户脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

from app.core.database import SessionLocal
from app.core.security import encrypt_data
from app.models.email import EmailAccount
from app.core.logger import logger


def add_email_account(
    email: str,
    smtp_host: str,
    smtp_port: int,
    smtp_username: str,
    smtp_password: str,
    display_name: str = None,
    daily_limit: int = 500,
    priority: int = 10,
    use_tls: bool = True
):
    """
    添加邮箱账户
    
    Args:
        email: 邮箱地址
        smtp_host: SMTP服务器
        smtp_port: SMTP端口
        smtp_username: SMTP用户名
        smtp_password: SMTP密码
        display_name: 显示名称
        daily_limit: 每日发送限额
        priority: 优先级
        use_tls: 是否使用TLS
    """
    db = SessionLocal()
    
    try:
        # 检查邮箱是否已存在
        existing = db.query(EmailAccount).filter(EmailAccount.email == email).first()
        if existing:
            print(f"❌ 邮箱账户已存在: {email}")
            return None
        
        # 加密密码
        encrypted_password = encrypt_data(smtp_password)
        
        # 创建邮箱账户
        account = EmailAccount(
            email=email,
            display_name=display_name or email,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_username=smtp_username,
            smtp_password=encrypted_password,
            use_tls=use_tls,
            daily_limit=daily_limit,
            priority=priority,
            is_active=True
        )
        
        db.add(account)
        db.commit()
        db.refresh(account)
        
        # 输出结果
        print("=" * 80)
        print("🎉 邮箱账户添加成功！")
        print("=" * 80)
        print(f"ID: {account.id}")
        print(f"邮箱: {account.email}")
        print(f"显示名称: {account.display_name}")
        print(f"SMTP服务器: {account.smtp_host}:{account.smtp_port}")
        print(f"每日限额: {account.daily_limit}")
        print(f"优先级: {account.priority}")
        print(f"是否启用: {account.is_active}")
        print(f"使用TLS: {account.use_tls}")
        print("=" * 80)
        
        logger.info(f"Email account added: {email}")
        return account
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add email account: {str(e)}")
        print(f"❌ 添加失败: {str(e)}")
        raise
    finally:
        db.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="添加邮箱账户")
    parser.add_argument("--email", required=True, help="邮箱地址")
    parser.add_argument("--smtp-host", required=True, help="SMTP服务器")
    parser.add_argument("--smtp-port", type=int, default=465, help="SMTP端口")
    parser.add_argument("--smtp-username", required=True, help="SMTP用户名")
    parser.add_argument("--smtp-password", required=True, help="SMTP密码")
    parser.add_argument("--display-name", help="显示名称")
    parser.add_argument("--daily-limit", type=int, default=500, help="每日发送限额")
    parser.add_argument("--priority", type=int, default=10, help="优先级")
    parser.add_argument("--no-tls", action="store_true", help="不使用TLS")
    
    args = parser.parse_args()
    
    add_email_account(
        email=args.email,
        smtp_host=args.smtp_host,
        smtp_port=args.smtp_port,
        smtp_username=args.smtp_username,
        smtp_password=args.smtp_password,
        display_name=args.display_name,
        daily_limit=args.daily_limit,
        priority=args.priority,
        use_tls=not args.no_tls
    )


if __name__ == "__main__":
    main()

