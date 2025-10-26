#!/usr/bin/env python3
"""
创建API密钥脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from datetime import datetime, timedelta

from app.core.database import SessionLocal
from app.core.security import generate_api_key, generate_api_secret, hash_password
from app.models.api_key import APIKey
from app.core.logger import logger


def create_api_key(
    name: str,
    description: str = None,
    expires_days: int = None,
    created_by: str = "system"
):
    """
    创建API密钥
    
    Args:
        name: 密钥名称
        description: 密钥描述
        expires_days: 过期天数（None表示永不过期）
        created_by: 创建人
    """
    db = SessionLocal()
    
    try:
        # 生成API Key和Secret
        api_key_str = generate_api_key()
        api_secret_str = generate_api_secret()
        
        # 计算过期时间
        expires_at = None
        if expires_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_days)
        
        # 创建API Key记录
        api_key = APIKey(
            api_key=api_key_str,
            api_secret_hash=hash_password(api_secret_str),
            name=name,
            description=description,
            expires_at=expires_at,
            created_by=created_by
        )
        
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        
        # 输出结果
        print("=" * 80)
        print("🎉 API密钥创建成功！")
        print("=" * 80)
        print(f"ID: {api_key.id}")
        print(f"名称: {api_key.name}")
        print(f"描述: {api_key.description or 'N/A'}")
        print(f"创建时间: {api_key.created_at}")
        print(f"过期时间: {api_key.expires_at or '永不过期'}")
        print("=" * 80)
        print("⚠️  请妥善保管以下信息，API Secret只显示一次！")
        print("=" * 80)
        print(f"API Key:    {api_key_str}")
        print(f"API Secret: {api_secret_str}")
        print("=" * 80)
        print("\n使用示例：")
        print(f"""
curl -X POST http://localhost:8000/api/v1/auth/token \\
  -H "Content-Type: application/json" \\
  -d '{{
    "api_key": "{api_key_str}",
    "api_secret": "{api_secret_str}"
  }}'
""")
        
        logger.info(f"API Key created: {name}")
        return api_key
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create API Key: {str(e)}")
        print(f"❌ 创建失败: {str(e)}")
        raise
    finally:
        db.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="创建API密钥")
    parser.add_argument("--name", required=True, help="密钥名称")
    parser.add_argument("--description", help="密钥描述")
    parser.add_argument("--expires-days", type=int, help="过期天数（不指定则永不过期）")
    parser.add_argument("--created-by", default="system", help="创建人")
    
    args = parser.parse_args()
    
    create_api_key(
        name=args.name,
        description=args.description,
        expires_days=args.expires_days,
        created_by=args.created_by
    )


if __name__ == "__main__":
    main()

