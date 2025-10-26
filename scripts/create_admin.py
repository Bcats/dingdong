"""
创建默认管理员账号
"""
from app.core.database import SessionLocal
from app.models import AdminUser
from app.core.security import get_password_hash


def create_default_admin():
    """创建默认管理员账号"""
    db = SessionLocal()
    
    try:
        # 检查是否已存在
        existing = db.query(AdminUser).filter(AdminUser.username == 'admin').first()
        
        if existing:
            print('⚠️  管理员账号已存在')
            print(f'   ID: {existing.id}')
            print(f'   用户名: {existing.username}')
            print(f'   昵称: {existing.nickname}')
            return
        
        # 创建管理员账号
        admin = AdminUser(
            username='admin',
            password_hash=get_password_hash('admin123'),
            nickname='系统管理员',
            is_active=True,
            is_superuser=True,
            login_count=0
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print('✅ 默认管理员账号创建成功')
        print(f'   ID: {admin.id}')
        print('   用户名: admin')
        print('   密码: admin123')
        print(f'   昵称: {admin.nickname}')
        
    except Exception as e:
        print(f'❌ 创建失败: {str(e)}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    create_default_admin()


