# 魔搭社区部署指南

## 快速部署步骤

### 1. 准备材料

确保已完成：
- [x] GitHub仓库已创建
- [x] 代码已推送到GitHub
- [x] KnowS API Key: `sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi`
- [x] StepFun API Key: `2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ`

### 2. 创建Skill

1. 访问：https://modelscope.cn/skills/create?template=custom
2. 填写基本信息：
   - **Skill名称**: `medevidence-ai`
   - **显示名称**: `医学循证检索助手`
   - **简介**: `基于KnowS医学循证API的智能检索工具，支持PubMed文献检索、循证分级和智能摘要生成`
   - **图标**: 上传一个医疗相关图标（可选）

### 3. 选择部署方式

选择 **"从GitHub导入"**：
- 粘贴GitHub仓库链接
- 选择分支: `main`
- 选择Python版本: `3.11`

### 4. 配置环境变量

在"高级配置"中添加：

```
KNOWS_API_KEY=sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi
STEPFUN_API_KEY=2XDrgYOtH3z0nnv1LoYQXD6AowAwCPwY1rZuMw6AWZES1mej4SH9MElA5wvHa4zKJ
KNOWS_API_BASE=https://api.nullht.com/v1
STEPFUN_API_BASE=https://api.stepfun.com/v1
STEPFUN_MODEL=step-1-flash
DEBUG=false
PORT=8000
```

### 5. 配置启动命令

启动命令：
```bash
python src/main.py
```

或（如果魔搭使用uvicorn）：
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 6. 提交审核

1. 点击"创建并部署"
2. 等待部署完成（通常3-5分钟）
3. 获取公开链接

### 7. 测试验证

部署成功后，测试以下接口：

```bash
# 健康检查
curl https://your-skill-url/modelscope/health

# 检索文献
curl -X POST https://your-skill-url/modelscope/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "diabetes treatment SGLT2",
    "max_results": 3,
    "generate_summary": true
  }'
```

### 8. 飞书表单登记

访问：https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh

填写：
- 项目名称: MedEvidence AI
- 项目简介: 医学循证智能检索助手
- 魔搭链接: `https://modelscope.cn/skills/your-skill-name`
- GitHub链接: `https://github.com/your-username/MedEvidence-AI`
- 团队成员: [你的名字]
- 联系方式: [你的邮箱/微信]

## 部署检查清单

提交前确认：
- [ ] Skill名称不与已有项目重复
- [ ] 环境变量已正确配置
- [ ] 启动命令正确
- [ ] 公开链接可以访问
- [ ] API测试通过
- [ ] 飞书表单已提交

## 常见问题

### Q: 部署失败怎么办？
A: 检查日志，常见问题：
- 依赖安装失败 → 检查requirements.txt
- 端口冲突 → 确认PORT环境变量
- API Key错误 → 检查环境变量配置

### Q: 如何更新已部署的Skill？
A: 在魔搭后台点击"重新部署"，或关联GitHub自动部署

### Q: 部署后链接打不开？
A: 等待5-10分钟，服务启动需要时间。如仍失败，查看日志

## 下一步

部署成功后：
1. ✅ 获取公开链接
2. ✅ 完成飞书表单
3. ✅ 录制演示视频
4. ✅ 在官方群分享成果

---

**祝部署顺利！🏆**
