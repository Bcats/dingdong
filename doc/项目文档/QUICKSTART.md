# 快速开始指南

本指南将帮助你快速部署和使用消息通知平台服务。

## 📋 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- Git

## 🚀 一键部署

### 1. 克隆项目

```bash
git clone <repository-url>
cd notification-platform
```

### 2. 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件（重要！）
vim .env
```

**必须修改的配置项**：

```env
# 数据库密码
DB_PASSWORD=your_secure_password

# RabbitMQ密码
RABBITMQ_PASSWORD=your_rabbitmq_password

# JWT密钥（至少32位）
JWT_SECRET_KEY=your_jwt_secret_key_at_least_32_chars

# 加密密钥（使用下面的命令生成）
ENCRYPTION_KEY=your_encryption_key_base64_encoded
```

**生成加密密钥**：

```python
# 运行Python生成Fernet密钥
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. 启动所有服务

```bash
# 启动
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 初始化数据库

```bash
# 运行数据库迁移
docker-compose exec api alembic upgrade head

# 验证迁移
docker-compose exec api alembic current
```

### 5. 创建API密钥

```bash
docker-compose exec api python scripts/create_api_key.py \
  --name "我的第一个密钥" \
  --description "用于测试"
```

**输出示例**：
```
================================================================================
🎉 API密钥创建成功！
================================================================================
ID: 1
名称: 我的第一个密钥
描述: 用于测试
创建时间: 2025-10-25 12:00:00
过期时间: 永不过期
================================================================================
⚠️  请妥善保管以下信息，API Secret只显示一次！
================================================================================
API Key:    noti_abc123def456...
API Secret: secret_xyz789...
================================================================================
```

**⚠️ 重要**：请立即保存API Key和API Secret，Secret只显示一次！

### 6. 添加邮箱账户

```bash
docker-compose exec api python scripts/add_email_account.py \
  --email noreply@example.com \
  --smtp-host smtp.example.com \
  --smtp-port 465 \
  --smtp-username noreply@example.com \
  --smtp-password your_email_password \
  --display-name "系统通知" \
  --daily-limit 500 \
  --priority 10
```

### 7. 验证部署

访问以下URL验证服务是否正常：

- **健康检查**: http://localhost:8000/health
- **API文档**: http://localhost:8000/docs
- **RabbitMQ管理界面**: http://localhost:15672 (admin/你的密码)
- **Celery监控**: http://localhost:5555

## 📝 快速使用

### 1. 获取访问令牌

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "noti_abc123def456...",
    "api_secret": "secret_xyz789..."
  }'
```

**响应**：
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

### 2. 发送邮件

```bash
# 将TOKEN替换为上一步获取的access_token
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST http://localhost:8000/api/v1/messages/email/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["user@example.com"],
    "subject": "测试邮件",
    "content": "<h1>你好！</h1><p>这是一封测试邮件。</p>"
  }'
```

**响应**：
```json
{
  "code": 0,
  "message": "Message queued for sending",
  "data": {
    "message_id": 1,
    "status": "pending",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### 3. 查询消息状态

```bash
# 查询单个消息
curl -X GET "http://localhost:8000/api/v1/messages/1" \
  -H "Authorization: Bearer $TOKEN"

# 查询消息列表
curl -X GET "http://localhost:8000/api/v1/messages?status=success&page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. 使用模板发送

**创建模板**：
```bash
curl -X POST http://localhost:8000/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "welcome_email",
    "name": "欢迎邮件",
    "type": "email",
    "subject_template": "欢迎{{name}}加入我们！",
    "content_template": "<h1>你好，{{name}}！</h1><p>欢迎加入{{company}}。</p>",
    "variables": {
      "name": {"type": "string", "required": true, "description": "用户名"},
      "company": {"type": "string", "required": true, "description": "公司名"}
    }
  }'
```

**使用模板发送**：
```bash
curl -X POST http://localhost:8000/api/v1/messages/email/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["user@example.com"],
    "template_code": "welcome_email",
    "template_variables": {
      "name": "张三",
      "company": "示例公司"
    }
  }'
```

## 🔧 常用命令

### 查看日志
```bash
# 所有服务
docker-compose logs -f

# 特定服务
docker-compose logs -f api
docker-compose logs -f celery-worker
```

### 重启服务
```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart api
```

### 停止服务
```bash
docker-compose down
```

### 数据库备份
```bash
docker-compose exec postgres pg_dump -U notification_user notification_db > backup.sql
```

### 查看Celery任务
```bash
# 查看worker状态
docker-compose exec celery-worker celery -A app.tasks.celery_app inspect active

# 查看定时任务
docker-compose exec celery-beat celery -A app.tasks.celery_app inspect scheduled
```

## 🐛 故障排查

### 服务无法启动

1. 检查端口占用
```bash
netstat -tulpn | grep -E '8000|5432|6379|5672|15672'
```

2. 查看日志
```bash
docker-compose logs api
```

### 邮件发送失败

1. 检查邮箱配置
```bash
docker-compose exec postgres psql -U notification_user -d notification_db -c "SELECT * FROM email_accounts;"
```

2. 查看Worker日志
```bash
docker-compose logs celery-worker
```

3. 测试SMTP连接
```bash
docker-compose exec api python -c "
import smtplib
server = smtplib.SMTP_SSL('smtp.example.com', 465)
server.login('user@example.com', 'password')
print('SMTP连接成功')
server.quit()
"
```

### 数据库连接失败

```bash
# 检查数据库状态
docker-compose ps postgres

# 手动连接测试
docker-compose exec postgres psql -U notification_user -d notification_db
```

## 📚 更多文档

- [完整README](./README.md)
- [需求文档](./doc/需求文档/需求文档-消息通知平台服务.md)
- [开发规范](./doc/开发规范/Python开发规范手册-消息通知平台.md)
- [数据库设计](./doc/数据库设计/数据库设计文档-消息通知平台.md)
- [API接口文档](./doc/API接口/openapi.yaml)
- [部署运维手册](./doc/部署运维/部署运维手册-消息通知平台.md)

## 💬 获取帮助

- 查看API文档: http://localhost:8000/docs
- 查看日志: `docker-compose logs -f`
- 提交Issue: <repository-url>/issues

---

祝你使用愉快！🎉

