# MedEvidence AI - Deploy Script for yigenfeng0707-netizen
$GitHubUsername = "yigenfeng0707-netizen"
$GitHubToken = Read-Host "请输入GitHub Token"
$RepoName = "MedEvidence-AI"
$Description = "Medical Evidence AI - Hackathon Project"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   MedEvidence AI - Deploy Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Git
Write-Host "[Step 1/6] Checking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    Write-Host "OK: Git found - $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git not found. Install from https://git-scm.com/download/win" -ForegroundColor Red
    pause
    exit 1
}

# Verify Token
Write-Host ""
Write-Host "[Step 2/6] Verifying GitHub Token..." -ForegroundColor Yellow
try {
    $headers = @{
        Authorization = "Bearer $GitHubToken"
        Accept = "application/vnd.github.v3+json"
    }
    $userInfo = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
    Write-Host "OK: Token valid for user: $($userInfo.login)" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Token verification failed" -ForegroundColor Red
    pause
    exit 1
}

# Create GitHub Repository
Write-Host ""
Write-Host "[Step 3/6] Creating GitHub Repository..." -ForegroundColor Yellow
try {
    $repoBody = @{
        name = $RepoName
        description = $Description
        private = $false
        auto_init = $false
    } | ConvertTo-Json -Depth 10
    
    $repoInfo = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $repoBody -ContentType "application/json"
    Write-Host "OK: Repository created" -ForegroundColor Green
    Write-Host "URL: $($repoInfo.html_url)" -ForegroundColor Cyan
} catch {
    if ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "NOTE: Repository already exists, using existing" -ForegroundColor Yellow
        $repoInfo = Invoke-RestMethod -Uri "https://api.github.com/repos/$GitHubUsername/$RepoName" -Headers $headers
        Write-Host "OK: Using existing repository" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to create repository - $_" -ForegroundColor Red
        pause
        exit 1
    }
}

# Initialize Git
Write-Host ""
Write-Host "[Step 4/6] Initializing Git Repository..." -ForegroundColor Yellow

Set-Location D:\stepFun\MedEvidence-AI

if (-not (Test-Path .git)) {
    git init
    Write-Host "OK: Git initialized" -ForegroundColor Green
} else {
    Write-Host "OK: Git already initialized" -ForegroundColor Green
}

# Configure Git
$gitUserName = git config user.name 2>$null
$gitUserEmail = git config user.email 2>$null
if (-not $gitUserName) {
    git config user.name $GitHubUsername
}
if (-not $gitUserEmail) {
    git config user.email "$GitHubUsername@users.noreply.github.com"
}

# Add and commit files
Write-Host "  Adding files..." -ForegroundColor Gray
git add .

$status = git status --porcelain
if ($status) {
    Write-Host "  Committing..." -ForegroundColor Gray
    git commit -m "Initial commit: MedEvidence AI MVP" 2>$null
    Write-Host "OK: Files committed" -ForegroundColor Green
} else {
    Write-Host "OK: No new changes to commit" -ForegroundColor Green
}

# Set remote
Write-Host ""
Write-Host "[Step 5/6] Configuring Remote..." -ForegroundColor Yellow

$remoteUrl = "https://$GitHubUsername`:$GitHubToken@github.com/$GitHubUsername/$RepoName.git"

$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    git remote set-url origin $remoteUrl
    Write-Host "OK: Remote updated" -ForegroundColor Green
} else {
    git remote add origin $remoteUrl
    Write-Host "OK: Remote added" -ForegroundColor Green
}

$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    git branch -M main
    Write-Host "OK: Branch renamed to main" -ForegroundColor Green
}

# Push to GitHub
Write-Host ""
Write-Host "[Step 6/6] Pushing to GitHub..." -ForegroundColor Yellow
try {
    git push -u origin main 2>$null
    Write-Host "OK: Push successful!" -ForegroundColor Green
} catch {
    Write-Host "NOTE: Trying force push..." -ForegroundColor Yellow
    git push -u origin main --force 2>$null
    Write-Host "OK: Force push successful!" -ForegroundColor Green
}

# Success
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   SUCCESS! GitHub Deploy Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Repository URL:" -ForegroundColor White
Write-Host "  https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Step: Deploy to ModelScope" -ForegroundColor Yellow
Write-Host ""
Write-Host "Configuration:" -ForegroundColor White
Write-Host "  GitHub: https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Gray
Write-Host "  Branch: main" -ForegroundColor Gray
Write-Host "  Python: 3.11" -ForegroundColor Gray
Write-Host "  Start: python src/main.py" -ForegroundColor Gray
Write-Host ""

$openDeploy = Read-Host "Open ModelScope deploy page now? (y/n)"
if ($openDeploy -eq "y" -or $openDeploy -eq "Y") {
    Write-Host "Opening ModelScope..." -ForegroundColor Cyan
    Start-Process "https://modelscope.cn/skills/create?template=custom"
}

Write-Host ""
Write-Host "After deployment, submit to:" -ForegroundColor White
Write-Host "  https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh" -ForegroundColor Cyan
Write-Host ""
Write-Host "Good luck!" -ForegroundColor Green
Write-Host ""

pause
