# 项目结构说明

## 📁 目录结构

```
notification-platform/
├── app/                          # 应用主目录
│   ├── __init__.py
│   ├── main.py                   # FastAPI应用入口
│   │
│   ├── api/                      # API路由
│   │   ├── __init__.py
│   │   ├── dependencies.py       # API依赖项（认证等）
│   │   └── v1/                   # API v1版本
│   │       ├── __init__.py
│   │       ├── health.py         # 健康检查
│   │       ├── auth.py           # 认证接口
│   │       ├── messages.py       # 消息接口
│   │       └── templates.py      # 模板接口
│   │
│   ├── core/                     # 核心模块
│   │   ├── __init__.py
│   │   ├── config.py             # 配置管理
│   │   ├── database.py           # 数据库连接
│   │   ├── logger.py             # 日志配置
│   │   └── security.py           # 安全功能（加密、JWT等）
│   │
│   ├── models/                   # 数据库模型（SQLAlchemy）
│   │   ├── __init__.py
│   │   ├── base.py               # 基础模型类
│   │   ├── message.py            # 消息记录模型
│   │   ├── template.py           # 模板模型
│   │   ├── email.py              # 邮件账户/附件模型
│   │   └── api_key.py            # API密钥模型
│   │
│   ├── schemas/                  # Pydantic数据模型
│   │   ├── __init__.py
│   │   ├── common.py             # 通用Schema
│   │   ├── auth.py               # 认证Schema
│   │   ├── message.py            # 消息Schema
│   │   └── template.py           # 模板Schema
│   │
│   ├── services/                 # 业务服务层
│   │   ├── __init__.py
│   │   ├── email_service.py      # 邮件发送服务
│   │   ├── template_service.py   # 模板服务
│   │   └── message_service.py    # 消息服务
│   │
│   ├── tasks/                    # Celery异步任务
│   │   ├── __init__.py
│   │   ├── celery_app.py         # Celery应用配置
│   │   ├── email_tasks.py        # 邮件发送任务
│   │   └── scheduled_tasks.py    # 定时任务
│   │
│   ├── utils/                    # 工具函数
│   │   ├── __init__.py
│   │   └── redis_client.py       # Redis客户端封装
│   │
│   └── tests/                    # 测试文件
│       ├── __init__.py
│       ├── conftest.py           # Pytest配置
│       ├── test_health.py        # 健康检查测试
│       └── test_auth.py          # 认证测试
│
├── docker/                       # Docker相关文件
│   └── Dockerfile                # 生产环境Dockerfile
│
├── scripts/                      # 工具脚本
│   ├── create_api_key.py         # 创建API密钥
│   ├── add_email_account.py      # 添加邮箱账户
│   └── init_db.py                # 初始化数据库
│
├── alembic/                      # 数据库迁移
│   ├── versions/                 # 迁移版本文件
│   ├── env.py                    # Alembic环境配置
│   └── script.py.mako            # 迁移模板
│
├── doc/                          # 文档目录
│   ├── 需求文档/
│   ├── 开发规范/
│   ├── 数据库设计/
│   ├── API接口/
│   └── 部署运维/
│
├── logs/                         # 日志目录（运行时生成）
├── backups/                      # 备份目录
│
├── .env                          # 环境变量配置（需创建）
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git忽略文件
├── .dockerignore                 # Docker忽略文件
├── .pre-commit-config.yaml       # Pre-commit配置
│
├── alembic.ini                   # Alembic配置
├── docker-compose.yml            # Docker Compose配置
├── Dockerfile                    # Dockerfile
├── pytest.ini                    # Pytest配置
├── Makefile                      # Make命令
│
├── requirements.txt              # 生产依赖
├── requirements-dev.txt          # 开发依赖
│
├── README.md                     # 项目README
├── QUICKSTART.md                 # 快速开始指南
└── PROJECT_STRUCTURE.md          # 本文件
```

## 🏗️ 架构设计

### 分层架构

```
┌─────────────────────────────────────────┐
│          API Layer (FastAPI)            │
│  - 路由 (routers)                       │
│  - 依赖注入 (dependencies)              │
│  - 数据验证 (Pydantic schemas)          │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│        Service Layer (Business)         │
│  - 业务逻辑                             │
│  - 服务编排                             │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      Data Layer (Models & Database)     │
│  - SQLAlchemy模型                       │
│  - 数据库操作                           │
└─────────────────────────────────────────┘
```

### 核心组件

1. **FastAPI应用** (`app/main.py`)
   - HTTP服务器
   - 路由管理
   - 中间件
   - 异常处理

2. **Celery Worker** (`app/tasks/`)
   - 异步任务处理
   - 邮件发送
   - 定时任务

3. **数据库** (PostgreSQL)
   - 持久化存储
   - 事务管理

4. **缓存** (Redis)
   - 消息去重
   - 会话存储

5. **消息队列** (RabbitMQ)
   - 任务队列
   - 消息传递

## 📝 代码规范

### 导入顺序
1. 标准库
2. 第三方库
3. 本地模块

### 命名规范
- 类名：PascalCase (`EmailService`)
- 函数/变量：snake_case (`send_email`)
- 常量：UPPER_CASE (`MAX_RETRY_COUNT`)
- 私有成员：`_private_method`

### 文档字符串
```python
def function(arg1: str, arg2: int) -> bool:
    """
    函数简述
    
    Args:
        arg1: 参数1说明
        arg2: 参数2说明
        
    Returns:
        bool: 返回值说明
        
    Raises:
        ValueError: 异常说明
    """
    pass
```

## 🔄 数据流

### 邮件发送流程
```
API请求 → 认证 → 数据验证 → 创建消息记录 → 
发送到队列 → Celery Worker → 邮箱池选择 → 
SMTP发送 → 更新状态 → 返回结果
```

### 模板渲染流程
```
API请求 → 获取模板 → Jinja2渲染 → 
生成内容 → 创建消息 → 发送
```

## 🛠️ 开发工作流

### 本地开发
```bash
# 1. 安装依赖
pip install -r requirements-dev.txt

# 2. 启动依赖服务
docker-compose up -d postgres redis rabbitmq

# 3. 运行迁移
alembic upgrade head

# 4. 启动API
uvicorn app.main:app --reload

# 5. 启动Worker（新终端）
celery -A app.tasks worker --loglevel=info

# 6. 启动Beat（新终端）
celery -A app.tasks beat --loglevel=info
```

### 添加新功能
1. 创建数据库模型 (`models/`)
2. 创建Pydantic Schema (`schemas/`)
3. 实现业务逻辑 (`services/`)
4. 创建API路由 (`api/v1/`)
5. 编写测试 (`tests/`)
6. 更新文档

### 数据库变更
```bash
# 1. 修改模型
vim app/models/xxx.py

# 2. 生成迁移
alembic revision --autogenerate -m "描述"

# 3. 应用迁移
alembic upgrade head

# 4. 回滚（如需要）
alembic downgrade -1
```

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest app/tests/test_auth.py

# 生成覆盖率报告
pytest --cov=app --cov-report=html
```

## 📊 监控

- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **Prometheus指标**: http://localhost:8000/metrics
- **RabbitMQ管理**: http://localhost:15672
- **Flower监控**: http://localhost:5555

## 🔒 安全

1. **环境变量**：敏感信息存储在`.env`
2. **密码加密**：使用bcrypt哈希
3. **数据加密**：使用Fernet对称加密
4. **JWT认证**：基于API Key/Secret
5. **日志脱敏**：敏感字段自动脱敏

## 📦 部署

详见 [部署运维手册](./doc/部署运维/部署运维手册-消息通知平台.md)

---

更多信息请参考项目文档目录。

