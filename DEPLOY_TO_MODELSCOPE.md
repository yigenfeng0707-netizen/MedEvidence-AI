# 魔搭社区部署指南

> **部署状态**：配置文件已就绪，待在魔搭平台操作

## 准备材料（已全部就绪）

- [x] GitHub仓库：https://github.com/yigenfeng0707-netizen/MedEvidence-AI
- [x] 分支：`master`
- [x] Python版本：3.11
- [x] KnowS API Key：`sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi`
- [x] StepFun API Key：`2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ`
- [x] 模型名：`step-2-16k`
- [x] 配置文件：`modelscope.yaml`、`smart_tool.json`

## 部署步骤

### 第1步：登录魔搭

访问：https://modelscope.cn/my/skills

点击 **「创建Skill」** 或 **「创建智能体」**。

### 第2步：选择导入方式

选择 **「从 GitHub 导入」**：

| 项 | 值 |
|----|----|
| GitHub 仓库地址 | `https://github.com/yigenfeng0707-netizen/MedEvidence-AI` |
| 分支 | `master` |
| Python 版本 | `3.11` |

### 第3步：填写基本信息

| 项 | 值 |
|----|----|
| Skill 名称 | `medevidence-ai` |
| 显示名称 | `医学循证检索助手` |
| 简介 | 基于KnowS医学循证API的智能检索Skill，支持PubMed文献检索、循证分级标注、智能摘要生成和引用格式化导出。 |
| 分类 | 医疗/健康 |
| 图标 | 🩺 |
| 标签 | 医疗, 医学文献, 循证医学, PubMed, 文献检索 |

### 第4步：配置运行环境

| 项 | 值 |
|----|----|
| 启动命令 | `uvicorn src.main:app --host 0.0.0.0 --port 8000` |
| 端口 | `8000` |
| 健康检查路径 | `GET /health` |

### 第5步：配置环境变量（重要！）

在「环境变量」或「高级配置」中添加以下变量：

```
# 必需 - 密钥（在魔搭平台配置，不要写进代码）
KNOWS_API_KEY=sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi
STEPFUN_API_KEY=2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ

# 可选 - 有默认值
KNOWS_API_BASE=https://api.nullht.com/v1
STEPFUN_API_BASE=https://api.stepfun.com/v1
STEPFUN_MODEL=step-2-16k
DEBUG=false
PORT=8000
CACHE_ENABLED=true
CACHE_TTL=3600
LOG_LEVEL=INFO
```

> ⚠️ **注意**：KNOWS_API_KEY 和 STEPFUN_API_KEY 务必在魔搭平台的「密钥/Secrets」区域配置，选择「不公开」，不要直接写在代码或配置文件里。

### 第6步：配置资源

| 项 | 值 |
|----|----|
| CPU | 2核 |
| 内存 | 4GiB |

### 第7步：提交部署

1. 点击 **「创建并部署」**
2. 等待构建和部署（通常 3-5 分钟）
3. 查看日志确认启动成功

### 第8步：部署后验证

部署成功后，你会获得一个 Skill 公开链接，格式类似：
```
https://modelscope.cn/skills/your-username/medevidence-ai
```

API 调用地址格式类似：
```
https://medevidence-ai-xxxx.modelscope.cn/api/v1/search
```

测试接口：

```bash
# 健康检查
curl https://your-skill-url/api/health

# 检索文献
curl -X POST https://your-skill-url/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SGLT2 inhibitors renal protection type 2 diabetes",
    "max_results": 3,
    "generate_summary": true
  }'
```

### 第9步：更新 smart_tool.json

部署成功后，把 `smart_tool.json` 里的 `entry_point` 替换成你的魔搭线上地址：

```json
"entry_point": "https://your-skill-url.api.modelscope.cn/api/v1/search"
```

然后提交并推送到 GitHub。

### 第10步：飞书表单登记

访问：https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh

填写：

| 项 | 值 |
|----|----|
| 项目名称 | MedEvidence AI |
| 项目简介 | 基于KnowS医学循证API的智能检索助手，支持PubMed文献检索、循证分级、智能摘要生成 |
| 魔搭链接 | `https://modelscope.cn/skills/your-username/medevidence-ai` |
| GitHub链接 | `https://github.com/yigenfeng0707-netizen/MedEvidence-AI` |
| 团队成员 | [你的名字] |
| 联系方式 | [你的邮箱/微信] |

## 部署检查清单

提交前确认：
- [ ] Skill名称不与已有项目重复
- [ ] GitHub仓库地址和分支正确
- [ ] KNOWS_API_KEY 和 STEPFUN_API_KEY 已配置为密钥（非公开）
- [ ] STEPFUN_MODEL 设置为 `step-2-16k`（不是 step-1-flash）
- [ ] 启动命令正确
- [ ] 健康检查路径为 `/health`
- [ ] 端口为 8000
- [ ] requirements.txt 在仓库根目录
- [ ] src/main.py 是正确入口
- [ ] 部署后公开链接可以访问
- [ ] API测试通过
- [ ] smart_tool.json 的 entry_point 已更新为线上地址
- [ ] 飞书表单已提交

## 常见问题

### Q: 部署失败怎么办？
A: 查看构建日志，常见原因：
- 依赖安装失败 → 检查 requirements.txt
- 端口冲突 → 确认 PORT 环境变量
- API Key错误 → 检查环境变量配置
- 找不到入口 → 确认启动命令路径正确

### Q: 服务启动但接口返回500？
A: 检查应用日志，常见原因：
- KnowS API 端点路径错误 → 确认 KNOWS_API_BASE 和端点路径
- StepFun 模型名错误 → 确认 STEPFUN_MODEL 是 step-2-16k
- API Key 无效 → 确认密钥正确

### Q: 如何更新已部署的Skill？
A: 在魔搭后台点击「重新部署」，或设置 GitHub 自动触发部署。

### Q: 部署后链接打不开？
A: 等待 5-10 分钟，服务冷启动需要时间。如仍失败，查看日志。

## 部署成功后做什么

1. ✅ 获取公开链接，更新 smart_tool.json
2. ✅ 完成飞书表单登记
3. ✅ 录制演示视频（展示检索流程、证据分级、摘要生成）
4. ✅ 在官方群/社区分享成果

---

**祝部署顺利！🏆**
