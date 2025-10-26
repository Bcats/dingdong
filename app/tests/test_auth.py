"""
认证API测试
"""
import pytest


def test_get_token_success(client, api_key_fixture):
    """测试获取Token成功"""
    response = client.post(
        "/api/v1/auth/token",
        json={
            "api_key": api_key_fixture["api_key"],
            "api_secret": api_key_fixture["api_secret"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


def test_get_token_invalid_credentials(client):
    """测试无效凭证"""
    response = client.post(
        "/api/v1/auth/token",
        json={
            "api_key": "invalid_key",
            "api_secret": "invalid_secret"
        }
    )
    
    assert response.status_code == 401

