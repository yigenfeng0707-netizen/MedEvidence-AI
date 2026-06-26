@echo off
chcp 65001 >nul
echo ==========================================
echo   MedEvidence AI - 快速部署工具
echo ==========================================
echo.

REM 检查Git是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Git，请先安装Git
    echo 下载地址: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] 初始化Git仓库...
git init
git add .
git commit -m "Initial commit: MedEvidence AI MVP

- 完成核心检索功能
- 集成KnowS和StepFun API  
- 添加循证分级和智能摘要
- 符合比赛规范要求"

echo.
echo [2/5] Git仓库初始化完成!
echo.
echo ==========================================
echo   下一步：创建GitHub仓库
echo ==========================================
echo.
echo 请按以下步骤操作：
echo.
echo 1. 访问: https://github.com/new
echo 2. 填写信息：
echo    - Repository name: MedEvidence-AI
echo    - Description: 医学循证智能检索助手 - 小X宝黑客松参赛作品
echo    - 选择 Public
echo 3. 点击 Create repository
echo.
echo 4. 复制仓库链接（选择HTTPS）：
echo    https://github.com/YOUR_USERNAME/MedEvidence-AI.git
echo.
set /p GITHUB_URL="[5/5] 粘贴GitHub仓库链接: "

echo.
echo 关联远程仓库...
git remote add origin %GITHUB_URL%

echo 推送代码到GitHub...
git push -u origin main

echo.
echo ==========================================
echo   ✅ GitHub推送完成！
echo ==========================================
echo.
echo 下一步：魔搭部署
echo 访问: https://modelscope.cn/skills/create?template=custom
echo.
echo 按任意键打开魔搭部署页面...
pause >nul
start https://modelscope.cn/skills/create?template=custom

echo.
echo 部署完成后，记得：
echo 1. 复制魔搭公开链接
echo 2. 填写飞书表单: https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh
echo.
pause
