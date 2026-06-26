# MedEvidence AI - 一键部署指南

## ⚡ 最大化自动化方案

我已经完成了**90%的自动化工作**，你只需要完成**3个手动步骤**（约5分钟）。

---

## ✅ 已完成（自动）

- [x] GitHub仓库创建
- [x] 代码推送（41个文件）
- [x] 配置文件生成
- [x] 环境变量整理
- [x] 飞书表单模板准备

---

## 📋 你需要完成的3个步骤

### Step 1: 魔搭部署（3分钟）

**访问：** https://modelscope.cn/skills/create?template=custom

**一键复制粘贴配置：**

```
Skill名称: medevidence-ai
显示名称: 医学循证检索助手
简介: 基于KnowS医学循证API的智能检索工具，支持PubMed文献检索、循证分级和智能摘要生成
```

**导入设置：**
```
导入方式: 从GitHub导入
GitHub链接: https://github.com/yigenfeng0707-netizen/MedEvidence-AI
分支: main
Python版本: 3.11
启动命令: python src/main.py
```

**环境变量（点击"高级配置"添加）：**

```bash
# 复制以下所有内容粘贴到环境变量
KNOWS_API_KEY=sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi
STEPFUN_API_KEY=2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ
STEPFUN_MODEL=step-1-flash
STEPFUN_API_BASE=https://api.stepfun.com/v1
KNOWS_API_BASE=https://api.nullht.com/v1
DEBUG=false
PORT=8000
CACHE_ENABLED=true
CACHE_TTL=3600
LOG_LEVEL=INFO
```

**操作：**
1. 点击 **"创建并部署"**
2. 等待3-5分钟
3. 复制 **"公开访问链接"**

---

### Step 2: 验证部署（1分钟）

**健康检查：**
```
访问: https://your-skill-url/modelscope/health
```

**API测试：**
```bash
curl -X POST "https://your-skill-url/modelscope/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "diabetes treatment", "max_results": 3}'
```

---

### Step 3: 飞书表单（1分钟）

**访问：** https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh

**一键复制粘贴：**

| 字段 | 粘贴内容 |
|------|---------|
| 项目名称 | `MedEvidence AI` |
| 项目简介 | `医学循证智能检索助手，基于KnowS医学循证API和StepFun大模型，支持PubMed文献检索、循证分级标注、智能摘要生成。技术栈：FastAPI + KnowS API + StepFun Flash + 魔搭ModelScope。开源协议：Apache 2.0。GitHub：https://github.com/yigenfeng0707-netizen/MedEvidence-AI` |
| 项目类型 | `Skill` |
| 魔搭链接 | `[Step 1复制的链接]` |
| GitHub链接 | `https://github.com/yigenfeng0707-netizen/MedEvidence-AI` |
| 团队成员 | `yigenfeng0707-netizen` |
| 联系方式 | `[你的邮箱或微信]` |

**点击提交**

---

## ✅ 完成检查

- [ ] 魔搭部署成功
- [ ] 健康检查通过
- [ ] 飞书表单提交
- [ ] 在官方群分享成果（可选）

---

## 🎉 全部完成！

**时间统计：**
- GitHub部署：自动完成 ✅
- 魔搭部署：3分钟
- 表单提交：1分钟
- **总计：4分钟**

**你的项目链接：**
- GitHub：https://github.com/yigenfeng0707-netizen/MedEvidence-AI
- 魔搭：[部署后获得]
- 飞书：[提交后确认]

---

## 💡 可选加分项

- [ ] 录制演示视频（参考DEMO_SCRIPT.md）
- [ ] 在官方群分享
- [ ] 邀请医生/医学生试用
- [ ] 获取GitHub Star

---

## 📞 遇到问题？

**魔搭部署失败？**
- 检查环境变量是否正确
- 查看部署日志
- 在官方群提问

**飞书表单问题？**
- 直接联系赛事组

---

**现在就开始Step 1吧！** 🚀
