# 使用GitHub CLI快速部署

## 方案A：GitHub CLI (gh) - 推荐

### 1. 安装GitHub CLI

**Windows (WinGet):**
```powershell
winget install --id GitHub.cli
```

**Mac (Homebrew):**
```bash
brew install gh
```

**Linux:**
```bash
# Debian/Ubuntu
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo apt update
sudo apt install gh
```

### 2. 登录GitHub

```bash
gh auth login
```

按提示选择：
- 选择 `GitHub.com`
- 选择 `HTTPS`
- 选择 `Login with a web browser`
- 复制验证码到浏览器授权

### 3. 一键创建仓库并推送

```bash
# 进入项目目录
cd D:\stepFun\MedEvidence-AI

# 创建GitHub仓库（会自动设为public）
gh repo create MedEvidence-AI --public --description "医学循证智能检索助手 - 小X宝黑客松参赛作品" --source=. --remote=origin --push

# 完成！
```

### 4. 验证

```bash
# 查看远程仓库
gh repo view --web
```

---

## 方案B：使用GitHub API Token

### 1. 创建Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写Note: `MedEvidence-AI-Deploy`
4. 勾选权限：
   - ✅ `repo` (完整仓库权限)
   - ✅ `workflow` (如果需要Actions)
5. 点击 Generate token
6. **立即复制Token**（只显示一次！）

### 2. 使用API创建仓库

**保存Token到环境变量：**
```powershell
# Windows PowerShell
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxx"
```

**创建仓库：**
```powershell
# 创建仓库
$headers = @{
    Authorization = "Bearer $env:GITHUB_TOKEN"
    Accept = "application/vnd.github.v3+json"
}

$body = @{
    name = "MedEvidence-AI"
    description = "医学循证智能检索助手 - 小X宝黑客松参赛作品"
    private = $false
    auto_init = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

### 3. 推送代码

```bash
git remote add origin https://$env:GITHUB_TOKEN@github.com/YOUR_USERNAME/MedEvidence-AI.git
git push -u origin main
```

---

## 方案C：使用我准备的自动化脚本

### 我已创建 `AUTO_DEPLOY.ps1`

**使用方法：**

1. **获取GitHub Token:**
   - 访问 https://github.com/settings/tokens
   - 创建Token（勾选repo权限）
   - 复制Token

2. **运行自动化脚本：**
   ```powershell
   cd D:\stepFun\MedEvidence-AI
   .\AUTO_DEPLOY.ps1
   ```

3. **按提示输入：**
   - GitHub用户名
   - Personal Access Token
   - 仓库名称

4. **自动完成：**
   - ✅ 创建GitHub仓库
   - ✅ 初始化Git
   - ✅ 推送代码
   - ✅ 打开魔搭部署页面

---

## 三种方案对比

| 方案 | 难度 | 速度 | 推荐度 |
|------|------|------|--------|
| GitHub CLI | 低 | 2分钟 | ⭐⭐⭐⭐⭐ |
| GitHub API | 中 | 3分钟 | ⭐⭐⭐⭐ |
| Web界面 | 低 | 5分钟 | ⭐⭐⭐ |

---

## 推荐使用GitHub CLI

最简单、最安全的方式：

```bash
# 1. 安装
winget install --id GitHub.cli

# 2. 登录
gh auth login

# 3. 创建并推送
cd D:\stepFun\MedEvidence-AI
gh repo create MedEvidence-AI --public --source=. --push

# 完成！
```

---

## 下一步

GitHub推送成功后：
1. 访问魔搭 https://modelscope.cn/skills/create?template=custom
2. 选择"从GitHub导入"
3. 填写环境变量（API Keys已配置在.env.production）
4. 部署并获取链接
5. 填写飞书表单

---

**需要我帮你创建AUTO_DEPLOY.ps1自动化脚本吗？** 🤖
