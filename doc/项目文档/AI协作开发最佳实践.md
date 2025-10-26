# AI 协作开发最佳实践

**版本**: v1.0  
**日期**: 2025-10-26  
**适用场景**: 使用 AI 助手进行软件开发项目

---

## 📖 目录

1. [项目启动阶段](#1-项目启动阶段)
2. [需求沟通技巧](#2-需求沟通技巧)
3. [开发协作流程](#3-开发协作流程)
4. [问题反馈方式](#4-问题反馈方式)
5. [代码审查要点](#5-代码审查要点)
6. [文档管理策略](#6-文档管理策略)
7. [Git 工作流程](#7-git-工作流程)
8. [工具使用建议](#8-工具使用建议)
9. [常见问题 FAQ](#9-常见问题-faq)
10. [检查清单](#10-检查清单)

---

## 1. 项目启动阶段

### 1.1 接手现有项目

#### ✅ 推荐做法

**第一步：提供项目概览**
```
"这是一个消息通知平台项目，使用 FastAPI + Vue3 开发。
项目目录结构如下：[贴出主要目录]
当前遇到的问题是：[具体问题描述]"
```

**第二步：说明当前状态**
- 项目运行状态（能否启动、有什么报错）
- 已完成的功能列表
- 待开发的功能列表
- 技术栈版本信息

**第三步：明确目标**
```
"我希望你帮我：
1. 修复当前的 XXX 问题
2. 实现 XXX 新功能
3. 优化 XXX 性能"
```

#### ❌ 避免的做法

- ❌ 直接问："帮我看看这个项目"（太宽泛）
- ❌ 不提供项目背景就报错误（缺少上下文）
- ❌ 一次性提出太多不相关的需求

#### 📝 示例：好的项目介绍

```markdown
## 项目背景
这是一个邮件通知平台，基于 Python FastAPI 和 Vue3 开发。

## 技术栈
- 后端：FastAPI 0.104、SQLAlchemy、PostgreSQL
- 前端：Vue3、TypeScript、Element Plus
- 部署：Docker、Docker Compose

## 当前状态
- ✅ 基础架构已搭建
- ✅ 用户认证已完成
- 🔨 消息管理模块开发中
- ❌ 邮件发送功能有bug

## 当前问题
运行 `docker-compose up` 后，数据库连接失败，错误信息：
[粘贴完整错误日志]

## 期望目标
1. 修复数据库连接问题
2. 完成消息管理的增删改查
3. 实现邮件发送的重试机制
```

---

### 1.2 启动新项目

#### ✅ 推荐做法

**第一步：提供详细需求文档**
```
"我要开发一个 XXX 系统，主要功能包括：
1. [功能1的详细描述]
2. [功能2的详细描述]
3. [功能3的详细描述]

技术栈要求：
- 后端：Python / Node.js / Java
- 前端：Vue / React / Angular
- 数据库：PostgreSQL / MySQL / MongoDB

非功能性需求：
- 需要支持 10000+ 用户
- 响应时间 < 200ms
- 需要Docker部署"
```

**第二步：分阶段开发**
```
"我们分阶段开发：
第一阶段：搭建基础架构
第二阶段：实现核心功能
第三阶段：完善周边功能
第四阶段：优化和部署"
```

#### 📝 示例：好的新项目需求

参考本项目的 `doc/需求文档/需求文档-消息通知平台服务.md`

---

## 2. 需求沟通技巧

### 2.1 描述功能需求

#### ✅ 清晰的需求描述

**使用 "用户故事" 格式**
```
作为 [角色]，
我希望 [功能]，
以便 [目的]。

示例：
作为管理员，
我希望能够查看所有邮件发送记录，
以便监控系统运行状态和排查问题。
```

**提供具体场景**
```
场景1：用户点击"发送"按钮
  - 系统验证表单数据
  - 显示加载状态
  - 调用后端API
  - 成功：显示成功提示，跳转到列表页
  - 失败：显示错误信息，保持在当前页

场景2：用户上传附件
  - 限制文件大小 < 10MB
  - 限制文件类型：pdf, doc, jpg, png
  - 显示上传进度
  - 支持多文件上传
```

**说明预期结果**
```
期望效果：
- UI：参考 Element Plus 的 Table 组件样式
- 交互：点击行展开详情，类似折叠面板
- 性能：列表加载时间 < 1秒（1000条数据）
```

#### ❌ 模糊的需求描述

- ❌ "做一个好看的界面"（什么是好看？）
- ❌ "优化一下性能"（优化什么？目标是什么？）
- ❌ "参考某某网站"（需要具体说明参考哪个功能）

---

### 2.2 报告错误问题

#### ✅ 完整的错误报告

**使用结构化格式**
```markdown
## 问题描述
[一句话概括问题]

## 复现步骤
1. 打开管理后台
2. 点击"消息管理"
3. 点击"导出数据"按钮

## 预期结果
下载一个包含所有消息记录的CSV文件

## 实际结果
浏览器控制台报错：500 Internal Server Error

## 错误信息
[粘贴完整的错误堆栈]
request.ts:101 GET http://localhost:8080/api/v1/messages?page=1&page_size=10000 500
...

## 环境信息
- 浏览器：Chrome 120.0
- 操作系统：Windows 11
- 项目版本：main 分支
- 服务状态：所有 Docker 容器正常运行

## 截图
[如果有UI问题，提供截图]
```

#### ❌ 不完整的错误报告

- ❌ "报错了"（什么报错？在哪里？）
- ❌ "不work"（什么不work？具体现象？）
- ❌ 只提供错误信息，不说明操作步骤

---

### 2.3 提出优化需求

#### ✅ 明确的优化目标

```markdown
## 当前问题
邮箱管理列表页，操作按钮（编辑、删除、测试）之间间距太小，
容易误点，特别是在小屏幕设备上。

## 优化建议
1. 增加按钮之间的间距（至少8px）
2. 添加按钮图标，提高可识别性
3. 在移动端改为下拉菜单展示

## 期望效果
- 桌面端：按钮横向排列，间距8-10px
- 移动端：使用更多操作下拉菜单
- 参考：Element Plus 的 Dropdown 组件
```

#### 📊 量化的性能目标

```
当前性能：
- 列表加载时间：3秒（1000条数据）
- 首屏渲染时间：1.5秒
- API响应时间：800ms

优化目标：
- 列表加载时间：< 1秒
- 首屏渲染时间：< 500ms
- API响应时间：< 200ms

优化方向：
- 后端：添加数据库索引、分页查询
- 前端：虚拟滚动、懒加载
- 缓存：Redis缓存热点数据
```

---

## 3. 开发协作流程

### 3.1 功能开发流程

#### 标准流程

```
1. 需求确认
   ↓
2. 技术方案讨论（如果是复杂功能）
   ↓
3. AI 生成代码
   ↓
4. 人工审查代码
   ↓
5. 测试验证
   ↓
6. 反馈调整（如有问题）
   ↓
7. 确认完成
```

#### 📝 实际示例

**第1步：需求确认**
```
用户："我需要在消息管理页面添加批量删除功能"
```

**第2步：技术方案**（可选，复杂功能需要）
```
AI："建议实现方案：
1. 前端：使用 el-table 的 selection 实现多选
2. 后端：新增 DELETE /api/v1/messages/batch 接口
3. 需要确认删除提示
4. 删除后刷新列表

你觉得这个方案可以吗？需要调整吗？"

用户："可以，但希望删除是软删除，不是物理删除"
```

**第3步：AI生成代码**
（AI开始实现代码）

**第4步：人工审查**
```
用户查看生成的代码，检查：
- 逻辑是否正确
- 是否有安全问题
- UI交互是否符合预期
```

**第5步：测试验证**
```
用户："实现后我测试发现，删除时没有加载提示"
```

**第6步：反馈调整**
（AI修复问题）

**第7步：确认完成**
```
用户："现在可以了，功能正常"
```

---

### 3.2 迭代开发策略

#### ✅ 推荐：小步快跑

```
第一次对话：实现基础功能
  └─ "先实现基本的列表展示和单条删除"

第二次对话：添加批量操作
  └─ "现在添加批量删除功能"

第三次对话：优化交互
  └─ "优化删除时的加载状态和错误提示"

第四次对话：完善细节
  └─ "添加删除成功后的提示音效"
```

#### ❌ 避免：一次性要求所有功能

```
❌ "帮我实现消息管理的所有功能：列表、详情、创建、编辑、
    删除、批量操作、导出、导入、筛选、排序、分页、
    权限控制、操作日志..."
```

**问题**：
- 一次性生成太多代码，难以审查
- 出现问题难以定位
- 可能有些需求理解不一致

---

### 3.3 代码审查要点

#### 前端代码审查清单

```typescript
// ✅ 检查点1：是否有类型定义
interface Message {
  id: number
  subject: string
  // ...
}

// ✅ 检查点2：是否有错误处理
try {
  await api.deleteMessage(id)
  ElMessage.success('删除成功')
} catch (error) {
  ElMessage.error('删除失败')
}

// ✅ 检查点3：是否有加载状态
const loading = ref(false)
loading.value = true
await fetchData()
loading.value = false

// ✅ 检查点4：是否有表单验证
const rules = {
  email: [
    { required: true, message: '请输入邮箱' },
    { type: 'email', message: '邮箱格式不正确' }
  ]
}

// ✅ 检查点5：是否有权限控制
if (hasPermission('message:delete')) {
  // 显示删除按钮
}
```

#### 后端代码审查清单

```python
# ✅ 检查点1：是否有参数验证
@router.delete("/messages/{id}")
async def delete_message(
    id: int = Path(..., gt=0),  # 验证ID > 0
    db: Session = Depends(get_db)
):
    ...

# ✅ 检查点2：是否有权限检查
current_user = get_current_user()
if not current_user.is_admin:
    raise HTTPException(403, "无权限")

# ✅ 检查点3：是否有异常处理
try:
    message = db.query(Message).filter_by(id=id).first()
    if not message:
        raise HTTPException(404, "消息不存在")
except Exception as e:
    logger.error(f"删除消息失败: {e}")
    raise HTTPException(500, "删除失败")

# ✅ 检查点4：是否有SQL注入防护
# 使用ORM而不是字符串拼接SQL
db.query(Message).filter(Message.id == id)  # ✅
# db.execute(f"DELETE FROM messages WHERE id = {id}")  # ❌

# ✅ 检查点5：是否有日志记录
logger.info(f"用户 {current_user.id} 删除了消息 {id}")
```

---

## 4. 问题反馈方式

### 4.1 遇到报错时

#### ✅ 标准反馈格式

```markdown
**问题类型**：[运行时错误 / 编译错误 / 逻辑错误 / UI显示问题]

**问题描述**：
点击开始测试按钮时，弹出提示"测试失败"

**错误信息**：
[粘贴完整的错误堆栈或控制台输出]
```
request.ts:101 GET http://localhost:8080/api/v1/test 500
Error: Request failed with status code 500
...
```

**复现步骤**：
1. 打开邮箱管理页面
2. 点击某个邮箱的"测试"按钮
3. 在弹窗中选择"发送测试邮件"
4. 输入收件人邮箱
5. 点击"开始测试"

**期望行为**：
应该显示测试成功提示，并发送一封测试邮件

**实际行为**：
显示"测试失败"，没有发送邮件

**相关代码**（如果知道问题可能在哪）：
admin-frontend/src/views/EmailAccounts/Index.vue 的 handleTestSubmit 函数
```

#### 🔍 如何获取完整错误信息

**浏览器控制台**
```
1. 按 F12 打开开发者工具
2. 切换到 Console 标签
3. 复制所有红色错误信息
4. 切换到 Network 标签，查看失败的请求详情
```

**后端日志**
```bash
# Docker环境
docker-compose logs api

# 查看实时日志
docker-compose logs -f api

# 查看最近100行
docker-compose logs --tail=100 api
```

**Python错误堆栈**
```
完整复制错误信息，包括：
- Traceback (最后一次调用)
- File路径和行号
- 错误类型和错误消息
```

---

### 4.2 功能不符合预期时

#### ✅ 清晰的对比说明

```markdown
## 功能：消息重试按钮

### 期望行为
1. 点击重试按钮
2. 显示确认对话框："确定要重试这条消息吗？"
3. 点击确定后，显示加载状态
4. 重试成功：提示"重试成功，消息已重新发送"
5. 重试失败：提示具体错误原因

### 实际行为
1. 点击重试按钮 ✅
2. 没有确认对话框 ❌（直接重试了）
3. 没有加载状态 ❌
4. 重试后显示英文错误"Maximum retry attempts (3) reached" ❌

### 需要调整
1. 添加确认对话框
2. 添加加载状态（禁用按钮 + 显示loading图标）
3. 错误信息改为中文
4. 如果已达到最大重试次数，按钮文字改为"强制重试"
```

#### 📸 使用截图对比

```markdown
期望效果：[贴图1 - 设计稿或参考页面]
实际效果：[贴图2 - 当前页面截图]
问题标注：[贴图3 - 在截图上标注问题]
```

---

### 4.3 性能问题反馈

#### ✅ 提供性能数据

```markdown
## 性能问题：消息列表加载缓慢

### 测试环境
- 数据量：1000条消息
- 浏览器：Chrome 120.0
- 网络：本地环境（Docker）

### 性能数据
使用 Chrome DevTools Performance 录制：

1. 页面加载时间：3.2秒
   - API请求时间：2.8秒
   - 数据渲染时间：0.4秒

2. API响应分析（Network标签）：
   - 请求URL：GET /api/v1/messages?page=1&page_size=1000
   - 响应时间：2843ms
   - 响应大小：1.2MB

3. 后端日志显示：
   - 数据库查询时间：2.5秒

### 优化建议
1. 添加数据库索引（created_at, status字段）
2. 减小默认page_size（改为100）
3. 前端使用虚拟滚动
4. 添加Redis缓存

### 期望目标
- 页面加载时间 < 1秒
- API响应时间 < 500ms
```

---

## 5. 代码审查要点

### 5.1 安全性检查

#### 🔒 常见安全问题

```python
# ❌ SQL注入风险
query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)

# ✅ 使用参数化查询
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))

# ❌ XSS风险（前端）
<div v-html="userInput"></div>

# ✅ 转义用户输入
<div>{{ userInput }}</div>

# ❌ 明文存储密码
user.password = request.password

# ✅ 哈希存储
user.password = bcrypt.hash(request.password)

# ❌ 缺少权限检查
@router.delete("/users/{id}")
def delete_user(id: int):
    # 任何人都能删除？

# ✅ 添加权限检查
@router.delete("/users/{id}")
def delete_user(id: int, current_user: User = Depends(get_current_admin)):
    if not current_user.is_admin:
        raise HTTPException(403, "无权限")
```

---

### 5.2 性能检查

#### ⚡ 常见性能问题

```python
# ❌ N+1查询问题
messages = db.query(Message).all()
for msg in messages:
    msg.sender = db.query(User).filter_by(id=msg.sender_id).first()

# ✅ 使用JOIN
messages = db.query(Message).join(User).all()

# ❌ 一次性加载大量数据
messages = db.query(Message).all()  # 10万条数据

# ✅ 分页加载
messages = db.query(Message).limit(100).offset(page * 100).all()

# ❌ 前端渲染大列表
<div v-for="item in 10000Items">{{ item }}</div>

# ✅ 使用虚拟滚动
<virtual-list :items="items" :item-height="50" />
```

---

### 5.3 代码质量检查

#### 📝 代码可读性

```python
# ❌ 缺少注释和文档
def process(data):
    result = []
    for item in data:
        if item.status == 1:
            result.append(item)
    return result

# ✅ 清晰的命名和注释
def get_active_messages(messages: List[Message]) -> List[Message]:
    """
    筛选出状态为"活跃"的消息
    
    Args:
        messages: 消息列表
        
    Returns:
        活跃状态的消息列表
    """
    return [msg for msg in messages if msg.status == MessageStatus.ACTIVE]
```

#### 🧪 测试覆盖

```python
# ✅ 关键功能应该有测试
def test_delete_message():
    # 准备数据
    message = create_test_message()
    
    # 执行删除
    response = client.delete(f"/api/v1/messages/{message.id}")
    
    # 验证结果
    assert response.status_code == 200
    assert db.query(Message).filter_by(id=message.id).first() is None
```

---

## 6. 文档管理策略

### 6.1 文档类型

#### 必备文档

```
项目根目录/
├── README.md                    ✅ 项目介绍和快速开始
├── .env.example                 ✅ 环境变量模板
├── doc/
│   ├── 需求文档/                ✅ 功能需求说明
│   ├── 开发规范/                ✅ 编码规范和最佳实践
│   ├── 数据库设计/              ✅ 数据库表结构
│   ├── API接口/                 ✅ API文档（OpenAPI）
│   ├── 用户指南/                ✅ 使用说明
│   ├── 部署运维/                ✅ 部署和运维手册
│   └── 项目文档/
│       ├── PROJECT_STATUS.md    ✅ 项目当前状态
│       └── 开发日志/            📝 开发过程记录
```

---

### 6.2 文档更新时机

#### ✅ 何时更新文档

```
1. 添加新功能时
   → 更新需求文档、API文档、用户指南

2. 修改数据库结构时
   → 更新数据库设计文档、运行迁移脚本

3. 修复重要bug时
   → 记录到开发日志，更新FAQ

4. 完成一个里程碑时
   → 更新 PROJECT_STATUS.md

5. 修改配置项时
   → 更新 .env.example 和部署文档
```

#### 📝 文档更新请求示例

```
"我刚才实现了消息重试功能，请帮我：
1. 更新 API 文档，添加 POST /api/v1/messages/{id}/retry 接口说明
2. 更新用户指南，说明如何使用重试功能
3. 更新 PROJECT_STATUS.md，标记此功能为已完成"
```

---

### 6.3 文档整理策略

#### 🗂️ 定期整理

```
每个开发阶段结束后：

1. 整理临时文档
   - 将开发过程中的临时报告移到"历史文档"
   - 保留核心文档在主目录

2. 更新项目状态
   - 更新功能完成度
   - 更新已知问题列表
   - 更新下一步计划

3. 清理过期信息
   - 删除已解决的问题记录
   - 删除过期的方案文档
```

---

## 7. Git 工作流程

### 7.1 提交规范

#### ✅ 使用约定式提交

```bash
# 格式
<type>(<scope>): <subject>

<body>

<footer>

# 类型（type）
feat:     新功能
fix:      修复bug
docs:     文档更新
style:    代码格式（不影响功能）
refactor: 重构
perf:     性能优化
test:     测试相关
chore:    构建/工具相关

# 示例
feat(message): 添加消息批量删除功能

- 前端添加多选框
- 后端添加批量删除API
- 添加确认提示

Closes #123
```

#### 📝 好的提交信息示例

```bash
# ✅ 清晰明确
feat: 添加邮箱测试功能，支持发送测试邮件

# ✅ 说明改动范围
fix(auth): 修复JWT token过期时间配置错误

# ✅ 包含必要上下文
refactor: 重构消息查询逻辑，优化性能
- 添加数据库索引
- 使用分页查询
- 添加Redis缓存
查询时间从3秒降低到300ms

# ❌ 太简单
fix: bug修复

# ❌ 太随意
update: 改了一些东西
```

---

### 7.2 分支管理

#### 🌿 推荐的分支策略

```
main
  ├── develop              # 开发分支
  │   ├── feature/xxx     # 功能分支
  │   ├── feature/yyy
  │   └── ...
  └── hotfix/xxx          # 紧急修复分支
```

#### 📋 工作流程

```bash
# 1. 从 develop 创建功能分支
git checkout develop
git checkout -b feature/message-batch-delete

# 2. 开发功能（多次提交）
git add .
git commit -m "feat: 添加批量删除UI"
git commit -m "feat: 实现批量删除API"

# 3. 合并到 develop
git checkout develop
git merge feature/message-batch-delete

# 4. 删除功能分支
git branch -d feature/message-batch-delete

# 5. develop 测试通过后，合并到 main
git checkout main
git merge develop
git push origin main
```

---

### 7.3 与AI协作的Git流程

#### ✅ 推荐做法

```
开发前：
  用户："我要开发批量删除功能，请帮我创建一个功能分支"
  AI：[执行 git checkout -b feature/batch-delete]

开发中：
  AI：自动在当前分支进行代码修改
  用户：随时可以测试和反馈

开发完成：
  用户："功能开发完成，请提交代码"
  AI：[执行 git add & git commit & git push]

代码审查：
  用户：在GitHub上review代码
  用户："有几个地方需要修改：[列出问题]"
  AI：修改后再次提交

合并代码：
  用户："可以合并了"
  AI：[合并到主分支并推送]
```

---

## 8. 工具使用建议

### 8.1 MCP工具使用

#### 🔧 已集成的工具

本项目已经集成了以下 MCP 工具：

```
1. Git MCP - 版本控制
   ✅ git_status      - 查看状态
   ✅ git_add         - 添加文件
   ✅ git_commit      - 提交代码
   ✅ git_push        - 推送到远程
   ✅ git_log         - 查看历史
   ✅ git_branch      - 分支管理

2. Filesystem MCP - 文件操作
   ✅ read_file       - 读取文件
   ✅ write_file      - 写入文件
   ✅ list_directory  - 列出目录

3. Puppeteer MCP - 浏览器自动化（可选）
   ✅ navigate        - 打开网页
   ✅ screenshot      - 截图
   ✅ click           - 点击元素
```

#### 💡 使用建议

```
充分利用工具能力：

1. 让AI自动处理Git操作
   "请提交代码到GitHub" 
   → AI会自动执行 add、commit、push

2. 让AI直接修改文件
   "修改配置文件中的数据库密码"
   → AI会读取、修改、保存文件

3. 让AI查看项目状态
   "检查一下当前有哪些未提交的文件"
   → AI会执行 git status 查看

4. 让AI管理分支
   "创建一个功能分支 feature/xxx"
   → AI会执行 git checkout -b
```

---

### 8.2 开发工具配置

#### 🛠️ 推荐的本地工具

```yaml
必备工具：
  - Git: 版本控制
  - Docker: 容器化开发
  - VS Code / PyCharm: 代码编辑器
  - Postman / Insomnia: API测试
  - DBeaver / pgAdmin: 数据库管理

VS Code 插件推荐：
  - Python
  - Vue - Official
  - ESLint
  - Prettier
  - GitLens
  - Docker
  - REST Client
```

---

## 9. 常见问题 FAQ

### Q1: AI生成的代码可以直接使用吗？

**A**: 不建议直接使用，应该先审查：

```
审查清单：
✅ 逻辑是否正确
✅ 是否有安全漏洞
✅ 是否有性能问题
✅ 代码风格是否统一
✅ 是否有足够的错误处理
✅ 是否有必要的注释

推荐流程：
1. AI生成代码
2. 人工仔细审查
3. 本地测试验证
4. 修改问题（如有）
5. 确认后提交
```

---

### Q2: 如何让AI理解我的项目结构？

**A**: 提供项目概览：

```markdown
## 方法1：提供目录结构
项目结构：
```
project/
├── app/          # 后端代码
│   ├── api/      # API路由
│   ├── models/   # 数据模型
│   └── services/ # 业务逻辑
├── admin-frontend/ # 前端代码
└── doc/          # 文档
```

## 方法2：说明技术栈
- 后端：FastAPI + SQLAlchemy + PostgreSQL
- 前端：Vue3 + TypeScript + Element Plus
- 遵循RESTful API设计

## 方法3：提供核心文件
"这是我的项目主要代码结构，请先熟悉一下：
- app/main.py - 应用入口
- app/models/message.py - 消息模型
- admin-frontend/src/router/index.ts - 前端路由"
```

---

### Q3: AI生成的代码有bug怎么办？

**A**: 清晰地反馈问题：

```markdown
## 标准反馈流程

1. 描述问题
   "你刚才实现的删除功能，点击后报错了"

2. 提供错误信息
   [粘贴完整的错误堆栈]

3. 说明复现步骤
   "在消息列表页，点击某条消息的删除按钮"

4. 说明期望行为
   "应该弹出确认框，确认后删除成功"

5. 提供额外信息（如果有）
   "我检查了后端日志，发现是权限检查有问题"

不要只说："不work"、"有bug"、"报错了"
```

---

### Q4: 如何让AI帮我优化代码？

**A**: 明确优化目标：

```
❌ 模糊的请求
"优化一下代码"

✅ 明确的请求
"帮我优化消息列表查询的性能，
当前1000条数据查询需要3秒，
希望优化到500ms以内。
可以考虑添加索引、使用分页、添加缓存等方法。"

✅ 具体的优化方向
"这段代码有N+1查询问题，
请改用JOIN查询来优化。"

✅ 提供性能数据
"根据Chrome Performance分析，
这个函数执行时间占了总时间的60%，
请帮我优化它。"
```

---

### Q5: 如何管理多个功能的并行开发？

**A**: 使用分支管理：

```bash
# 功能1：消息批量删除
git checkout -b feature/batch-delete
[与AI协作开发功能1]
git add . && git commit -m "feat: 批量删除"

# 切换到功能2：邮件模板
git checkout develop
git checkout -b feature/email-template
[与AI协作开发功能2]
git add . && git commit -m "feat: 邮件模板"

# 功能1开发完成，合并
git checkout develop
git merge feature/batch-delete

# 继续开发功能2
git checkout feature/email-template
```

---

### Q6: AI会不会把敏感信息提交到Git？

**A**: 采取保护措施：

```
1. 使用 .gitignore
   ✅ 已配置忽略 .env, env.dev 等敏感文件
   ✅ 已配置忽略 venv, node_modules 等

2. 使用 .env.example
   ✅ 提供模板文件，不包含真实密码
   
3. 提交前检查
   用户："请提交代码前，先用 git diff 检查，
         确认没有敏感信息"
   
4. 定期审查
   git log --all --full-history -- .env
   （检查是否误提交敏感文件）
```

---

### Q7: 如何让AI的代码风格符合项目规范？

**A**: 提供规范文档：

```
方法1：提供规范文档
"请按照 doc/开发规范/Python开发规范手册.md 
 中的规范来编写代码"

方法2：提供代码示例
"请参考 app/api/v1/messages.py 中的代码风格，
 保持一致的命名和结构"

方法3：明确说明规范
"代码规范要求：
- 使用类型注解
- 函数添加文档字符串
- 错误统一使用HTTPException
- 使用驼峰命名法"

方法4：配置代码检查工具
"使用 black 格式化代码"
"使用 eslint 检查代码"
```

---

## 10. 检查清单

### 10.1 功能开发检查清单

#### 开发前

```
□ 需求是否清晰明确？
□ 技术方案是否可行？
□ 是否需要数据库变更？
□ 是否影响现有功能？
□ 是否需要更新文档？
```

#### 开发中

```
□ 代码是否符合规范？
□ 是否有充分的错误处理？
□ 是否有必要的日志记录？
□ UI交互是否友好？
□ 是否考虑了边界情况？
```

#### 开发后

```
□ 功能是否正常工作？
□ 是否通过了测试？
□ 是否更新了文档？
□ 是否提交了代码？
□ 是否通知了相关人员？
```

---

### 10.2 代码提交检查清单

#### 提交前检查

```bash
# 1. 查看修改内容
git diff

# 2. 确认没有敏感信息
git diff | grep -i "password\|secret\|key"

# 3. 查看将要提交的文件
git status

# 4. 确认 .gitignore 工作正常
git status --ignored

# 5. 运行测试
pytest  # Python
npm test  # Node.js

# 6. 代码格式化
black .  # Python
npm run lint  # Node.js

# 7. 提交代码
git add .
git commit -m "feat: ..."
git push
```

#### 提交后检查

```
□ 远程仓库是否更新成功？
□ CI/CD是否通过？（如果有）
□ 是否通知团队成员？
□ 是否更新了 CHANGELOG？
□ 是否打了版本标签？（如果是release）
```

---

### 10.3 问题排查检查清单

#### 遇到问题时

```
□ 错误信息是否完整？
□ 是否能稳定复现？
□ 是否检查了日志？
□ 是否检查了网络？
□ 是否检查了权限？
□ 是否检查了配置？
□ 是否搜索过类似问题？
□ 是否尝试过重启服务？
```

#### 向AI反馈时

```
□ 是否提供了完整的错误堆栈？
□ 是否说明了复现步骤？
□ 是否提供了环境信息？
□ 是否提供了相关代码？
□ 是否说明了期望行为？
□ 是否提供了截图（UI问题）？
```

---

## 11. 最佳实践总结

### ✅ DO - 推荐做法

```
1. 需求沟通
   ✅ 使用结构化格式描述需求
   ✅ 提供具体的使用场景和示例
   ✅ 说明预期结果和验收标准
   ✅ 一次专注于一个功能

2. 问题反馈
   ✅ 提供完整的错误信息
   ✅ 说明详细的复现步骤
   ✅ 提供环境和版本信息
   ✅ 使用截图辅助说明

3. 代码审查
   ✅ 仔细检查AI生成的代码
   ✅ 测试所有关键功能
   ✅ 检查安全性和性能
   ✅ 确保符合代码规范

4. 文档管理
   ✅ 及时更新相关文档
   ✅ 定期整理历史文档
   ✅ 保持文档与代码同步
   ✅ 使用清晰的文档结构

5. 版本控制
   ✅ 使用规范的提交信息
   ✅ 合理使用分支管理
   ✅ 提交前检查敏感信息
   ✅ 保持提交历史清晰
```

---

### ❌ DON'T - 避免的做法

```
1. 需求沟通
   ❌ 需求描述过于模糊
   ❌ 一次提出太多需求
   ❌ 不提供具体示例
   ❌ 频繁改变需求

2. 问题反馈
   ❌ 只说"不work"或"有bug"
   ❌ 不提供错误信息
   ❌ 不说明复现步骤
   ❌ 同时反馈多个不相关问题

3. 代码使用
   ❌ 不审查直接使用AI代码
   ❌ 不测试就提交代码
   ❌ 忽略安全性检查
   ❌ 不遵循项目规范

4. 文档管理
   ❌ 不更新文档
   ❌ 文档与代码不一致
   ❌ 保留过多过期文档
   ❌ 文档结构混乱

5. 版本控制
   ❌ 提交信息随意填写
   ❌ 直接在主分支开发
   ❌ 提交敏感信息
   ❌ 不检查就强制推送
```

---

## 12. 快速参考

### 🚀 常用命令速查

```bash
# 项目启动
docker-compose up -d              # 启动所有服务
docker-compose ps                 # 查看服务状态
docker-compose logs -f api        # 查看实时日志

# 数据库操作
docker-compose exec api alembic upgrade head  # 运行迁移
docker-compose exec api python scripts/init_db.py  # 初始化

# Git操作
git status                        # 查看状态
git diff                          # 查看修改
git add .                         # 添加所有文件
git commit -m "feat: xxx"         # 提交
git push                          # 推送

# 代码检查
pytest                            # 运行测试
black .                           # 格式化Python代码
npm run lint                      # 检查前端代码
```

---

### 📝 对话模板

```markdown
## 新功能开发
"我需要实现 [功能名称]。

功能描述：
[详细描述]

使用场景：
1. [场景1]
2. [场景2]

技术要求：
- 后端：[要求]
- 前端：[要求]
- 性能：[要求]

参考：
[提供参考链接或截图]"

---

## 问题反馈
"遇到问题了。

问题描述：
[一句话概括]

复现步骤：
1. [步骤1]
2. [步骤2]

错误信息：
```
[完整的错误堆栈]
```

预期行为：
[应该怎样]

实际行为：
[实际怎样]"

---

## 代码审查
"我review了代码，发现以下问题：

问题1：[文件名:行号]
[描述问题]
建议：[修改建议]

问题2：[文件名:行号]
[描述问题]
建议：[修改建议]

请修复这些问题。"

---

## 优化请求
"需要优化 [模块名称]。

当前问题：
[性能数据或用户反馈]

优化目标：
[具体的量化目标]

优化方向：
[建议的优化方法]

测试环境：
[数据量、硬件配置等]"
```

---

## 13. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2025-10-26 | 初始版本，基于消息通知平台项目的实践经验 |

---

## 14. 反馈与改进

这份最佳实践文档会随着项目经验不断更新和完善。

**如何提供反馈**：
1. 在项目中遇到文档未覆盖的场景
2. 发现更好的协作方式
3. 有新的工具或技巧

请记录下来，定期回顾和更新这份文档。

---

**文档维护者**: AI协作开发团队  
**最后更新**: 2025-10-26  
**适用项目**: 消息通知平台 (dingdong)

---

## 附录：本项目实践案例

本文档基于 **消息通知平台 (dingdong)** 项目的实际开发经验编写。

### 成功案例

1. **项目清理**
   - 问题：项目中有145MB无关文件
   - 做法：用户提供清晰的清理需求，AI生成清理脚本
   - 结果：成功清理，节省145MB空间

2. **功能开发**
   - 问题：管理后台多个功能待开发
   - 做法：分模块逐个实现（模板管理、邮箱管理、消息管理）
   - 结果：功能完整实现，代码质量高

3. **问题修复**
   - 问题：重试次数显示异常 "3/"
   - 做法：用户提供截图和详细描述，AI快速定位并修复
   - 结果：问题当天解决

4. **Git提交**
   - 问题：需要提交代码到GitHub
   - 做法：使用Git MCP工具，AI自动完成提交和推送
   - 结果：成功提交138个文件到GitHub

### 经验教训

1. **清晰的沟通很重要**
   - 详细的错误信息节省了大量排查时间
   - 截图对UI问题帮助很大

2. **小步迭代更高效**
   - 一次开发一个功能，测试通过再继续
   - 避免一次性改动太多代码

3. **及时更新文档**
   - 边开发边更新文档
   - 定期整理历史文档

4. **代码审查不可少**
   - AI生成的代码要人工审查
   - 测试验证后再提交

这些经验都融入到了本最佳实践文档中。

