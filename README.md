# 消息通知平台服务

一个支持多渠道（邮件、微信、短信）的通用消息通知平台服务。

## 📋 功能特性

### 第一期（MVP - 当前版本）
- ✅ 邮件发送功能（支持邮箱池轮询和自动切换）
- ✅ 消息模板管理（基础功能，支持版本管理）
- ✅ 消息发送历史记录
- ✅ 消息发送失败重试机制
- ✅ 消息去重机制（防止重复发送）
- ✅ RESTful API接口（含健康检查）
- ✅ 基础的消息队列集成（RabbitMQ + Celery）
- ✅ API认证和鉴权（JWT Token）
- ✅ 基础监控指标暴露

### 第二期（规划中）
- 📅 短信发送功能（阿里云渠道）
- 📅 微信消息发送功能
- 📅 微信公众号消息发送功能
- 📅 定时/延迟发送功能
- 📅 管理后台界面
- 📅 消息统计分析功能

## 🏗️ 技术栈

- **Web框架**: FastAPI
- **数据库**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0
- **缓存**: Redis 7+
- **消息队列**: RabbitMQ 3.11+
- **任务队列**: Celery
- **部署**: Docker + Docker Compose

## 🚀 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.10+ (本地开发)

### 一键部署

```bash
# 1. 克隆项目
git clone <repository-url>
cd notification-platform

# 2. 复制配置文件
cp .env.example .env

# 3. 修改配置文件（重要！）
# 修改 .env 中的密码和密钥
vim .env

# 4. 启动所有服务
docker-compose up -d

# 5. 查看服务状态
docker-compose ps

# 6. 初始化数据库
docker-compose exec api alembic upgrade head

# 7. 创建API密钥
docker-compose exec api python scripts/create_api_key.py

# 8. 访问API文档
# 浏览器打开: http://localhost:8000/docs
```

### 本地开发

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements-dev.txt

# 3. 启动依赖服务（PostgreSQL, Redis, RabbitMQ）
docker-compose up -d postgres redis rabbitmq

# 4. 复制配置文件
cp .env.example .env

# 5. 运行数据库迁移
alembic upgrade head

# 6. 启动API服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. 启动Celery Worker（新终端）
celery -A app.tasks worker --loglevel=info

# 8. 启动Celery Beat（新终端）
celery -A app.tasks beat --loglevel=info
```

## 📚 文档

### 项目文档
- [项目状态](./doc/项目文档/PROJECT_STATUS.md) - 项目当前开发状态和进度
- [项目结构](./doc/项目文档/PROJECT_STRUCTURE.md) - 详细的项目目录结构说明
- [快速开始指南](./doc/项目文档/QUICKSTART.md) - 新手入门指南

### 需求与设计
- [需求文档](./doc/需求文档/需求文档-消息通知平台服务.md)
- [数据库设计](./doc/数据库设计/数据库设计文档-消息通知平台.md)
- [API接口文档](./doc/API接口/openapi.yaml)

### 开发与部署
- [开发规范](./doc/开发规范/Python开发规范手册-消息通知平台.md)
- [部署运维手册](./doc/部署运维/部署运维手册-消息通知平台.md)

### MCP工具
- [MCP工具使用指南](./doc/MCP插件/README.md) - AI增强工具配置和使用

## 🔧 配置说明

### 重要配置项

| 配置项 | 说明 | 示例 |
|--------|------|------|
| DATABASE_URL | 数据库连接 | postgresql://user:pass@localhost:5432/db |
| REDIS_URL | Redis连接 | redis://localhost:6379/0 |
| JWT_SECRET_KEY | JWT密钥 | 至少32位随机字符串 |
| ENCRYPTION_KEY | 加密密钥 | Fernet密钥（Base64） |

### 生成加密密钥

```python
# JWT密钥
import secrets
print(secrets.token_urlsafe(32))

# Fernet加密密钥
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 运行特定测试
pytest app/tests/test_email_service.py
```

## 📊 监控

- **健康检查**: http://localhost:8000/health
- **就绪检查**: http://localhost:8000/health/ready
- **存活检查**: http://localhost:8000/health/live
- **监控指标**: http://localhost:8000/metrics
- **API文档**: http://localhost:8000/docs
- **RabbitMQ管理**: http://localhost:15672 (admin/密码见.env)
- **Celery监控**: http://localhost:5555 (Flower)

## 🔐 API使用示例

### 1. 获取Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET"
  }'
```

### 2. 发送邮件

```bash
curl -X POST http://localhost:8000/api/v1/messages/email/send \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "测试邮件",
    "content": "<h1>Hello World</h1>"
  }'
```

### 3. 查询消息状态

```bash
curl -X GET "http://localhost:8000/api/v1/messages?status=success&page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📦 项目结构

```
notification-platform/
├── app/                    # 应用主目录
│   ├── api/               # API路由
│   │   └── v1/           # v1版本接口
│   ├── core/             # 核心配置
│   ├── models/           # 数据库模型
│   ├── schemas/          # Pydantic模型
│   ├── services/         # 业务服务层
│   ├── tasks/            # Celery任务
│   ├── utils/            # 工具函数
│   └── main.py           # 应用入口
├── docker/               # Docker配置
├── scripts/              # 工具脚本
├── doc/                  # 文档
├── logs/                 # 日志目录
├── backups/              # 备份目录
├── .env.example          # 环境变量示例
├── requirements.txt      # 生产依赖
├── requirements-dev.txt  # 开发依赖
└── docker-compose.yml    # Docker编排
```

## 🤝 贡献指南

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📄 许可证

MIT License

## 👥 联系方式

- 邮箱: support@example.com
- 文档: https://docs.example.com
- Issue: https://github.com/your-org/notification-platform/issues

