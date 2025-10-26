"""
模板API
"""
from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_api_key, get_current_user
from app.models.api_key import APIKey
from app.models.admin_user import AdminUser
from app.models.template import MessageTemplate, MessageTemplateHistory
from app.schemas import (
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    TemplatePreviewRequest,
    TemplatePreviewResponse,
    TemplateHistoryResponse,
    TemplateRollbackRequest,
    ResponseModel,
)
from app.services.template_service import TemplateService
from app.core.logger import logger


router = APIRouter(prefix="/templates", tags=["Templates"])


@router.post("", response_model=ResponseModel[TemplateResponse], status_code=status.HTTP_201_CREATED)
async def create_template(
    request: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """创建模板"""
    # 检查编码是否已存在
    existing = db.query(MessageTemplate).filter(MessageTemplate.code == request.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template with code '{request.code}' already exists"
        )
    
    # 创建模板
    template = MessageTemplate(
        code=request.code,
        name=request.name,
        type=request.type,
        description=request.description,
        subject_template=request.subject_template,
        content_template=request.content_template,
        variables=request.variables,
        created_by=api_key.name
    )
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    # 创建初始版本历史
    template_service = TemplateService(db)
    template_service.create_version_history(
        template,
        change_reason="Initial creation",
        changed_by=api_key.name
    )
    
    logger.info(f"Template created: {template.code}")
    
    return ResponseModel(
        code=0,
        message="Template created successfully",
        data=TemplateResponse.model_validate(template)
    )


@router.get("", response_model=ResponseModel[List[TemplateResponse]])
async def list_templates(
    type: str = None,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """查询模板列表"""
    query = db.query(MessageTemplate).filter(MessageTemplate.deleted_at == None)
    
    if type:
        query = query.filter(MessageTemplate.type == type)
    if is_active is not None:
        query = query.filter(MessageTemplate.is_active == is_active)
    
    templates = query.all()
    
    return ResponseModel(
        code=0,
        message="Success",
        data=[TemplateResponse.model_validate(t) for t in templates]
    )


@router.get("/{template_id}", response_model=ResponseModel[TemplateResponse])
async def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """获取模板详情"""
    template = db.query(MessageTemplate).filter(
        MessageTemplate.id == template_id,
        MessageTemplate.deleted_at == None
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return ResponseModel(
        code=0,
        message="Success",
        data=TemplateResponse.model_validate(template)
    )


@router.put("/{template_id}", response_model=ResponseModel[TemplateResponse])
async def update_template(
    template_id: int,
    request: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """更新模板"""
    template = db.query(MessageTemplate).filter(
        MessageTemplate.id == template_id,
        MessageTemplate.deleted_at == None
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    template_service = TemplateService(db)
    
    # 更新模板
    updated_template = template_service.update_template(
        template=template,
        subject_template=request.subject_template,
        content_template=request.content_template,
        variables=request.variables,
        change_reason=request.change_reason,
        changed_by=api_key.name
    )
    
    # 更新其他字段
    if request.name is not None:
        updated_template.name = request.name
    if request.description is not None:
        updated_template.description = request.description
    if request.is_active is not None:
        updated_template.is_active = request.is_active
    
    db.commit()
    db.refresh(updated_template)
    
    logger.info(f"Template updated: {updated_template.code}")
    
    return ResponseModel(
        code=0,
        message="Template updated successfully",
        data=TemplateResponse.model_validate(updated_template)
    )


@router.delete("/{template_id}", response_model=ResponseModel[None])
async def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """删除模板（软删除）"""
    template = db.query(MessageTemplate).filter(
        MessageTemplate.id == template_id,
        MessageTemplate.deleted_at == None
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    template.soft_delete()
    db.commit()
    
    logger.info(f"Template deleted: {template.code}")
    
    return ResponseModel(
        code=0,
        message="Template deleted successfully",
        data=None
    )


@router.post("/preview", response_model=ResponseModel[TemplatePreviewResponse])
async def preview_template(
    request: TemplatePreviewRequest,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """预览模板"""
    template_service = TemplateService(db)
    
    success, subject, content, error = template_service.preview_template(
        subject_template=request.subject_template,
        content_template=request.content_template,
        variables=request.variables
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return ResponseModel(
        code=0,
        message="Success",
        data=TemplatePreviewResponse(
            subject=subject,
            content=content
        )
    )


@router.get("/{template_id}/history", response_model=ResponseModel[List[TemplateHistoryResponse]])
async def get_template_history(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """获取模板历史版本"""
    template = db.query(MessageTemplate).filter(
        MessageTemplate.id == template_id,
        MessageTemplate.deleted_at == None
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    history = db.query(MessageTemplateHistory).filter(
        MessageTemplateHistory.template_id == template_id
    ).order_by(MessageTemplateHistory.version.desc()).all()
    
    return ResponseModel(
        code=0,
        message="Success",
        data=[TemplateHistoryResponse.model_validate(h) for h in history]
    )


@router.post("/{template_id}/rollback", response_model=ResponseModel[TemplateResponse])
async def rollback_template(
    template_id: int,
    request: TemplateRollbackRequest,
    db: Session = Depends(get_db),
    current_user: Union[AdminUser, APIKey] = Depends(get_current_user)
):
    """回滚模板到指定版本"""
    template = db.query(MessageTemplate).filter(
        MessageTemplate.id == template_id,
        MessageTemplate.deleted_at == None
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    template_service = TemplateService(db)
    
    updated_template = template_service.rollback_template(
        template=template,
        target_version=request.target_version,
        changed_by=api_key.name
    )
    
    if not updated_template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Version {request.target_version} not found"
        )
    
    logger.info(f"Template rolled back: {template.code} to version {request.target_version}")
    
    return ResponseModel(
        code=0,
        message="Template rolled back successfully",
        data=TemplateResponse.model_validate(updated_template)
    )


__all__ = ["router"]

