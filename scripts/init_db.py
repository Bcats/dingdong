#!/usr/bin/env python3
"""
初始化数据库脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base, check_db_connection
from app.core.logger import logger
from app.models import *  # noqa


def init_database():
    """初始化数据库"""
    print("=" * 80)
    print("🚀 开始初始化数据库...")
    print("=" * 80)
    
    # 检查数据库连接
    print("1. 检查数据库连接...")
    if not check_db_connection():
        print("❌ 数据库连接失败！")
        return False
    print("✅ 数据库连接成功")
    
    # 创建所有表
    print("\n2. 创建数据库表...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功")
    except Exception as e:
        print(f"❌ 创建表失败: {str(e)}")
        logger.error(f"Failed to create tables: {str(e)}")
        return False
    
    # 列出所有创建的表
    print("\n3. 已创建的表：")
    for table in Base.metadata.sorted_tables:
        print(f"   - {table.name}")
    
    print("\n" + "=" * 80)
    print("✅ 数据库初始化完成！")
    print("=" * 80)
    print("\n下一步：")
    print("1. 运行数据库迁移: alembic upgrade head")
    print("2. 创建API密钥: python scripts/create_api_key.py --name '默认密钥'")
    print("3. 添加邮箱账户: python scripts/add_email_account.py --email xxx@example.com ...")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    init_database()

