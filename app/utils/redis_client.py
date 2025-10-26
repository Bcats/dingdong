"""
Redis客户端封装
"""
import redis
from typing import Optional, Any
import json
from app.core.config import settings
from app.core.logger import logger


class RedisClient:
    """Redis客户端"""
    
    def __init__(self):
        """初始化Redis连接"""
        self.client = redis.from_url(
            settings.REDIS_URL,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
            socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
            socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[str]:
        """获取值"""
        try:
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Redis GET error: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """设置值"""
        try:
            return self.client.set(key, value, ex=ex)
        except Exception as e:
            logger.error(f"Redis SET error: {str(e)}")
            return False
    
    def setex(self, key: str, time: int, value: Any) -> bool:
        """设置值（带过期时间）"""
        try:
            return self.client.setex(key, time, value)
        except Exception as e:
            logger.error(f"Redis SETEX error: {str(e)}")
            return False
    
    def delete(self, *keys: str) -> int:
        """删除键"""
        try:
            return self.client.delete(*keys)
        except Exception as e:
            logger.error(f"Redis DELETE error: {str(e)}")
            return 0
    
    def exists(self, *keys: str) -> int:
        """检查键是否存在"""
        try:
            return self.client.exists(*keys)
        except Exception as e:
            logger.error(f"Redis EXISTS error: {str(e)}")
            return 0
    
    def expire(self, key: str, time: int) -> bool:
        """设置过期时间"""
        try:
            return self.client.expire(key, time)
        except Exception as e:
            logger.error(f"Redis EXPIRE error: {str(e)}")
            return False
    
    def ttl(self, key: str) -> int:
        """获取TTL"""
        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(f"Redis TTL error: {str(e)}")
            return -1
    
    def incr(self, key: str, amount: int = 1) -> int:
        """递增"""
        try:
            return self.client.incr(key, amount)
        except Exception as e:
            logger.error(f"Redis INCR error: {str(e)}")
            return 0
    
    def decr(self, key: str, amount: int = 1) -> int:
        """递减"""
        try:
            return self.client.decr(key, amount)
        except Exception as e:
            logger.error(f"Redis DECR error: {str(e)}")
            return 0
    
    def hget(self, name: str, key: str) -> Optional[str]:
        """获取哈希值"""
        try:
            return self.client.hget(name, key)
        except Exception as e:
            logger.error(f"Redis HGET error: {str(e)}")
            return None
    
    def hset(self, name: str, key: str, value: Any) -> int:
        """设置哈希值"""
        try:
            return self.client.hset(name, key, value)
        except Exception as e:
            logger.error(f"Redis HSET error: {str(e)}")
            return 0
    
    def hgetall(self, name: str) -> dict:
        """获取所有哈希值"""
        try:
            return self.client.hgetall(name)
        except Exception as e:
            logger.error(f"Redis HGETALL error: {str(e)}")
            return {}
    
    def set_json(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """设置JSON值"""
        try:
            json_str = json.dumps(value, ensure_ascii=False)
            return self.set(key, json_str, ex=ex)
        except Exception as e:
            logger.error(f"Redis SET_JSON error: {str(e)}")
            return False
    
    def get_json(self, key: str) -> Optional[Any]:
        """获取JSON值"""
        try:
            value = self.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis GET_JSON error: {str(e)}")
            return None
    
    def ping(self) -> bool:
        """检查连接"""
        try:
            return self.client.ping()
        except Exception as e:
            logger.error(f"Redis PING error: {str(e)}")
            return False


# 创建全局Redis客户端实例
redis_client = RedisClient()


__all__ = ["RedisClient", "redis_client"]

