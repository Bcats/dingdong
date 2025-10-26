"""
管理员用户模型
"""
from sqlalchemy import Column, String, Boolean, Integer
from app.models.base import BaseModel


class AdminUser(BaseModel):
    """管理员用户表"""
    __tablename__ = "admin_users"

    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    nickname = Column(String(100), comment="昵称")
    email = Column(String(100), comment="邮箱")
    phone = Column(String(20), comment="手机号")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员")
    login_count = Column(Integer, default=0, comment="登录次数")
    last_login_at = Column(String(50), comment="最后登录时间")
    last_login_ip = Column(String(50), comment="最后登录IP")
    
    def __repr__(self):
        return f"<AdminUser(id={self.id}, username={self.username})>"

