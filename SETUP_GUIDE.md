# MedEvidence AI 设置指南

## 方案A：本地测试（推荐）

### 1. 确保Python环境

```bash
# 检查Python版本（需要 >= 3.9）
python --version

# 如果没有pip，尝试以下方法安装
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### 2. 创建虚拟环境

```bash
# 进入项目目录
cd D:\stepFun\MedEvidence-AI

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. 安装依赖

```bash
# 确保在虚拟环境中，然后安装依赖
pip install -r requirements.txt
```

### 4. 运行测试版本

```bash
# 使用模拟API测试（无需真实API Key）
python test_main.py

# 服务启动后，访问：
# http://localhost:8000/docs  # API文档
# http://localhost:8000/      # 首页
```

### 5. 切换到真实API

编辑 `.env` 文件：
```
KNOWS_API_KEY=sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi  # 已配置
STEPFUN_API_KEY=your_stepfun_api_key_here  # 需要申请
```

然后运行真实版本：
```bash
python src/main.py
```

---

## 方案B：直接魔搭部署（更快）

如果本地环境配置困难，可以直接部署到魔搭社区测试。

### 1. 创建GitHub仓库

```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit: MedEvidence AI MVP"

# 在GitHub创建仓库，然后推送
git remote add origin https://github.com/your-username/MedEvidence-AI.git
git push -u origin main
```

### 2. 魔搭部署

访问：https://modelscope.cn/skills/create?template=custom

- 选择"从GitHub导入"
- 粘贴仓库链接
- 配置环境变量：
  - `KNOWS_API_KEY`: `sk-knows-aWsL8pr0PkN88F9JlqUWzKYuwkxFw5mi`
  - `STEPFUN_API_KEY`: `your_key_here`
- 提交审核

### 3. 获取链接并测试

部署成功后，获得公开链接，在浏览器中测试API。

---

## StepFun API Key申请步骤

1. 访问：https://platform.stepfun.com/
2. 点击右上角"注册/登录"
3. 完成注册并登录
4. 进入"API密钥"页面
5. 点击"创建密钥"
6. 复制Key并填入 `.env` 文件

---

## 快速验证

服务启动后，测试以下请求：

```bash
# 健康检查
curl http://localhost:8000/health

# 检索文献
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "diabetes treatment SGLT2",
    "max_results": 3,
    "generate_summary": true
  }'

# 快速检索
curl "http://localhost:8000/api/v1/search/quick?query=COVID-19%20vaccine&max_results=2"
```

---

## 常见问题

### Q: pip命令找不到？
A: 尝试 `python -m pip install` 或使用Python官方安装程序重新安装。

### Q: 依赖安装失败？
A: 确保Python版本 >= 3.9，升级pip: `python -m pip install --upgrade pip`

### Q: 端口8000被占用？
A: 修改 `.env` 文件中的 `PORT` 值，或使用 `python test_main.py` 后指定端口。

### Q: KnowS API报错？
A: 检查 `.env` 中的 `KNOWS_API_KEY` 是否正确，确保网络连接正常。

---

## 下一步

1. ✅ 本地测试通过 → 申请StepFun Key → 切换到真实API
2. ✅ 创建GitHub仓库 → 推送到GitHub
3. ✅ 魔搭社区部署 → 获取公开链接
4. ✅ 飞书表单登记 → 完成作品提交

有任何问题，随时在官方群提问！
