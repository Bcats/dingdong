# Python开发规范手册 - 消息通知平台

**版本**：v1.0  
**日期**：2025-10-24  
**制定人**：技术委员会  
**参考标准**：阿里巴巴开发规范 + PEP 8 + Google Python Style Guide

---

## 【强制】【推荐】【参考】说明

- 🔴 **【强制】**：必须遵守的规约，违反会导致代码无法通过Code Review或导致严重问题
- 🟡 **【推荐】**：建议遵守的规约，有助于提升代码质量
- 🟢 **【参考】**：可以参考的规约，根据实际情况灵活使用

---

## 一、编程规约

### 1.1 命名风格

#### 1.1.1 【强制】代码中的命名均不能以下划线或美元符号开始或结束

**反例**：
```python
_name = "test"
name_ = "test"
```

**正例**：
```python
user_name = "test"
email_address = "test@example.com"
```

#### 1.1.2 【强制】代码中的命名严禁使用拼音与英文混合的方式，更不允许直接使用中文

说明：正确的英文拼写和语法可以让阅读者易于理解，避免歧义。

**反例**：
```python
# 拼音命名
yonghu_name = "张三"

# 中文命名
用户名 = "张三"

# 拼音英文混合
getPingfenByName()
```

**正例**：
```python
user_name = "张三"
get_score_by_name()
```

**例外**：国际通用的名称，如alibaba、taobao、youku、hangzhou等。

#### 1.1.3 【强制】类名使用UpperCamelCase风格

**正例**：
```python
class EmailService:
    pass

class MessageTemplate:
    pass

class UserDTO:
    pass
```

#### 1.1.4 【强制】方法名、参数名、成员变量、局部变量都统一使用snake_case风格

**正例**：
```python
def send_email(recipient_address: str, email_content: str) -> bool:
    message_id = generate_message_id()
    return True
```

#### 1.1.5 【强制】常量命名全部大写，单词间用下划线隔开

**正例**：
```python
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
EMAIL_DAILY_LIMIT = 500
```

#### 1.1.6 【强制】类型变量名应该简短且有意义

**正例**：
```python
from typing import TypeVar

T = TypeVar('T')
KT = TypeVar('KT')  # Key Type
VT = TypeVar('VT')  # Value Type
```

#### 1.1.7 【推荐】如果模块名与类名相同，模块名使用小写

**正例**：
```python
# 文件：email_service.py
class EmailService:
    pass
```

#### 1.1.8 【推荐】避免使用单字符变量名，除非是循环迭代器

**反例**：
```python
def process(d, t, s):
    pass
```

**正例**：
```python
def process_message(data: dict, message_type: str, status: str):
    pass

# 循环中可以使用单字符
for i in range(10):
    print(i)
```

### 1.2 常量定义

#### 1.2.1 【强制】不允许任何魔法值（即未经预先定义的常量）直接出现在代码中

**反例**：
```python
def check_retry_count(count: int) -> bool:
    if count > 3:  # 魔法值
        return False
    return True
```

**正例**：
```python
MAX_RETRY_COUNT = 3

def check_retry_count(count: int) -> bool:
    if count > MAX_RETRY_COUNT:
        return False
    return True
```

#### 1.2.2 【推荐】使用枚举类定义相关常量

**正例**：
```python
from enum import Enum

class MessageStatus(str, Enum):
    """消息状态枚举"""
    PENDING = "pending"
    SENDING = "sending"
    SUCCESS = "success"
    FAILED = "failed"

class MessageType(str, Enum):
    """消息类型枚举"""
    EMAIL = "email"
    SMS = "sms"
    WECHAT = "wechat"
```

### 1.3 代码格式

#### 1.3.1 【强制】使用4个空格进行缩进，禁止使用Tab字符

说明：混用Tab和空格会导致代码格式混乱。

**配置Black自动格式化**：
```bash
black --line-length 100 --target-version py310 .
```

#### 1.3.2 【强制】每行代码最大长度不超过100个字符

说明：过长的行会影响可读性。

**正例**：
```python
# 长参数列表换行
def send_email(
    recipient: str,
    subject: str,
    content: str,
    attachments: list = None,
    cc: list = None,
    bcc: list = None
) -> dict:
    pass

# 长字符串换行
error_message = (
    "发送失败：SMTP连接超时，"
    "请检查网络连接或联系系统管理员"
)
```

#### 1.3.3 【强制】左大括号不换行，右大括号单独一行

说明：虽然Python没有大括号，但字典、列表等结构遵循类似原则。

**正例**：
```python
user_info = {
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 30
}

email_list = [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com"
]
```

#### 1.3.4 【强制】if/elif/else/try/except/finally/with等语句必须有冒号

**正例**：
```python
if message_status == MessageStatus.SUCCESS:
    logger.info("消息发送成功")
elif message_status == MessageStatus.FAILED:
    logger.error("消息发送失败")
else:
    logger.warning("消息状态未知")
```

#### 1.3.5 【推荐】运算符前后、逗号后面需要加空格

**正例**：
```python
result = a + b
items = [1, 2, 3, 4, 5]
user_dict = {"name": "test", "age": 20}
```

#### 1.3.6 【推荐】函数定义之间空两行，类方法之间空一行

**正例**：
```python
class EmailService:
    """邮件服务类"""
    
    def __init__(self):
        pass
    
    def send_email(self, recipient: str) -> bool:
        """发送邮件"""
        pass
    
    def get_account(self) -> dict:
        """获取邮箱账户"""
        pass


def send_message(message_id: str) -> bool:
    """发送消息（模块级函数）"""
    pass


def get_message(message_id: str) -> dict:
    """获取消息（模块级函数）"""
    pass
```

### 1.4 注释规约

#### 1.4.1 【强制】类、类属性、类方法的注释必须使用Docstring，不得使用单行注释

**正例**：
```python
class EmailService:
    """邮件服务类
    
    提供邮件发送、邮箱池管理等功能。
    
    Attributes:
        email_pool: 邮箱池对象
        retry_count: 重试次数
    """
    
    def send_email(self, recipient: str, subject: str, content: str) -> bool:
        """发送邮件
        
        Args:
            recipient: 收件人邮箱地址
            subject: 邮件主题
            content: 邮件内容（支持HTML）
            
        Returns:
            bool: 发送成功返回True，失败返回False
            
        Raises:
            ValueError: 当邮箱地址格式不正确时
            SMTPException: 当SMTP连接失败时
            
        Examples:
            >>> service = EmailService()
            >>> service.send_email("user@example.com", "测试", "<p>测试内容</p>")
            True
        """
        pass
```

#### 1.4.2 【强制】所有的抽象方法（包括接口中的方法）必须用Docstring注释

**正例**：
```python
from abc import ABC, abstractmethod

class MessageSender(ABC):
    """消息发送器抽象基类"""
    
    @abstractmethod
    def send(self, recipient: str, content: str) -> bool:
        """发送消息
        
        Args:
            recipient: 接收人
            content: 消息内容
            
        Returns:
            bool: 发送成功返回True
        """
        pass
```

#### 1.4.3 【强制】所有的类都必须添加创建者和创建日期

**正例**：
```python
class EmailService:
    """邮件服务类
    
    提供邮件发送、邮箱池管理等功能。
    
    Author:
        张三 (zhangsan@example.com)
        
    Created:
        2025-10-24
        
    Modified:
        2025-10-25 - 添加邮箱池自动切换功能
    """
    pass
```

#### 1.4.4 【推荐】方法内部单行注释，在被注释语句上方另起一行，使用 # 注释

**正例**：
```python
def process_message(message: dict) -> bool:
    # 验证消息格式
    if not validate_message(message):
        return False
    
    # 获取可用的邮箱账户
    account = email_pool.get_available_account()
    
    # 发送邮件
    return send_via_smtp(account, message)
```

#### 1.4.5 【推荐】特殊注释标记，请注明标记人与标记时间

**正例**：
```python
def send_email(recipient: str) -> bool:
    # TODO(zhangsan 2025-10-24): 添加发送失败重试机制
    # FIXME(lisi 2025-10-25): 修复邮箱池并发访问问题
    # NOTE: 该方法暂不支持附件发送
    pass
```

**标记说明**：
- `TODO`: 待实现的功能
- `FIXME`: 需要修复的bug
- `NOTE`: 重要说明
- `HACK`: 临时解决方案
- `XXX`: 需要优化的代码

#### 1.4.6 【推荐】复杂的业务逻辑必须添加注释

**正例**：
```python
def select_email_account(self) -> Optional[EmailAccount]:
    """选择可用的邮箱账户
    
    选择策略：
    1. 优先选择priority字段值大的邮箱（优先级高）
    2. 相同优先级下，选择daily_sent_count最小的（发送数量少）
    3. 跳过is_active=False的邮箱（已禁用）
    4. 跳过daily_sent_count >= daily_limit的邮箱（已达上限）
    
    Returns:
        EmailAccount: 可用的邮箱账户，如果没有可用账户返回None
    """
    accounts = (
        db.query(EmailAccount)
        .filter(
            EmailAccount.is_active == True,
            EmailAccount.daily_sent_count < EmailAccount.daily_limit
        )
        .order_by(
            EmailAccount.priority.desc(),
            EmailAccount.daily_sent_count.asc()
        )
        .all()
    )
    
    return accounts[0] if accounts else None
```

### 1.5 代码质量

#### 1.5.1 【强制】避免在finally块中使用return

说明：finally块中的return会覆盖try块中的return。

**反例**：
```python
def get_result():
    try:
        return "success"
    finally:
        return "finally"  # 会覆盖try中的返回值
```

**正例**：
```python
def get_result():
    result = None
    try:
        result = "success"
    except Exception as e:
        logger.error(f"错误: {e}")
    finally:
        # 清理资源
        cleanup()
    return result
```

#### 1.5.2 【强制】不要在循环中使用try...except，应该在循环外部使用

**反例**：
```python
for item in items:
    try:
        process(item)
    except Exception as e:
        logger.error(f"处理失败: {e}")
```

**正例**：
```python
try:
    for item in items:
        process(item)
except Exception as e:
    logger.error(f"处理失败: {e}")
```

**例外**：如果需要单独处理每个item的异常，可以在循环内使用try。

#### 1.5.3 【强制】禁止在代码中使用裸露的except

说明：捕获所有异常会隐藏错误。

**反例**：
```python
try:
    send_email()
except:  # 不指定异常类型
    pass
```

**正例**：
```python
try:
    send_email()
except SMTPException as e:
    logger.error(f"SMTP错误: {e}")
except Exception as e:
    logger.error(f"未知错误: {e}")
    raise
```

#### 1.5.4 【推荐】使用类型注解

**正例**：
```python
from typing import Optional, List, Dict

def send_email(
    recipient: str,
    subject: str,
    content: str,
    attachments: Optional[List[str]] = None
) -> Dict[str, any]:
    """发送邮件"""
    pass

def get_message(message_id: str) -> Optional[Dict]:
    """获取消息"""
    pass
```

#### 1.5.5 【推荐】及早返回，减少嵌套

**反例**：
```python
def process_message(message: dict) -> bool:
    if validate(message):
        if check_permission():
            if has_available_account():
                return send(message)
            else:
                return False
        else:
            return False
    else:
        return False
```

**正例**：
```python
def process_message(message: dict) -> bool:
    if not validate(message):
        return False
    
    if not check_permission():
        return False
    
    if not has_available_account():
        return False
    
    return send(message)
```

---

## 二、ORM规约（SQLAlchemy）

### 2.1 模型定义

#### 2.1.1 【强制】表名使用复数形式，采用snake_case命名

**正例**：
```python
class MessageRecord(Base):
    __tablename__ = "message_records"
    
    id = Column(BigInteger, primary_key=True)
    message_id = Column(String(64), unique=True, nullable=False)
```

#### 2.1.2 【强制】所有字段必须添加注释（comment参数）

**正例**：
```python
class EmailAccount(Base):
    __tablename__ = "email_accounts"
    
    id = Column(BigInteger, primary_key=True)
    email = Column(
        String(255), 
        unique=True, 
        nullable=False,
        comment="邮箱地址"
    )
    daily_limit = Column(
        Integer,
        default=500,
        comment="日发送上限"
    )
```

#### 2.1.3 【强制】必须定义created_at和updated_at字段

**正例**：
```python
from datetime import datetime

class MessageRecord(Base):
    __tablename__ = "message_records"
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="创建时间"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="更新时间"
    )
```

#### 2.1.4 【推荐】使用关系引用而不是直接使用外键ID

**正例**：
```python
class MessageRecord(Base):
    __tablename__ = "message_records"
    
    id = Column(BigInteger, primary_key=True)
    template_id = Column(BigInteger, ForeignKey("message_templates.id"))
    
    # 定义关系
    template = relationship("MessageTemplate", back_populates="messages")

class MessageTemplate(Base):
    __tablename__ = "message_templates"
    
    id = Column(BigInteger, primary_key=True)
    
    # 反向关系
    messages = relationship("MessageRecord", back_populates="template")
```

### 2.2 查询规约

#### 2.2.1 【强制】不要使用select *，明确指定需要的字段

**反例**：
```python
messages = db.query(MessageRecord).all()
```

**正例**：
```python
messages = (
    db.query(
        MessageRecord.id,
        MessageRecord.message_id,
        MessageRecord.status,
        MessageRecord.created_at
    )
    .all()
)
```

#### 2.2.2 【强制】禁止在循环中执行SQL查询（N+1问题）

**反例**：
```python
messages = db.query(MessageRecord).all()
for message in messages:
    # 每次循环都会查询数据库
    template = db.query(MessageTemplate).filter_by(
        id=message.template_id
    ).first()
```

**正例**：
```python
# 使用joinedload预加载关联数据
from sqlalchemy.orm import joinedload

messages = (
    db.query(MessageRecord)
    .options(joinedload(MessageRecord.template))
    .all()
)

for message in messages:
    # 直接访问关联对象，不会触发额外查询
    template = message.template
```

#### 2.2.3 【强制】使用参数化查询防止SQL注入

**反例**：
```python
# 危险！容易SQL注入
email = request.args.get("email")
query = f"SELECT * FROM email_accounts WHERE email = '{email}'"
db.execute(query)
```

**正例**：
```python
# 使用SQLAlchemy ORM（自动防注入）
email = request.args.get("email")
account = db.query(EmailAccount).filter_by(email=email).first()

# 或使用参数化查询
from sqlalchemy import text
result = db.execute(
    text("SELECT * FROM email_accounts WHERE email = :email"),
    {"email": email}
)
```

#### 2.2.4 【推荐】大量数据查询使用分页或游标

**正例**：
```python
def get_messages_paginated(page: int = 1, page_size: int = 20):
    """分页查询消息"""
    offset = (page - 1) * page_size
    messages = (
        db.query(MessageRecord)
        .order_by(MessageRecord.created_at.desc())
        .limit(page_size)
        .offset(offset)
        .all()
    )
    return messages

# 大数据量使用游标（yield_per）
def process_all_messages():
    """流式处理所有消息"""
    for message in db.query(MessageRecord).yield_per(1000):
        process(message)
```

---

## 三、异常处理规约

### 3.1 异常定义

#### 3.1.1 【强制】自定义异常类必须继承自Exception或其子类

**正例**：
```python
class NotificationException(Exception):
    """通知平台基础异常"""
    pass

class EmailSendException(NotificationException):
    """邮件发送异常"""
    pass

class NoAvailableAccountException(NotificationException):
    """无可用邮箱账户异常"""
    pass
```

#### 3.1.2 【强制】异常类命名使用Exception结尾

**正例**：
```python
class TemplateNotFoundException(NotificationException):
    """模板不存在异常"""
    pass

class RateLimitException(NotificationException):
    """频率限制异常"""
    pass
```

### 3.2 异常处理

#### 3.2.1 【强制】异常捕获后必须处理，不允许空捕获

**反例**：
```python
try:
    send_email()
except Exception:
    pass  # 空处理，隐藏了错误
```

**正例**：
```python
try:
    send_email()
except SMTPException as e:
    logger.error(f"SMTP错误: {e}", exc_info=True)
    raise EmailSendException(f"邮件发送失败: {e}")
```

#### 3.2.2 【强制】事务性操作必须正确处理异常和回滚

**正例**：
```python
from sqlalchemy.orm import Session

def create_message(db: Session, message_data: dict) -> MessageRecord:
    """创建消息记录（事务操作）"""
    try:
        message = MessageRecord(**message_data)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    except Exception as e:
        db.rollback()
        logger.error(f"创建消息失败: {e}")
        raise
    finally:
        db.close()
```

#### 3.2.3 【推荐】使用上下文管理器自动处理资源释放

**正例**：
```python
from contextlib import contextmanager

@contextmanager
def get_db_session():
    """数据库会话上下文管理器"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# 使用
with get_db_session() as db:
    message = db.query(MessageRecord).first()
```

---

## 四、日志规约

### 4.1 日志级别

#### 4.1.1 【强制】严格按照日志级别使用日志

- **DEBUG**：详细的调试信息（生产环境关闭）
- **INFO**：关键信息点记录
- **WARNING**：警告信息，不影响主流程
- **ERROR**：错误信息，影响功能但不影响系统
- **CRITICAL**：严重错误，系统无法继续运行

**正例**：
```python
from loguru import logger

# DEBUG - 调试信息
logger.debug(f"开始处理消息: {message_id}")

# INFO - 关键操作
logger.info(f"邮件发送成功: message_id={message_id}, recipient={recipient}")

# WARNING - 警告
logger.warning(f"邮箱{email}达到日发送上限，自动切换到下一个邮箱")

# ERROR - 错误
logger.error(f"邮件发送失败: {error_message}", exc_info=True)

# CRITICAL - 严重错误
logger.critical("数据库连接失败，系统无法启动")
```

### 4.2 日志内容

#### 4.2.1 【强制】生产环境禁止输出DEBUG日志

**配置示例**：
```python
import sys
from loguru import logger

# 移除默认handler
logger.remove()

# 生产环境配置
if settings.ENV == "production":
    logger.add(
        sys.stdout,
        level="INFO",  # 生产环境只记录INFO及以上
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    )
else:
    logger.add(
        sys.stdout,
        level="DEBUG",  # 开发环境记录DEBUG
        colorize=True
    )
```

#### 4.2.2 【强制】日志中必须包含request_id，便于追踪

**正例**：
```python
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

def log_with_request_id(message: str, level: str = "info"):
    """带request_id的日志"""
    request_id = request_id_var.get()
    getattr(logger, level)(f"[{request_id}] {message}")

# 使用
request_id_var.set("req_xyz789")
log_with_request_id("开始发送邮件", "info")
```

#### 4.2.3 【强制】敏感信息必须脱敏后记录

**正例**：
```python
def mask_email(email: str) -> str:
    """邮箱脱敏"""
    if "@" not in email:
        return "***"
    local, domain = email.split("@")
    return f"{local[0]}***@{domain}"

def mask_phone(phone: str) -> str:
    """手机号脱敏"""
    if len(phone) != 11:
        return "***"
    return f"{phone[:3]}****{phone[-4:]}"

# 使用
logger.info(f"发送邮件到: {mask_email('user@example.com')}")
logger.info(f"发送短信到: {mask_phone('13800138000')}")
```

#### 4.2.4 【推荐】使用结构化日志（JSON格式）

**正例**：
```python
import json

def log_structured(event: str, **kwargs):
    """结构化日志"""
    log_data = {
        "event": event,
        "request_id": request_id_var.get(),
        **kwargs
    }
    logger.info(json.dumps(log_data, ensure_ascii=False))

# 使用
log_structured(
    "email_sent",
    message_id="msg_123",
    recipient=mask_email("user@example.com"),
    duration_ms=150
)
```

---

## 五、单元测试规约

### 5.1 测试命名

#### 5.1.1 【强制】测试文件命名以test_开头

**正例**：
```
tests/
├── test_email_service.py
├── test_message_service.py
└── test_template_service.py
```

#### 5.1.2 【强制】测试类命名以Test开头

**正例**：
```python
class TestEmailService:
    """邮件服务测试类"""
    
    def test_send_email_success(self):
        """测试邮件发送成功场景"""
        pass
    
    def test_send_email_failed(self):
        """测试邮件发送失败场景"""
        pass
```

#### 5.1.3 【强制】测试方法命名以test_开头，清晰描述测试内容

**正例**：
```python
def test_select_email_account_by_priority(self):
    """测试按优先级选择邮箱账户"""
    pass

def test_email_pool_switches_when_limit_reached(self):
    """测试邮箱达到上限时自动切换"""
    pass
```

### 5.2 测试原则

#### 5.2.1 【强制】单元测试必须遵循AIR原则

- **A**utomatic（自动化）：测试用例通常是被持续集成工具自动执行
- **I**ndependent（独立性）：测试用例之间不能互相依赖
- **R**epeatable（可重复）：测试用例不受外部环境影响，能重复执行

#### 5.2.2 【强制】单元测试必须使用assert断言

**正例**：
```python
def test_generate_message_id():
    """测试生成消息ID"""
    message_id = generate_message_id()
    
    # 使用assert断言
    assert message_id is not None
    assert message_id.startswith("msg_")
    assert len(message_id) == 32
```

#### 5.2.3 【推荐】测试覆盖率不低于60%，核心功能不低于80%

**配置pytest-cov**：
```bash
pytest --cov=app --cov-report=html --cov-report=term
```

#### 5.2.4 【推荐】使用fixture管理测试数据

**正例**：
```python
import pytest

@pytest.fixture
def sample_message():
    """测试消息数据"""
    return {
        "to": "test@example.com",
        "subject": "测试邮件",
        "content": "<p>测试内容</p>"
    }

@pytest.fixture
def db_session():
    """数据库会话"""
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

def test_create_message(db_session, sample_message):
    """测试创建消息"""
    message = create_message(db_session, sample_message)
    assert message.id is not None
```

---

## 六、安全规约

### 6.1 数据安全

#### 6.1.1 【强制】敏感信息必须加密存储

**正例**：
```python
from cryptography.fernet import Fernet

class EncryptionService:
    """加密服务"""
    
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, plain_text: str) -> str:
        """加密"""
        return self.cipher.encrypt(plain_text.encode()).decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """解密"""
        return self.cipher.decrypt(encrypted_text.encode()).decode()

# 使用
encryption_service = EncryptionService(settings.ENCRYPTION_KEY)
encrypted_password = encryption_service.encrypt("smtp_password")
```

#### 6.1.2 【强制】密码必须使用单向哈希加密

**正例**：
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """密码哈希"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)
```

### 6.2 输入验证

#### 6.2.1 【强制】所有外部输入必须进行验证

**正例**：
```python
from pydantic import BaseModel, EmailStr, validator

class EmailSendRequest(BaseModel):
    """邮件发送请求"""
    to: EmailStr  # 自动验证邮箱格式
    subject: str
    content: str
    
    @validator("subject")
    def validate_subject(cls, v):
        """验证主题"""
        if not v or len(v) > 255:
            raise ValueError("邮件主题不能为空且不能超过255个字符")
        return v
    
    @validator("content")
    def validate_content(cls, v):
        """验证内容"""
        if not v:
            raise ValueError("邮件内容不能为空")
        # 防止XSS攻击
        return bleach.clean(v)
```

#### 6.2.2 【强制】文件上传必须验证文件类型和大小

**正例**：
```python
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".png", ".doc", ".docx", ".xls", ".xlsx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_upload_file(file: UploadFile):
    """验证上传文件"""
    # 验证文件扩展名
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型: {file_ext}"
        )
    
    # 验证文件大小
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"文件大小超过限制: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
    
    # 重置文件指针
    await file.seek(0)
    return True
```

---

## 七、工程结构规约

### 7.1 项目结构

#### 7.1.1 【强制】项目必须按照标准目录结构组织

**标准结构**：
```
notification-platform/
├── app/                        # 应用代码
│   ├── __init__.py
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置管理
│   ├── api/                    # API接口
│   │   ├── __init__.py
│   │   ├── v1/                 # API版本1
│   │   │   ├── __init__.py
│   │   │   ├── email.py        # 邮件接口
│   │   │   ├── template.py     # 模板接口
│   │   │   └── message.py      # 消息接口
│   │   └── deps.py             # 依赖项
│   ├── core/                   # 核心功能
│   │   ├── __init__.py
│   │   ├── security.py         # 安全相关
│   │   └── logging.py          # 日志配置
│   ├── models/                 # 数据库模型
│   │   ├── __init__.py
│   │   ├── message.py
│   │   ├── template.py
│   │   └── email_account.py
│   ├── schemas/                # Pydantic模型
│   │   ├── __init__.py
│   │   ├── message.py
│   │   └── template.py
│   ├── services/               # 业务逻辑
│   │   ├── __init__.py
│   │   ├── email_service.py
│   │   ├── template_service.py
│   │   └── message_service.py
│   ├── tasks/                  # Celery任务
│   │   ├── __init__.py
│   │   └── email_tasks.py
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── encryption.py
│       └── validators.py
├── tests/                      # 测试代码
│   ├── __init__.py
│   ├── conftest.py             # pytest配置
│   ├── test_email_service.py
│   └── test_template_service.py
├── docker/                     # Docker相关
│   ├── Dockerfile
│   └── docker-compose.yml
├── alembic/                    # 数据库迁移
│   ├── versions/
│   └── env.py
├── docs/                       # 文档
├── scripts/                    # 脚本
├── requirements.txt            # 依赖
├── .env.example                # 环境变量示例
├── .gitignore
├── README.md
└── pyproject.toml              # 项目配置
```

### 7.2 模块划分

#### 7.2.1 【强制】按照功能模块划分代码，避免大杂烩

说明：每个模块职责单一，便于维护。

#### 7.2.2 【推荐】使用依赖注入管理组件依赖

**正例**：
```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/email/send")
async def send_email(
    request: EmailSendRequest,
    db: Session = Depends(get_db),  # 依赖注入
    current_user: User = Depends(get_current_user)
):
    """发送邮件接口"""
    return email_service.send(db, request, current_user)
```

---

## 八、Git规约

### 8.1 分支管理

#### 8.1.1 【强制】必须使用Git Flow工作流

- `main`：主分支，生产环境代码
- `develop`：开发分支
- `feature/*`：功能分支
- `hotfix/*`：紧急修复分支
- `release/*`：发布分支

#### 8.1.2 【强制】分支命名规范

**正例**：
```
feature/email-pool-management
feature/message-deduplication
hotfix/fix-smtp-timeout
release/v1.0.0
```

### 8.2 提交规范

#### 8.2.1 【强制】提交信息必须遵循规范格式

**格式**：
```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型（type）**：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**正例**：
```
feat(email): 添加邮箱池自动切换功能

- 实现邮箱按优先级选择
- 实现邮箱达到上限自动切换
- 添加邮箱连续失败自动禁用功能

Closes #123
```

---

## 九、附录

### 9.1 代码检查工具配置

#### Black配置（pyproject.toml）
```toml
[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

#### Flake8配置（.flake8）
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,build,dist,.venv
ignore = E203, E266, E501, W503
max-complexity = 10
```

#### Pylint配置（.pylintrc）
```ini
[MASTER]
ignore=CVS,.git,__pycache__,.venv

[MESSAGES CONTROL]
disable=C0111,R0903,W0212

[FORMAT]
max-line-length=100
```

### 9.2 Pre-commit配置

**.pre-commit-config.yaml**：
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]
```

---

## 文档结束

本开发规范参考阿里巴巴开发手册、PEP 8、Google Python Style Guide制定，是消息通知平台项目的强制性规范。

所有开发人员必须严格遵守【强制】规约，建议遵守【推荐】规约，可参考【参考】规约。

**版本更新记录**：
- v1.0 (2025-10-24)：初始版本发布

