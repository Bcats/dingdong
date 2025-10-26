# MCP工具配置手册

> 更新时间：2025-10-26  
> 配置位置：`c:\Users\swj\.cursor\mcp.json`

## 📋 已配置工具列表

| 工具名 | 包名 | 版本 | 状态 | 说明 |
|--------|------|------|------|------|
| **filesystem** | @modelcontextprotocol/server-filesystem | 官方最新 | ✅ 已启用 | 文件系统增强操作 |
| **memory** | @modelcontextprotocol/server-memory | 官方最新 | ✅ 已启用 | 持久化知识库 |
| **puppeteer** | @modelcontextprotocol/server-puppeteer | 官方最新 | ✅ 已启用 | 浏览器自动化 |
| **git** | @cyanheads/git-mcp-server | 2.5.6+ | ✅ 已启用 | Git版本控制 |

---

## 1. 🗂️ Filesystem - 文件系统工具

### 功能
- 📁 递归搜索文件
- 📝 批量文件操作
- 📊 文件监控
- 🔍 高级文件查询

### 配置
```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "D:\\workspace\\ai\\dingdong"
    ]
  }
}
```

### 使用示例
```
搜索项目中所有包含"TODO"的文件
列出app目录下所有Python文件
读取config目录下的所有配置文件
```

---

## 2. 🧠 Memory - 记忆工具

### 功能
- 💾 持久化知识存储
- 🔗 实体关系管理
- 🔍 知识检索
- 📝 观察记录

### 配置
```json
{
  "memory": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-memory"
    ]
  }
}
```

### 使用场景
- 记住项目特定的配置和约定
- 存储重要的技术决策
- 维护项目知识图谱

---

## 3. 🌐 Puppeteer - 浏览器自动化

### 功能
- 🖼️ 网页截图
- 🔄 页面导航
- 💻 JavaScript执行
- 🖱️ 页面交互（点击、填写、悬停）
- 📄 PDF生成
- 🕷️ 网页爬取

### 配置
```json
{
  "puppeteer": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-puppeteer"
    ],
    "env": {
      "PUPPETEER_EXECUTABLE_PATH": "C:\\Users\\swj\\.cache\\puppeteer\\chrome\\131.0.6778.204\\chrome-win64\\chrome.exe"
    }
  }
}
```

### Chrome浏览器
- **位置**：`C:\Users\swj\.cache\puppeteer\chrome\131.0.6778.204\chrome-win64\chrome.exe`
- **版本**：131.0.6778.204
- **大小**：约170MB

### 使用示例
```
访问 https://example.com 并截图
获取百度首页的标题
测试我的网站 http://localhost:3000 是否正常
```

---

## 4. 🔧 Git - 版本控制工具

### 功能
- 📊 查看仓库状态 (`git status`)
- ➕ 添加文件到暂存区 (`git add`)
- 💾 提交更改 (`git commit`)
- 📜 查看提交历史 (`git log`)
- 🌿 分支管理 (`git branch/checkout`)
- 🔄 推送和拉取 (`git push/pull`)
- 📝 查看差异 (`git diff`)
- 🏷️ 标签管理 (`git tag`)

### 配置
```json
{
  "git": {
    "command": "npx",
    "args": [
      "-y",
      "@cyanheads/git-mcp-server",
      "D:\\workspace\\ai\\dingdong"
    ]
  }
}
```

### 工作目录
- **仓库路径**：`D:\workspace\ai\dingdong`
- **当前分支**：`main`

### 使用示例
```
查看当前Git状态
添加所有更改的文件到暂存区
提交代码，提交信息为"完成用户登录功能"
查看最近5次提交历史
创建新分支 feature/new-api
推送到远程仓库
```

---

## 🔄 重启Cursor加载MCP工具

每次修改`mcp.json`后，必须重启Cursor：

### 重启步骤
1. **完全关闭Cursor**（所有窗口）
2. 等待10秒
3. 重新打开Cursor
4. 等待30秒让MCP加载
5. 验证工具是否可用

### 验证方法
询问AI："你现在有哪些MCP工具可用？"

---

## 📝 完整配置文件

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:\\workspace\\ai\\dingdong"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "puppeteer": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-puppeteer"
      ],
      "env": {
        "PUPPETEER_EXECUTABLE_PATH": "C:\\Users\\swj\\.cache\\puppeteer\\chrome\\131.0.6778.204\\chrome-win64\\chrome.exe"
      }
    },
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@cyanheads/git-mcp-server",
        "D:\\workspace\\ai\\dingdong"
      ]
    }
  }
}
```

---

## 🛠️ 故障排除

### 问题1：MCP工具未连接
**解决**：完全重启Cursor（不是刷新）

### 问题2：Puppeteer找不到Chrome
**解决**：检查环境变量`PUPPETEER_EXECUTABLE_PATH`是否正确

### 问题3：Git操作失败
**解决**：确保工作目录是有效的Git仓库

### 问题4：包下载失败
**解决**：清除npm缓存
```powershell
npm cache clean --force
```

---

## 📚 相关资源

### 官方文档
- [MCP官方网站](https://modelcontextprotocol.org/)
- [Puppeteer官方文档](https://pptr.dev/)
- [Git MCP Server](https://github.com/cyanheads/git-mcp-server)

### 项目文档
- `doc\项目文档\` - 项目相关文档
- `doc\安装部署\` - 安装部署文档

---

## 📞 获取帮助

遇到问题时，可以：
1. 询问AI："帮我检查MCP工具配置"
2. 询问AI："测试[工具名]是否可用"
3. 查看Cursor输出面板的错误信息

---

## 🎯 最佳实践

### 1. Git提交规范
```
类型: 简短描述

详细说明（可选）

示例：
feat: 添加用户登录功能
fix: 修复邮件发送失败问题
docs: 更新API文档
refactor: 重构用户模块代码
```

### 2. 使用建议
- ✅ 定期提交代码（小步快走）
- ✅ 写清晰的提交信息
- ✅ 使用分支进行功能开发
- ✅ 提交前检查代码状态

### 3. 安全注意
- ⚠️ 不要提交敏感信息（密码、密钥）
- ⚠️ 使用`.gitignore`排除不需要的文件
- ⚠️ 检查`.env`文件是否被忽略

---

**文档版本**：v1.0  
**最后更新**：2025-10-26  
**维护者**：AI助手


