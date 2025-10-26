"""Pydantic数据模型"""
from app.schemas.common import ResponseModel, PaginationModel, PagedResponse, HealthResponse
from app.schemas.auth import TokenRequest, TokenResponse
from app.schemas.message import (
    EmailSendRequest,
    EmailSendResponse,
    MessageQuery,
    MessageResponse,
    BatchQueryRequest,
)
from app.schemas.template import (
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    TemplatePreviewRequest,
    TemplatePreviewResponse,
    TemplateHistoryResponse,
    TemplateRollbackRequest,
)
from app.schemas.email_account import (
    EmailAccountCreate,
    EmailAccountUpdate,
    EmailAccountResponse,
    EmailAccountTestRequest,
    EmailAccountTestResponse,
)


__all__ = [
    # Common
    "ResponseModel",
    "PaginationModel",
    "PagedResponse",
    "HealthResponse",
    
    # Auth
    "TokenRequest",
    "TokenResponse",
    
    # Message
    "EmailSendRequest",
    "EmailSendResponse",
    "MessageQuery",
    "MessageResponse",
    "BatchQueryRequest",
    
    # Template
    "TemplateCreate",
    "TemplateUpdate",
    "TemplateResponse",
    "TemplatePreviewRequest",
    "TemplatePreviewResponse",
    "TemplateHistoryResponse",
    "TemplateRollbackRequest",
    
    # Email Account
    "EmailAccountCreate",
    "EmailAccountUpdate",
    "EmailAccountResponse",
    "EmailAccountTestRequest",
    "EmailAccountTestResponse",
]
