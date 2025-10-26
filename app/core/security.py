"""
安全相关功能
包括密码哈希、JWT Token、数据加密等
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import bcrypt
from cryptography.fernet import Fernet

from app.core.config import settings
from app.core.logger import logger

# Fernet加密实例
try:
    fernet = Fernet(settings.ENCRYPTION_KEY.encode())
except Exception as e:
    logger.error(f"Failed to initialize Fernet encryption: {str(e)}")
    logger.warning("Please generate a valid Fernet key using: from cryptography.fernet import Fernet; print(Fernet.generate_key())")
    raise


def hash_password(password: str) -> str:
    """
    哈希密码
    
    Args:
        password: 明文密码
        
    Returns:
        str: 哈希后的密码
    """
    # bcrypt有72字节的限制，手动截断
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # 使用 bcrypt 直接哈希
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码
        
    Returns:
        bool: 是否匹配
    """
    # bcrypt有72字节的限制，手动截断
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # 使用 bcrypt 直接验证
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量
        
    Returns:
        str: JWT Token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    
    # 更新过期时间和签发时间
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    
    # 如果没有指定type，默认为"access"
    if "type" not in to_encode:
        to_encode["type"] = "access"
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建刷新令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量
        
    Returns:
        str: JWT Token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解码JWT Token
    
    Args:
        token: JWT Token
        
    Returns:
        Optional[Dict]: 解码后的数据，如果失败返回None
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {str(e)}")
        return None


def encrypt_data(data: str) -> str:
    """
    加密数据（使用Fernet对称加密）
    
    Args:
        data: 明文数据
        
    Returns:
        str: 加密后的数据（Base64编码）
    """
    try:
        encrypted = fernet.encrypt(data.encode())
        return encrypted.decode()
    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        raise


def decrypt_data(encrypted_data: str) -> str:
    """
    解密数据
    
    Args:
        encrypted_data: 加密的数据（Base64编码）
        
    Returns:
        str: 明文数据
    """
    try:
        decrypted = fernet.decrypt(encrypted_data.encode())
        return decrypted.decode()
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        raise


def generate_api_key() -> str:
    """
    生成API Key
    
    Returns:
        str: API Key (格式: noti_xxxxx)
    """
    import secrets
    random_part = secrets.token_urlsafe(32)
    return f"noti_{random_part}"


def generate_api_secret() -> str:
    """
    生成API Secret
    
    Returns:
        str: API Secret (格式: secret_xxxxx)
    """
    import secrets
    # bcrypt限制密码长度为72字节，使用更短的随机部分
    # token_urlsafe(24) 生成约32字符，加上"secret_"前缀，总长度约39字符
    random_part = secrets.token_urlsafe(24)
    return f"secret_{random_part}"


def generate_request_id() -> str:
    """
    生成请求ID
    
    Returns:
        str: 请求ID (UUID格式)
    """
    import uuid
    return str(uuid.uuid4())


# 为了语义清晰，添加密码加密的别名函数
def encrypt_password(password: str) -> str:
    """
    加密密码（SMTP密码等敏感信息）
    
    这是encrypt_data的别名，用于语义更清晰
    
    Args:
        password: 明文密码
        
    Returns:
        str: 加密后的密码
    """
    return encrypt_data(password)


def decrypt_password(encrypted_password: str) -> str:
    """
    解密密码
    
    这是decrypt_data的别名，用于语义更清晰
    
    Args:
        encrypted_password: 加密的密码
        
    Returns:
        str: 明文密码
    """
    return decrypt_data(encrypted_password)


__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "encrypt_data",
    "decrypt_data",
    "encrypt_password",
    "decrypt_password",
    "generate_api_key",
    "generate_api_secret",
    "generate_request_id",
]

