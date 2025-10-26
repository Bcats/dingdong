# ============================================
# 项目文件清理脚本 (PowerShell)
# 用途: 准备提交Git仓库前的文件清理
# 日期: 2025-10-26
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "项目文件清理脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 设置错误处理
$ErrorActionPreference = "Continue"

# 记录清理结果
$deletedItems = @()
$failedItems = @()

# 函数: 删除文件或目录
function Remove-ItemSafe {
    param(
        [string]$Path,
        [string]$Description
    )
    
    if (Test-Path $Path) {
        try {
            Write-Host "正在删除: $Description" -ForegroundColor Yellow
            Write-Host "  路径: $Path" -ForegroundColor Gray
            Remove-Item -Path $Path -Recurse -Force
            $script:deletedItems += $Description
            Write-Host "  ✓ 删除成功" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ 删除失败: $($_.Exception.Message)" -ForegroundColor Red
            $script:failedItems += $Description
        }
    }
    else {
        Write-Host "跳过: $Description (不存在)" -ForegroundColor Gray
    }
    Write-Host ""
}

# ============================================
# 第一步: 删除完全无关的文件
# ============================================
Write-Host "[步骤 1/4] 删除无关文件..." -ForegroundColor Cyan
Write-Host ""

Remove-ItemSafe -Path "chrome" -Description "Chrome浏览器安装包目录"
Remove-ItemSafe -Path "doc/MCP插件" -Description "MCP插件文档目录"
Remove-ItemSafe -Path "doc/安装部署/Node.js升级完成说明.md" -Description "Node.js升级说明"

# ============================================
# 第二步: 清理运行时和临时文件
# ============================================
Write-Host "[步骤 2/4] 清理运行时文件..." -ForegroundColor Cyan
Write-Host ""

# 清理日志文件（保留目录）
if (Test-Path "logs") {
    Write-Host "正在清理日志文件..." -ForegroundColor Yellow
    Get-ChildItem -Path "logs" -File | ForEach-Object {
        try {
            Remove-Item $_.FullName -Force
            Write-Host "  ✓ 删除: $($_.Name)" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ 删除失败: $($_.Name)" -ForegroundColor Red
        }
    }
    # 创建 .gitkeep
    New-Item -Path "logs/.gitkeep" -ItemType File -Force | Out-Null
    Write-Host "  ✓ 创建 logs/.gitkeep" -ForegroundColor Green
}
Write-Host ""

# 清理备份目录（保留目录）
if (Test-Path "backups") {
    Write-Host "正在清理备份文件..." -ForegroundColor Yellow
    Get-ChildItem -Path "backups" -File | ForEach-Object {
        try {
            Remove-Item $_.FullName -Force
            Write-Host "  ✓ 删除: $($_.Name)" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ 删除失败: $($_.Name)" -ForegroundColor Red
        }
    }
    # 创建 .gitkeep
    New-Item -Path "backups/.gitkeep" -ItemType File -Force | Out-Null
    Write-Host "  ✓ 创建 backups/.gitkeep" -ForegroundColor Green
}
Write-Host ""

# 删除前端临时目录
Remove-ItemSafe -Path "admin-frontend/EmailAccounts" -Description "前端EmailAccounts临时目录"
Remove-ItemSafe -Path "admin-frontend/Messages" -Description "前端Messages临时目录"
Remove-ItemSafe -Path "admin-frontend/Templates" -Description "前端Templates临时目录"

# ============================================
# 第三步: 整理文档结构
# ============================================
Write-Host "[步骤 3/4] 整理文档结构..." -ForegroundColor Cyan
Write-Host ""

# 创建历史文档目录
$historyDirs = @(
    "doc/项目文档/历史文档",
    "doc/需求文档/历史文档",
    "doc/运维文档/历史文档",
    "doc/部署运维/历史文档"
)

foreach ($dir in $historyDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
        Write-Host "✓ 创建目录: $dir" -ForegroundColor Green
    }
}
Write-Host ""

# 移动项目文档历史文件
$projectDocHistoryFiles = @(
    "API补充完成报告.md",
    "会话交接-邮件发送测试.md",
    "功能测试和文档创建总结.md",
    "后台功能实现完成报告.md",
    "登录响应格式修复.md",
    "管理后台创建完成报告.md",
    "管理后台功能优化完成报告.md",
    "管理后台启动成功报告.md",
    "管理后台开发方案.md",
    "管理后台问题修复报告.md",
    "管理员登录系统实现报告.md",
    "邮件发送功能调试报告.md",
    "邮件模板中文乱码修复.md",
    "问题修复报告-消息管理功能.md",
    "需求实现进度对比.md",
    "项目整理记录.md"
)

Write-Host "正在移动项目文档历史文件..." -ForegroundColor Yellow
foreach ($file in $projectDocHistoryFiles) {
    $source = "doc/项目文档/$file"
    $dest = "doc/项目文档/历史文档/$file"
    if (Test-Path $source) {
        try {
            Move-Item -Path $source -Destination $dest -Force
            Write-Host "  ✓ 移动: $file" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ 移动失败: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}
Write-Host ""

# 移动需求文档历史文件
$requirementDocHistoryFiles = @(
    "需求文档修订总结-v1.1.md",
    "需求文档审阅-问题清单.md"
)

Write-Host "正在移动需求文档历史文件..." -ForegroundColor Yellow
foreach ($file in $requirementDocHistoryFiles) {
    $source = "doc/需求文档/$file"
    $dest = "doc/需求文档/历史文档/$file"
    if (Test-Path $source) {
        try {
            Move-Item -Path $source -Destination $dest -Force
            Write-Host "  ✓ 移动: $file" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ 移动失败: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}
Write-Host ""

# 移动运维文档历史文件
$opsDocHistoryFiles = @(
    "监控配置完成总结.md"
)

Write-Host "正在移动运维文档历史文件..." -ForegroundColor Yellow
foreach ($file in $opsDocHistoryFiles) {
    $source = "doc/运维文档/$file"
    $dest = "doc/运维文档/历史文档/$file"
    if (Test-Path $source) {
        try {
            Move-Item -Path $source -Destination $dest -Force
            Write-Host "  ✓ 移动: $file" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ 移动失败: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}
Write-Host ""

# 移动部署运维历史文件
$deployDocHistoryFiles = @(
    "Flower服务修复记录.md"
)

Write-Host "正在移动部署运维历史文件..." -ForegroundColor Yellow
foreach ($file in $deployDocHistoryFiles) {
    $source = "doc/部署运维/$file"
    $dest = "doc/部署运维/历史文档/$file"
    if (Test-Path $source) {
        try {
            Move-Item -Path $source -Destination $dest -Force
            Write-Host "  ✓ 移动: $file" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ 移动失败: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}
Write-Host ""

# ============================================
# 第四步: 显示清理总结
# ============================================
Write-Host "[步骤 4/4] 清理完成" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "清理总结" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($deletedItems.Count -gt 0) {
    Write-Host "✓ 成功删除 $($deletedItems.Count) 项:" -ForegroundColor Green
    $deletedItems | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
    Write-Host ""
}

if ($failedItems.Count -gt 0) {
    Write-Host "✗ 删除失败 $($failedItems.Count) 项:" -ForegroundColor Red
    $failedItems | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "下一步操作建议" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 检查清理结果是否符合预期" -ForegroundColor Yellow
Write-Host "2. 查看 Git 状态: git status" -ForegroundColor Yellow
Write-Host "3. 添加文件到 Git: git add ." -ForegroundColor Yellow
Write-Host "4. 提交更改: git commit -m 'chore: cleanup project structure and organize documentation'" -ForegroundColor Yellow
Write-Host ""
Write-Host "注意: 请确保 .gitignore 和 .env.example 已经创建" -ForegroundColor Cyan
Write-Host ""

