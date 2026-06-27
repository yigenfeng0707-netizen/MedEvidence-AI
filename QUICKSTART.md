# 快速开始

## 环境准备

### 1. 申请API密钥

#### KnowS API
1. 访问 https://developers.nullht.com/
2. 注册账号并创建应用
3. 获取API Key

#### StepFun API
1. 访问 https://platform.stepfun.com/
2. 注册账号
3. 创建API Key

### 2. 本地部署

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/MedEvidence-AI.git
cd MedEvidence-AI

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入您的API Keys

# 5. 启动服务
python src/main.py

# 或使用uvicorn
uvicorn src.main:app --reload
```

### 3. 测试API

服务启动后，访问 http://localhost:8000/docs 查看API文档并测试。

#### 示例请求

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SGLT2 inhibitors renal protection",
    "max_results": 5,
    "generate_summary": true
  }'
```

## 魔搭社区部署

### 1. 准备Skill描述文件

确保 `smart_tool.json` 已填写完整。

### 2. 提交到魔搭社区

1. 访问 https://modelscope.cn/skills/create?template=custom
2. 上传代码仓库
3. 配置环境变量
4. 提交审核

### 3. 飞书表单登记

提交后，访问以下链接登记：
https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh

## 常见问题

### Q: 为什么需要KnowS API？
A: KnowS提供医学循证证据检索能力，是本Skill的核心数据源。

### Q: 支持哪些医学数据库？
A: 目前主要支持PubMed和KnowS数据库。

### Q: 如何确保医疗合规？
A: 本工具仅检索公开学术文献，不处理患者数据，不做诊断承诺。

## 获取帮助

- 问题反馈: https://github.com/your-username/MedEvidence-AI/issues
- 邮件: medevidence@example.com
