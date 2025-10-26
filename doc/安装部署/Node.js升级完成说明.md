# Node.js 升级完成说明

## ✅ 升级状态

### 已完成的工作

1. **✓ Node.js 20.18.0 已下载并安装**
   - 安装位置：`D:\runtime\nodejs\nodejs-v20.18.0`
   - 文件大小：77.62 MB
   - 包含：Node.js v20.18.0 + npm 10.8.2

2. **✓ 当前会话已可使用新版本**
   - 当前PowerShell窗口中已经可以使用Node.js 20.18.0
   - 验证：运行 `node --version` 显示 `v20.18.0`

### 需要完成的最后一步

**⚠️ 重要：更新系统环境变量（需要管理员权限）**

虽然当前会话可以使用新版本，但要让所有新打开的终端和Cursor都能使用新版本，需要更新系统环境变量。

---

## 🚀 完成环境变量更新

### 方法1：双击批处理文件（推荐，最简单）

1. **找到文件**：在项目根目录找到这个文件：
   ```
   更新Node.js环境变量（管理员）.bat
   ```

2. **双击运行**：
   - 双击该文件
   - Windows会弹出UAC对话框，询问是否允许此应用对设备进行更改
   - 点击"是"

3. **等待完成**：
   - 脚本会自动更新系统PATH
   - 显示"更新完成"后，按任意键关闭窗口

### 方法2：手动以管理员身份运行PowerShell

如果方法1不起作用，可以手动执行：

1. **打开管理员PowerShell**：
   - 按 `Win + X`
   - 选择"Windows PowerShell (管理员)"

2. **导航到项目目录**：
   ```powershell
   cd D:\workspace\ai\dingdong
   ```

3. **运行更新脚本**：
   ```powershell
   .\update-nodejs-path.ps1
   ```

### 方法3：手动修改（如果脚本都不工作）

1. **打开环境变量设置**：
   - 右键"此电脑" → 属性
   - 点击"高级系统设置"
   - 点击"环境变量"

2. **编辑系统PATH**：
   - 在"系统变量"区域找到"Path"
   - 点击"编辑"
   - 找到：`D:\runtime\nodejs\nodejs-v12.14.0`
   - 改为：`D:\runtime\nodejs\nodejs-v20.18.0`
   - 点击"确定"保存

---

## 🔄 重启应用

环境变量更新后，需要重启相关应用：

1. **关闭所有PowerShell/CMD窗口**
2. **重启Cursor**（如果正在运行）
3. **重启其他IDE**（如VS Code等）

---

## ✅ 验证升级

重启后，打开新的PowerShell窗口，运行：

```powershell
node --version
# 应该显示：v20.18.0

npm --version
# 应该显示：10.8.2

# 查看Node.js路径
(Get-Command node).Source
# 应该显示：D:\runtime\nodejs\nodejs-v20.18.0\node.exe
```

---

## 📋 安装目录结构

您的Node.js安装目录现在应该是这样的：

```
D:\runtime\nodejs\
├── nodejs-v12.14.0\    (旧版本 - 可以删除)
└── nodejs-v20.18.0\    (新版本 - 正在使用)
    ├── node.exe
    ├── npm
    ├── npm.cmd
    └── ...
```

### 清理旧版本（可选）

确认新版本工作正常后，可以删除旧版本：

```powershell
# 验证新版本工作正常后
Remove-Item -Path "D:\runtime\nodejs\nodejs-v12.14.0" -Recurse -Force
```

---

## 🎯 下一步：配置MCP工具

Node.js升级完成后，就可以开始配置MCP工具了！

### 快速开始

1. **阅读快速指南**：
   ```
   doc\MCP插件\06-快速开始.md
   ```

2. **配置最小化MCP工具**（大约5分钟）：
   - Filesystem（文件系统）
   - Git（版本控制）
   - Memory（知识库）

3. **编辑Cursor配置文件**：
   
   打开配置文件：
   ```powershell
   explorer "$env:APPDATA\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings"
   ```
   
   编辑 `cline_mcp_settings.json`：
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
       "git": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-git",
           "--repository",
           "D:\\workspace\\ai\\dingdong"
         ]
       },
       "memory": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-memory"
         ]
       }
     }
   }
   ```

4. **重启Cursor并测试**：
   ```
   请列出当前项目根目录的所有文件
   ```

### 完整文档

查看完整的MCP工具文档：
- 📚 主文档：`doc\MCP插件\README.md`
- 🚀 快速开始：`doc\MCP插件\06-快速开始.md`
- 📖 详细配置：`doc\MCP插件\04-工具配置详解.md`

---

## ❓ 常见问题

### Q: 更新后仍然显示旧版本？

A: 确保：
1. 已运行环境变量更新脚本
2. 已重启所有终端窗口
3. 已重启Cursor

### Q: 遇到"执行策略"错误？

A: 运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: 还是不行怎么办？

A: 查看故障排除文档：
```
doc\MCP插件\05-常见问题.md
```

---

## 📞 需要帮助？

如果遇到任何问题：

1. 查看 `doc\MCP插件\05-常见问题.md`
2. 直接询问我
3. 提供错误信息以便诊断

---

**祝您使用愉快！** 🎉

下一步：[配置MCP工具](doc/MCP插件/06-快速开始.md)



