"""
模板服务
处理消息模板的渲染、版本管理等
"""
from typing import Dict, Any, Optional
from jinja2 import Template, TemplateSyntaxError, UndefinedError
from sqlalchemy.orm import Session

from app.models.template import MessageTemplate, MessageTemplateHistory, TemplateType
from app.core.logger import logger


class TemplateService:
    """模板服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_template(self, code: str) -> Optional[MessageTemplate]:
        """
        根据编码获取模板
        
        Args:
            code: 模板编码
            
        Returns:
            Optional[MessageTemplate]: 模板对象
        """
        template = (
            self.db.query(MessageTemplate)
            .filter(
                MessageTemplate.code == code,
                MessageTemplate.is_active == True,
                MessageTemplate.deleted_at == None
            )
            .first()
        )
        
        if not template:
            logger.warning(f"Template not found or inactive: {code}")
        
        return template
    
    def render_template(
        self,
        template_str: str,
        variables: Dict[str, Any]
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """
        渲染模板
        
        Args:
            template_str: 模板字符串（Jinja2语法）
            variables: 模板变量
            
        Returns:
            tuple: (是否成功, 渲染结果, 错误信息)
        """
        try:
            template = Template(template_str)
            result = template.render(**variables)
            return True, result, None
        except TemplateSyntaxError as e:
            error_msg = f"Template syntax error: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
        except UndefinedError as e:
            error_msg = f"Template variable undefined: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Template render error: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def render_message_template(
        self,
        code: str,
        variables: Dict[str, Any]
    ) -> tuple[bool, Optional[str], Optional[str], Optional[str], Optional[int]]:
        """
        渲染消息模板（主题+内容）
        
        Args:
            code: 模板编码
            variables: 模板变量
            
        Returns:
            tuple: (是否成功, 主题, 内容, 错误信息, 版本号)
        """
        template = self.get_template(code)
        if not template:
            return False, None, None, f"Template not found: {code}", None
        
        # 渲染主题
        subject = None
        if template.subject_template:
            success, subject, error = self.render_template(
                template.subject_template,
                variables
            )
            if not success:
                return False, None, None, f"Subject render error: {error}", template.version
        
        # 渲染内容
        success, content, error = self.render_template(
            template.content_template,
            variables
        )
        if not success:
            return False, None, None, f"Content render error: {error}", template.version
        
        return True, subject, content, None, template.version
    
    def create_version_history(
        self,
        template: MessageTemplate,
        change_reason: Optional[str] = None,
        changed_by: Optional[str] = None
    ) -> MessageTemplateHistory:
        """
        创建模板版本历史
        
        Args:
            template: 模板对象
            change_reason: 变更原因
            changed_by: 变更人
            
        Returns:
            MessageTemplateHistory: 历史记录
        """
        history = MessageTemplateHistory(
            template_id=template.id,
            version=template.version,
            subject_template=template.subject_template,
            content_template=template.content_template,
            variables=template.variables,
            change_reason=change_reason,
            changed_by=changed_by
        )
        
        self.db.add(history)
        self.db.commit()
        
        logger.info(f"Created version history for template {template.code}, version {template.version}")
        return history
    
    def update_template(
        self,
        template: MessageTemplate,
        subject_template: Optional[str] = None,
        content_template: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        change_reason: Optional[str] = None,
        changed_by: Optional[str] = None
    ) -> MessageTemplate:
        """
        更新模板并创建历史版本
        
        Args:
            template: 模板对象
            subject_template: 新的主题模板
            content_template: 新的内容模板
            variables: 新的变量定义
            change_reason: 变更原因
            changed_by: 变更人
            
        Returns:
            MessageTemplate: 更新后的模板
        """
        # 创建历史版本
        self.create_version_history(template, change_reason, changed_by)
        
        # 更新模板
        if subject_template is not None:
            template.subject_template = subject_template
        if content_template is not None:
            template.content_template = content_template
        if variables is not None:
            template.variables = variables
        
        template.version += 1
        template.updated_by = changed_by
        
        self.db.commit()
        
        logger.info(f"Updated template {template.code} to version {template.version}")
        return template
    
    def rollback_template(
        self,
        template: MessageTemplate,
        target_version: int,
        changed_by: Optional[str] = None
    ) -> Optional[MessageTemplate]:
        """
        回滚模板到指定版本
        
        Args:
            template: 模板对象
            target_version: 目标版本号
            changed_by: 操作人
            
        Returns:
            Optional[MessageTemplate]: 回滚后的模板，如果失败返回None
        """
        # 查找目标版本
        history = (
            self.db.query(MessageTemplateHistory)
            .filter(
                MessageTemplateHistory.template_id == template.id,
                MessageTemplateHistory.version == target_version
            )
            .first()
        )
        
        if not history:
            logger.warning(f"Version {target_version} not found for template {template.code}")
            return None
        
        # 创建当前版本的历史记录
        self.create_version_history(
            template,
            change_reason=f"Rollback from version {template.version} to {target_version}",
            changed_by=changed_by
        )
        
        # 恢复到目标版本
        template.subject_template = history.subject_template
        template.content_template = history.content_template
        template.variables = history.variables
        template.version += 1  # 回滚也算一个新版本
        template.updated_by = changed_by
        
        self.db.commit()
        
        logger.info(f"Rolled back template {template.code} to version {target_version}, new version is {template.version}")
        return template
    
    def preview_template(
        self,
        subject_template: Optional[str],
        content_template: str,
        variables: Dict[str, Any]
    ) -> tuple[bool, Optional[str], Optional[str], Optional[str]]:
        """
        预览模板渲染结果
        
        Args:
            subject_template: 主题模板
            content_template: 内容模板
            variables: 模板变量
            
        Returns:
            tuple: (是否成功, 主题, 内容, 错误信息)
        """
        # 渲染主题
        subject = None
        if subject_template:
            success, subject, error = self.render_template(subject_template, variables)
            if not success:
                return False, None, None, f"Subject render error: {error}"
        
        # 渲染内容
        success, content, error = self.render_template(content_template, variables)
        if not success:
            return False, None, None, f"Content render error: {error}"
        
        return True, subject, content, None


__all__ = ["TemplateService"]

