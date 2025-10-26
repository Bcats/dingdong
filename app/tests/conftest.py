"""
Pytest配置文件
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings


# 创建测试数据库引擎
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def api_key_fixture(db_session):
    """创建测试API Key"""
    from app.models.api_key import APIKey
    from app.core.security import generate_api_key, generate_api_secret, hash_password
    
    api_key_str = generate_api_key()
    api_secret_str = generate_api_secret()
    
    api_key = APIKey(
        api_key=api_key_str,
        api_secret_hash=hash_password(api_secret_str),
        name="test_key",
        is_active=True
    )
    
    db_session.add(api_key)
    db_session.commit()
    db_session.refresh(api_key)
    
    return {
        "api_key": api_key_str,
        "api_secret": api_secret_str,
        "object": api_key
    }

