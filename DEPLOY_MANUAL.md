# 快速部署手册（10分钟完成）

## ⚡ 3步快速部署

### Step 1: GitHub仓库（3分钟）

#### 1.1 创建仓库
1. 打开 https://github.com/new
2. 填写：
   - **Repository name**: `MedEvidence-AI`
   - **Description**: `医学循证智能检索助手 - 小X宝开源医疗黑客松参赛作品`
   - **选择**: ☑️ Public
3. 点击 **Create repository**

#### 1.2 推送代码
在创建的仓库页面，找到 **"…or push an existing repository from the command line"**，复制下方命令：

```bash
git remote add origin https://github.com/YOUR_USERNAME/MedEvidence-AI.git
git branch -M main
git push -u origin main
```

**或者运行我准备的脚本：**

**Windows CMD:**
```cmd
D:
cd D:\stepFun\MedEvidence-AI
QUICK_DEPLOY.bat
```

**Windows PowerShell:**
```powershell
cd D:\stepFun\MedEvidence-AI
.\QUICK_DEPLOY.ps1
```

**Mac/Linux:**
```bash
cd D:\stepFun\MedEvidence-AI
chmod +x QUICK_DEPLOY.sh
./QUICK_DEPLOY.sh
```

#### 1.3 验证
- 刷新GitHub页面
- 确认文件已上传

---

### Step 2: 魔搭部署（5分钟）

#### 2.1 创建Skill
1. 访问 https://modelscope.cn/skills/create?template=custom
2. 填写基本信息：
   - **Skill名称**: `medevidence-ai`
   - **显示名称**: `医学循证检索助手`
   - **简介**: `基于KnowS医学循证API的智能检索工具`

#### 2.2 导入代码
1. 选择 **"从GitHub导入"**
2. 粘贴GitHub链接：`https://github.com/YOUR_USERNAME/MedEvidence-AI`
3. 选择分支：`main`
4. Python版本：`3.11`

#### 2.3 配置环境变量
点击"高级配置"，添加以下变量：

```
KNOWS_API_KEY=sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi
STEPFUN_API_KEY=2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ
KNOWS_API_BASE=https://api.nullht.com/v1
STEPFUN_API_BASE=https://api.stepfun.com/v1
STEPFUN_MODEL=step-1-flash
DEBUG=false
PORT=8000
```

#### 2.4 配置启动命令
启动命令输入：
```bash
python src/main.py
```

#### 2.5 部署
1. 点击 **"创建并部署"**
2. 等待3-5分钟
3. 获取公开链接

#### 2.6 测试
在浏览器中测试：
```
https://your-skill-url/modelscope/health
```
应该返回健康状态

---

### Step 3: 飞书登记（2分钟）

1. 访问 https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh
2. 填写表单：

| 字段 | 填写内容 |
|------|---------|
| 项目名称 | MedEvidence AI |
| 项目简介 | 医学循证智能检索助手，支持PubMed文献检索、循证分级、智能摘要 |
| 项目类型 | Skill |
| 魔搭链接 | https://modelscope.cn/skills/medevidence-ai |
| GitHub链接 | https://github.com/YOUR_USERNAME/MedEvidence-AI |
| 团队成员 | [你的名字] |
| 联系方式 | [你的邮箱或微信] |

3. 提交表单

---

## ✅ 完成检查

部署完成后，确认以下链接可访问：

- [ ] GitHub: `https://github.com/YOUR_USERNAME/MedEvidence-AI`
- [ ] 魔搭健康检查: `https://your-skill-url/modelscope/health`
- [ ] 魔搭检索API: `https://your-skill-url/modelscope/api/v1/search`
- [ ] 飞书表单已提交

---

## 🎉 部署成功！

你已经完成了：
1. ✅ GitHub代码托管
2. ✅ 魔搭社区部署
3. ✅ 飞书作品登记

**下一步（可选）：**
- 录制演示视频
- 在官方群分享成果
- 邀请医生/医学生试用

**比赛结果公布：7月15日**

---

## 🆘 常见问题

### Q: Git推送失败？
**A**: 检查Git配置
```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

### Q: 魔搭部署失败？
**A**: 检查日志中的错误信息，常见问题：
- 依赖安装失败 → 检查requirements.txt
- 端口冲突 → 确认PORT=8000
- API Key错误 → 检查环境变量

### Q: API测试无响应？
**A**: 等待5-10分钟，服务启动需要时间

---

**部署过程遇到问题？随时在官方群提问！**
