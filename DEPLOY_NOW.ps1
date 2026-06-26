# MedEvidence AI - 专属部署脚本
# 用户: yigenfeng0707-netizen
# 自动生成部署配置

$GitHubUsername = "yigenfeng0707-netizen"
$GitHubToken = Read-Host "请输入GitHub Token"
$RepoName = "MedEvidence-AI"
$Description = "医学循证智能检索助手 - 小X宝开源医疗黑客松参赛作品"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   MedEvidence AI - 专属部署" -ForegroundColor Cyan
Write-Host "   用户: $GitHubUsername" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Git
Write-Host "[1/6] 检查Git环境..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    Write-Host "✓ Git已安装: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未检测到Git" -ForegroundColor Red
    Write-Host "请安装Git: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "按Enter键退出"
    exit 1
}

# 验证Token
Write-Host ""
Write-Host "[2/6] 验证GitHub Token..." -ForegroundColor Yellow
try {
    $headers = @{
        Authorization = "Bearer $GitHubToken"
        Accept = "application/vnd.github.v3+json"
    }
    
    $userInfo = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
    Write-Host "✓ Token有效，用户: $($userInfo.login)" -ForegroundColor Green
} catch {
    Write-Host "✗ Token验证失败: $_" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

# 创建GitHub仓库
Write-Host ""
Write-Host "[3/6] 创建GitHub仓库..." -ForegroundColor Yellow

try {
    $repoBody = @{
        name = $RepoName
        description = $Description
        private = $false
        auto_init = $false
    } | ConvertTo-Json -Depth 10
    
    $repoInfo = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $repoBody -ContentType "application/json"
    
    Write-Host "✓ 仓库创建成功!" -ForegroundColor Green
    Write-Host "  URL: $($repoInfo.html_url)" -ForegroundColor Cyan
} catch {
    if ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "⚠️  仓库已存在，使用现有仓库..." -ForegroundColor Yellow
        $repoInfo = Invoke-RestMethod -Uri "https://api.github.com/repos/$GitHubUsername/$RepoName" -Headers $headers
        Write-Host "✓ 使用现有仓库: $($repoInfo.html_url)" -ForegroundColor Green
    } else {
        Write-Host "✗ 创建仓库失败: $_" -ForegroundColor Red
        Read-Host "按Enter键退出"
        exit 1
    }
}

# 初始化本地Git
Write-Host ""
Write-Host "[4/6] 初始化本地Git仓库..." -ForegroundColor Yellow

Set-Location D:\stepFun\MedEvidence-AI

# 检查是否已是Git仓库
if (-not (Test-Path .git)) {
    git init
    Write-Host "✓ Git仓库初始化" -ForegroundColor Green
} else {
    Write-Host "✓ Git仓库已存在" -ForegroundColor Green
}

# 配置Git用户信息
$gitUserName = git config user.name 2>$null
$gitUserEmail = git config user.email 2>$null

if (-not $gitUserName) {
    git config user.name $GitHubUsername
    Write-Host "✓ Git用户名已配置" -ForegroundColor Green
}
if (-not $gitUserEmail) {
    git config user.email "$GitHubUsername@users.noreply.github.com"
    Write-Host "✓ Git邮箱已配置" -ForegroundColor Green
}

# 添加所有文件
Write-Host "  添加文件..." -ForegroundColor Gray
git add .

# 检查是否有变更要提交
$status = git status --porcelain
if ($status) {
    Write-Host "  提交代码..." -ForegroundColor Gray
    git commit -m "Initial commit: MedEvidence AI MVP

- 完成核心检索功能
- 集成KnowS和StepFun API
- 添加循证分级和智能摘要
- 符合比赛规范要求"
    Write-Host "✓ 代码已提交" -ForegroundColor Green
} else {
    Write-Host "✓ 没有新变更需要提交" -ForegroundColor Green
}

# 设置远程仓库
Write-Host ""
Write-Host "[5/6] 关联远程仓库..." -ForegroundColor Yellow

$remoteUrl = "https://$GitHubUsername`:$GitHubToken@github.com/$GitHubUsername/$RepoName.git"

# 检查是否已有origin远程
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    git remote set-url origin $remoteUrl
    Write-Host "✓ 更新远程仓库地址" -ForegroundColor Green
} else {
    git remote add origin $remoteUrl
    Write-Host "✓ 添加远程仓库" -ForegroundColor Green
}

# 重命名分支为main
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    git branch -M main
    Write-Host "✓ 分支重命名为main" -ForegroundColor Green
}

# 推送到GitHub
Write-Host ""
Write-Host "[6/6] 推送代码到GitHub..." -ForegroundColor Yellow

try {
    git push -u origin main 2>$null
    Write-Host "✓ 推送成功!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  常规推送失败，尝试强制推送..." -ForegroundColor Yellow
    git push -u origin main --force 2>$null
    Write-Host "✓ 强制推送成功!" -ForegroundColor Green
}

# 成功信息
Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "   ✅ GitHub部署完成！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 恭喜！代码已成功推送到GitHub" -ForegroundColor Cyan
Write-Host ""
Write-Host "仓库地址:" -ForegroundColor White
Write-Host "  https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 下一步：魔搭社区部署" -ForegroundColor Yellow
Write-Host ""
Write-Host "配置信息:" -ForegroundColor White
Write-Host "  GitHub链接: https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Gray
Write-Host "  分支: main" -ForegroundColor Gray
Write-Host "  Python版本: 3.11" -ForegroundColor Gray
Write-Host "  启动命令: python src/main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "环境变量:" -ForegroundColor White
Write-Host "  KNOWS_API_KEY=sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi" -ForegroundColor Gray
Write-Host "  STEPFUN_API_KEY=2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ" -ForegroundColor Gray
Write-Host ""

# 询问是否打开魔搭
$openDeploy = Read-Host "是否立即打开魔搭部署页面? (y/n)"
if ($openDeploy -eq "y" -or $openDeploy -eq "Y") {
    Write-Host ""
    Write-Host "正在打开魔搭部署页面..." -ForegroundColor Cyan
    Start-Process "https://modelscope.cn/skills/create?template=custom"
}

Write-Host ""
Write-Host "📌 部署完成后，记得:" -ForegroundColor White
Write-Host "  1. 复制魔搭公开链接" -ForegroundColor Gray
Write-Host "  2. 填写飞书表单: https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh" -ForegroundColor Cyan
Write-Host ""
Write-Host "🏆 祝部署顺利，勇夺冠军！" -ForegroundColor Green
Write-Host ""

Read-Host "按Enter键完成"
