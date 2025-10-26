"""
数据库连接和会话管理
"""
from typing import Generator
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool, QueuePool

from app.core.config import settings
from app.core.logger import logger


# 创建数据库引擎
if settings.DEBUG:
    # 开发环境使用NullPool（无连接池）
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        echo=settings.DB_ECHO,
    )
else:
    # 生产环境使用QueuePool（连接池）
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        pool_recycle=settings.DB_POOL_RECYCLE,
        pool_pre_ping=True,  # 连接前检查
        echo=settings.DB_ECHO,
    )


# 事件监听：记录慢查询
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """记录SQL执行开始时间"""
    conn.info.setdefault("query_start_time", []).append(None)
    import time
    conn.info["query_start_time"][-1] = time.time()


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """记录慢查询"""
    import time
    total_time = time.time() - conn.info["query_start_time"].pop()
    
    # 记录超过1秒的慢查询
    if total_time > 1.0:
        logger.warning(
            f"Slow query detected",
            extra={
                "duration": f"{total_time:.2f}s",
                "sql": statement[:500],  # 只记录前500个字符
            }
        )


# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# 创建Base类
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    
    用法：
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    初始化数据库
    创建所有表（仅用于开发环境，生产环境使用Alembic）
    """
    from app.models import message, email, template, api_key  # noqa
    
    if settings.is_development:
        logger.info("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    else:
        logger.warning("Database initialization skipped in production. Use Alembic migrations.")


def check_db_connection() -> bool:
    """
    检查数据库连接
    
    Returns:
        bool: 连接是否正常
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False


__all__ = ["engine", "SessionLocal", "Base", "get_db", "init_db", "check_db_connection"]

