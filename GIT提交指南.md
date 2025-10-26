# Git 提交指南

## 📋 当前状态

✅ **项目清理已完成**
- 删除了约 145MB 无关文件
- 整理了 20+ 历史文档到独立目录
- 配置了 `.gitignore` 和 `.env.example`
- Git 仓库已初始化

---

## 🚀 快速提交（推荐）

### 一键提交命令

```powershell
# 1. 查看将要提交的文件
git status

# 2. 添加所有文件到暂存区
git add .

# 3. 再次确认（重要！）
git status

# 4. 提交
git commit -m "feat: 初始化消息通知平台项目

- 添加后端API（FastAPI + PostgreSQL + Redis + RabbitMQ）
- 添加管理后台（Vue3 + Element Plus）
- 添加数据库迁移（Alembic）
- 添加Docker部署配置
- 添加完整项目文档和运维脚本
- 配置Git忽略文件和环境变量模板"

# 5. 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/your-username/your-repo.git

# 6. 推送到远程仓库
git push -u origin main
```

---

## ⚠️ 提交前必须检查

### 1. 确认敏感文件已被忽略

```powershell
# 查看被忽略的文件
git status --ignored

# 确认以下文件在忽略列表中：
# - env.dev
# - .env
# - venv/
# - node_modules/
# - logs/
# - backups/
```

### 2. 确认不会提交敏感信息

```powershell
# 检查暂存的文件中是否包含密码等敏感信息
git diff --cached | Select-String -Pattern "password|secret|key" -Context 2
```

### 3. 验证 .gitignore 正常工作

```powershell
# 应该看不到 venv, node_modules, .env 等
git status
```

---

## 📝 分步提交（谨慎方案）

如果你想更仔细地控制提交内容，可以分步提交：

### 第1步：配置文件

```powershell
git add .gitignore .env.example .dockerignore .pre-commit-config.yaml
git add Makefile pytest.ini
git commit -m "chore: 添加项目配置文件"
```

### 第2步：依赖管理

```powershell
git add requirements.txt requirements-dev.txt
git add alembic.ini
git commit -m "chore: 添加依赖管理配置"
```

### 第3步：Docker配置

```powershell
git add docker-compose.yml docker/
git commit -m "chore: 添加Docker部署配置"
```

### 第4步：后端代码

```powershell
git add app/ alembic/
git commit -m "feat: 添加后端API和数据库迁移

- FastAPI应用框架
- SQLAlchemy数据模型
- Celery异步任务
- 邮件发送服务
- 消息管理API
- 模板管理API
- 认证和授权"
```

### 第5步：前端代码

```powershell
git add admin-frontend/
git commit -m "feat: 添加管理后台

- Vue3 + Element Plus
- 消息管理界面
- 模板管理界面
- 邮箱管理界面
- 响应式布局"
```

### 第6步：运维脚本

```powershell
git add scripts/
git commit -m "feat: 添加运维脚本

- 数据库初始化
- 创建管理员
- 创建API密钥
- 邮箱账户管理
- 邮件测试工具"
```

### 第7步：文档

```powershell
git add doc/ README.md
git commit -m "docs: 添加项目文档

- 需求文档
- 开发规范
- 数据库设计
- 用户指南
- 运维文档
- 部署手册
- API文档"
```

### 第8步：推送

```powershell
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

---

## 🔍 提交后验证

### 1. 检查远程仓库

```powershell
# 查看远程仓库地址
git remote -v

# 查看提交历史
git log --oneline
```

### 2. 克隆测试（可选）

```powershell
# 在另一个目录克隆仓库，确保一切正常
cd ..
git clone https://github.com/your-username/your-repo.git test-clone
cd test-clone

# 验证项目结构
ls

# 检查是否缺少必要文件
# 应该有：.gitignore, .env.example, README.md 等
```

---

## 📊 提交统计

### 预期提交内容

```
约 60+ 个源代码文件
约 20+ 个文档文件
约 10+ 个配置文件
总计：约 90-100 个文件
```

### 不会提交的内容（已忽略）

```
venv/              - Python虚拟环境
node_modules/      - Node.js依赖
logs/              - 日志文件
backups/           - 备份文件
.env, env.dev      - 敏感配置
__pycache__/       - Python缓存
```

---

## 🛠️ 常见问题

### Q1: 如何撤销 git add？

```powershell
# 撤销所有文件
git reset

# 撤销特定文件
git reset HEAD <file>
```

### Q2: 如何修改最后一次提交？

```powershell
# 修改提交信息
git commit --amend -m "新的提交信息"

# 添加遗漏的文件到最后一次提交
git add forgotten-file
git commit --amend --no-edit
```

### Q3: 提交了敏感文件怎么办？

```powershell
# ⚠️ 在推送前：
git reset --soft HEAD~1  # 撤销最后一次提交，保留更改
git add .gitignore       # 先添加.gitignore
git commit -m "chore: 添加gitignore"
# 然后重新添加其他文件

# ⚠️ 已经推送到远程：
# 需要使用 git filter-branch 或 BFG Repo-Cleaner 清除历史
# 这比较复杂，建议寻求帮助
```

### Q4: 如何查看将要提交的内容？

```powershell
# 查看所有变更
git diff --cached

# 查看文件列表
git status

# 查看某个文件的变更
git diff --cached <file>
```

### Q5: 推送失败怎么办？

```powershell
# 如果远程仓库已有内容
git pull origin main --rebase
git push -u origin main

# 如果是新仓库但有README
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 📚 Git 最佳实践

### 1. 提交信息规范

使用约定式提交（Conventional Commits）：

```
feat:     新功能
fix:      修复bug
docs:     文档更新
style:    代码格式（不影响功能）
refactor: 重构
test:     测试相关
chore:    构建/工具相关
perf:     性能优化
```

示例：
```
feat: 添加邮件批量发送功能
fix: 修复邮件模板中文乱码问题
docs: 更新API文档
chore: 升级依赖包版本
```

### 2. 提交频率

- ✅ 每完成一个功能就提交
- ✅ 修复一个bug就提交
- ✅ 提交前确保代码可运行
- ❌ 不要一次提交太多内容
- ❌ 不要提交无法运行的代码

### 3. 分支管理

```powershell
# 创建开发分支
git checkout -b develop

# 创建功能分支
git checkout -b feature/new-feature

# 创建修复分支
git checkout -b hotfix/fix-bug

# 合并分支
git checkout main
git merge develop
```

---

## ✅ 检查清单

提交前请确认：

- [ ] 已删除所有无关文件（chrome, MCP插件等）
- [ ] 已清理所有日志和临时文件
- [ ] `.gitignore` 已正确配置
- [ ] `.env.example` 已创建（不含敏感信息）
- [ ] `env.dev` 和 `.env` 不在提交列表中
- [ ] `venv/` 和 `node_modules/` 不在提交列表中
- [ ] README.md 内容正确
- [ ] 项目文档已整理
- [ ] 运行 `git status` 确认文件列表
- [ ] 运行 `git diff --cached` 检查内容
- [ ] 提交信息清晰明确

---

## 🎯 提交后的工作

### 1. 创建 README 徽章（可选）

在 README.md 中添加：

```markdown
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Vue](https://img.shields.io/badge/Vue-3.3-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)
```

### 2. 配置 GitHub Actions（可选）

创建 `.github/workflows/test.yml` 自动运行测试。

### 3. 添加 License

```powershell
# 在GitHub上添加License文件
# 推荐：MIT, Apache 2.0, GPL
```

### 4. 编写详细的 README

确保 README.md 包含：
- 项目介绍
- 功能特性
- 快速开始
- 安装部署
- 使用文档
- 贡献指南
- 许可证

---

**最后更新**: 2025-10-26  
**准备状态**: ✅ 已准备好提交

