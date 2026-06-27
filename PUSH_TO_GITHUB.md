# 推送到GitHub指南

## 第一步：创建GitHub仓库

1. 访问 https://github.com/new
2. 填写信息：
   - Repository name: `MedEvidence-AI`
   - Description: `医学循证智能检索助手 - 小X宝黑客松参赛作品`
   - 选择 `Public`（公开仓库，符合比赛要求）
   - 勾选 `Add a README file`（可选）
3. 点击 `Create repository`

## 第二步：推送代码

### 初始化本地仓库

```bash
cd D:\stepFun\MedEvidence-AI

# 初始化Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: MedEvidence AI MVP

- 完成核心检索功能
- 集成KnowS和StepFun API
- 添加循证分级和智能摘要
- 符合比赛规范要求"
```

### 关联远程仓库

```bash
# 替换 your-username 为你的GitHub用户名
git remote add origin https://github.com/your-username/MedEvidence-AI.git

# 推送代码
git push -u origin main
```

## 第三步：添加 Secrets（用于CI/CD）

1. 进入GitHub仓库
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 添加以下Secrets：
   - `KNOWS_API_KEY`: `sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi`
   - `STEPFUN_API_KEY`: `2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ`

## 第四步：验证

1. 刷新GitHub页面，确认文件已上传
2. 确认文件列表包含：
   - ✅ README.md
   - ✅ LICENSE
   - ✅ smart_tool.json
   - ✅ src/ 目录
   - ✅ requirements.txt

## 第五步：获取仓库链接

复制仓库链接，用于魔搭部署：
```
https://github.com/your-username/MedEvidence-AI
```

## 注意事项

⚠️ **安全提醒**：
- `.env` 文件已添加到 `.gitignore`，不会提交到GitHub
- API Keys通过GitHub Secrets管理，不会在代码中暴露
- 生产环境使用 `.env.production` 模板

## 下一步

推送成功后，前往魔搭社区部署：
https://modelscope.cn/skills/create?template=custom
