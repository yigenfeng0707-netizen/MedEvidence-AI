# 🚀 MedEvidence AI - 快速开始

## ⚡ 10分钟完成部署

### 选择你的部署方式

#### 🥇 方案1：全自动部署（推荐）
**最适合：想最快完成部署**

1. **获取GitHub Token**（2分钟）
   - 访问 https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 勾选 `repo` 权限
   - 复制Token

2. **运行自动化脚本**（3分钟）
   ```powershell
   cd D:\stepFun\MedEvidence-AI
   .\AUTO_DEPLOY.ps1
   ```
   
3. **按提示输入：**
   - GitHub用户名
   - Personal Access Token
   - 脚本自动完成：创建仓库 → 推送代码 → 打开魔搭

4. **魔搭部署**（3分钟）
   - 脚本会自动打开魔搭页面
   - 选择"从GitHub导入"
   - 配置环境变量（已自动复制）
   - 点击部署

5. **飞书登记**（2分钟）
   - 访问表单填写

✅ **完成！**

---

#### 🥈 方案2：GitHub CLI（简单）
**最适合：已安装GitHub CLI**

```powershell
# 1. 安装GitHub CLI
winget install --id GitHub.cli

# 2. 登录
gh auth login

# 3. 创建并推送仓库
cd D:\stepFun\MedEvidence-AI
gh repo create MedEvidence-AI --public --source=. --push

# 4. 魔搭部署
# 访问: https://modelscope.cn/skills/create?template=custom
```

---

#### 🥉 方案3：手动操作（传统）
**最适合：喜欢手动控制**

1. 访问 https://github.com/new 创建仓库
2. 复制仓库链接
3. 运行 `QUICK_DEPLOY.bat`
4. 按提示操作

详细步骤见 `DEPLOY_MANUAL.md`

---

## 📋 部署配置速查

### GitHub信息
```
仓库名: MedEvidence-AI
描述: 医学循证智能检索助手 - 小X宝开源医疗黑客松参赛作品
类型: Public
```

### 魔搭配置
```
Skill名称: medevidence-ai
显示名称: 医学循证检索助手
分支: main
Python: 3.11
启动命令: python src/main.py
```

### 环境变量
```
KNOWS_API_KEY=sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi
STEPFUN_API_KEY=2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ
STEPFUN_MODEL=step-1-flash
DEBUG=false
PORT=8000
```

### 飞书表单
```
链接: https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh
```

---

## 🎯 推荐执行顺序

```
如果你选择方案1（全自动）：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 获取GitHub Token (2分钟)
   └── 访问 https://github.com/settings/tokens
   └── 创建Token，勾选repo权限
   
2. 运行AUTO_DEPLOY.ps1 (3分钟)
   └── cd D:\stepFun\MedEvidence-AI
   └── .\AUTO_DEPLOY.ps1
   └── 输入用户名和Token
   
3. 魔搭部署 (3分钟)
   └── 脚本自动打开魔搭页面
   └── 选择"从GitHub导入"
   └── 粘贴GitHub链接
   └── 配置环境变量
   └── 点击部署
   
4. 飞书登记 (2分钟)
   └── 访问飞书表单
   └── 填写信息提交
   
✅ 总计: 10分钟完成全部部署！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📞 遇到问题？

### 常见问题

**Q: 脚本运行失败？**
```
A: 以管理员身份运行PowerShell
右键PowerShell → 以管理员身份运行
```

**Q: Token创建后复制不了？**
```
A: Token只显示一次！请重新生成
```

**Q: 魔搭部署失败？**
```
A: 检查日志，常见问题：
- 依赖安装失败 → 检查requirements.txt
- 端口冲突 → 确认PORT=8000
- API Key错误 → 检查环境变量
```

**Q: 其他问题？**
```
A: 查看详细文档：
- SETUP_GUIDE.md - 环境配置
- DEPLOY_MANUAL.md - 部署指南
- GITHUB_CLI_GUIDE.md - GitHub CLI使用
```

---

## 📁 相关文件

| 文件 | 用途 | 推荐 |
|------|------|------|
| `AUTO_DEPLOY.ps1` | 全自动部署脚本 | ⭐⭐⭐⭐⭐ |
| `QUICK_DEPLOY.bat` | 快速部署批处理 | ⭐⭐⭐⭐ |
| `QUICK_DEPLOY.ps1` | 快速部署PowerShell | ⭐⭐⭐⭐ |
| `DEPLOY_MANUAL.md` | 详细部署手册 | ⭐⭐⭐ |
| `GITHUB_CLI_GUIDE.md` | GitHub CLI指南 | ⭐⭐⭐ |

---

## ✅ 部署完成检查

部署成功后，确认：

- [ ] GitHub仓库可访问
- [ ] 魔搭Skill运行正常
- [ ] 飞书表单已提交
- [ ] 在官方群分享成果

---

## 🎉 准备好了吗？

**立即开始：**

```powershell
cd D:\stepFun\MedEvidence-AI
.\AUTO_DEPLOY.ps1
```

**或者：**

```cmd
D:
cd D:\stepFun\MedEvidence-AI
QUICK_DEPLOY.bat
```

---

**祝你部署顺利，勇夺冠军！🏆**

**有任何问题随时提问！**
