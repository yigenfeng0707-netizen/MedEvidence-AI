# MedEvidence AI - ModelScope Skill

## 基本信息

- **名称**: medevidence-ai
- **显示名称**: 医学循证检索助手
- **描述**: 基于KnowS医学循证API的智能检索工具，支持PubMed文献检索、循证分级和智能摘要生成
- **版本**: 1.0.0
- **作者**: yigenfeng0707-netizen
- **许可证**: Apache-2.0

## 功能

- 自然语言检索：用中文/英文描述疾病，自动转换为专业检索式
- 循证分级标注：自动标注Level 1-5证据等级
- 智能摘要生成：StepFun大模型生成中文摘要和临床要点
- 多源数据整合：KnowS医学循证API + PubMed开放数据

## 技术栈

- FastAPI (Python 3.11)
- KnowS 医学循证API
- StepFun Flash 大模型

## 部署配置

### 启动命令
```bash
python src/main.py
```

### 环境变量
```bash
KNOWS_API_KEY=your_knows_api_key
STEPFUN_API_KEY=your_stepfun_api_key
STEPFUN_MODEL=step-1-flash
PORT=8000
```

### 端口
8000

## API接口

### 健康检查
- **路径**: `/health`
- **方法**: GET

### 文献检索
- **路径**: `/api/v1/search`
- **方法**: POST
- **参数**: 
  - query: 检索关键词
  - max_results: 最大结果数
  - generate_summary: 是否生成摘要

## 依赖

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.0.0
httpx>=0.26.0
openai>=1.12.0
```

## 安装

```bash
pip install -r requirements.txt
python src/main.py
```

## 使用示例

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "diabetes treatment",
    "max_results": 5,
    "generate_summary": true
  }'
```

## 开源协议

Apache License 2.0
