# MedEvidence AI - 快速部署脚本 (PowerShell)
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   MedEvidence AI - 快速部署工具" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Git
Write-Host "[1/5] 检查Git环境..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    Write-Host "✓ Git已安装: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未检测到Git，请先安装Git" -ForegroundColor Red
    Write-Host "下载地址: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "按Enter键退出"
    exit 1
}

# 初始化Git
Write-Host ""
Write-Host "[2/5] 初始化Git仓库..." -ForegroundColor Yellow
Set-Location D:\stepFun\MedEvidence-AI

git init
git add .
git commit -m "Initial commit: MedEvidence AI MVP`n`n- 完成核心检索功能`n- 集成KnowS和StepFun API`n- 添加循证分级和智能摘要`n- 符合比赛规范要求"

Write-Host ""
Write-Host "✓ Git仓库初始化完成!" -ForegroundColor Green

# 显示GitHub创建指南
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   下一步：创建GitHub仓库" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "请按以下步骤操作：" -ForegroundColor White
Write-Host ""
Write-Host "1. 访问: https://github.com/new" -ForegroundColor Yellow
Write-Host "2. 填写信息：" -ForegroundColor White
Write-Host "   - Repository name: MedEvidence-AI" -ForegroundColor Gray
Write-Host "   - Description: 医学循证智能检索助手" -ForegroundColor Gray
Write-Host "   - 选择 Public" -ForegroundColor Gray
Write-Host "3. 点击 Create repository" -ForegroundColor White
Write-Host ""
Write-Host "4. 复制Quick setup中的HTTPS链接:" -ForegroundColor White
Write-Host "   https://github.com/YOUR_USERNAME/MedEvidence-AI.git" -ForegroundColor Green
Write-Host ""

$githubUrl = Read-Host "[3/5] 粘贴GitHub仓库链接"

Write-Host ""
Write-Host "[4/5] 关联远程仓库..." -ForegroundColor Yellow
git remote add origin $githubUrl

Write-Host "[5/5] 推送代码到GitHub..." -ForegroundColor Yellow
try {
    git push -u origin main
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "   ✅ GitHub推送完成！" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "⚠️ 推送失败，尝试强制推送..." -ForegroundColor Yellow
    git push -u origin main --force
}

Write-Host ""
Write-Host "下一步：魔搭部署" -ForegroundColor Cyan
Write-Host "正在打开魔搭部署页面..." -ForegroundColor Yellow

# 打开浏览器
Start-Process "https://modelscope.cn/skills/create?template=custom"

Write-Host ""
Write-Host "📋 部署完成后，记得：" -ForegroundColor White
Write-Host "1. 复制魔搭公开链接" -ForegroundColor Gray
Write-Host "2. 填写飞书表单: https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh" -ForegroundColor Gray
Write-Host ""

Read-Host "按Enter键完成"
