# MedEvidence AI

> 医学循证智能检索助手 - 用AI照亮医学研究的每一个角落

**一句话描述**：基于KnowS医学循证API的智能检索Skill，支持PubMed文献检索、循证分级、智能摘要和格式化导出

---

## 1. 项目简介与医疗场景

### 解决的痛点

在医学研究与临床实践中，医护人员和医学研究者面临以下核心痛点：

- **文献检索效率低**：PubMed等数据库检索需要专业检索式，普通医生难以快速找到高质量证据
- **信息过载**：检索结果动辄数百篇，缺乏有效的分级筛选机制
- **阅读成本高**：英文文献阅读耗时，关键信息提取困难
- **循证等级不清**：难以快速判断研究证据的可靠性和适用性

### 目标受众

- 👨‍⚕️ **临床医生**：快速获取最新诊疗指南和临床证据
- 👩‍🎓 **医学研究生**：文献调研和论文写作支持
- 🔬 **医学研究员**：系统性综述和Meta分析文献检索
- 📚 **医学生**：循证医学学习和病例讨论

### 核心价值主张

**"让循证医学触手可及"** - 通过AI技术降低医学文献检索门槛，提升医疗决策的证据质量。

---

## 2. 功能特性

### 核心功能

- ✅ **自然语言检索**：用中文/英文描述疾病/症状，自动转换为专业检索式
- ✅ **循证分级标注**：自动标注证据等级（Level 1: RCT/Meta分析 → Level 5: 专家意见）
- ✅ **智能摘要生成**：基于StepFun大模型生成中文临床意义摘要
- ✅ **多源数据整合**：集成KnowS医学循证API + PubMed开放接口
- ✅ **引用格式化**：支持APA、Vancouver、GB/T 7714等引用格式导出
- ✅ **相关文献推荐**：基于引用关系和内容相似度推荐相关研究

### 技术特色

- 🔒 **零患者数据**：仅检索公开学术文献，符合医疗合规要求
- ⚡ **RAG增强检索**：本地向量缓存加速重复查询
- 🌐 **多语言支持**：支持中英文混合检索和输出
- 📊 **循证可视化**：证据等级分布图表展示

---

## 3. 魔搭社区运行/部署指南

### 魔搭展示链接

> 🚀 **在线体验**：https://modelscope.cn/skills/MedEvidence-AI (待发布后更新)

### 本地运行步骤

#### 环境要求

- Python >= 3.9
- pip >= 21.0

#### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/your-username/MedEvidence-AI.git
cd MedEvidence-AI

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的API Keys
# KNOWS_API_KEY=your_knows_api_key_here
# STEPFUN_API_KEY=your_stepfun_api_key_here
```

#### 启动服务

```bash
# 开发模式
python src/main.py

# 或使用uvicorn
uvicorn src.main:app --reload --port 8000
```

#### 访问服务

- API文档：http://localhost:8000/docs
- 测试界面：http://localhost:8000/

### 魔搭社区部署

1. 访问 [魔搭Skill创建页面](https://modelscope.cn/skills/create?template=custom)
2. 上传代码仓库链接
3. 配置环境变量（API Keys）
4. 提交审核

---

## 4. 演示与输入输出示例

### 使用示例

#### 示例1：基础文献检索

**输入**：
```
检索关于"2型糖尿病患者使用SGLT2抑制剂的肾脏保护作用"的最新文献
```

**输出**：
```json
{
  "query": "SGLT2 inhibitors renal protection type 2 diabetes",
  "results_count": 42,
  "evidence_summary": {
    "level_1": 8,  // RCT/Meta分析
    "level_2": 15, // 队列研究
    "level_3": 12, // 病例对照
    "level_4": 7   // 病例系列
  },
  "top_results": [
    {
      "title": "SGLT2 inhibitors for primary and secondary prevention of cardiovascular and renal outcomes in type 2 diabetes",
      "journal": "The Lancet",
      "year": 2025,
      "pmid": "12345678",
      "evidence_level": "Level 1 - Meta分析",
      "abstract_zh": "本Meta分析纳入了12项RCT研究，共45,000名患者。结果显示SGLT2抑制剂可降低肾脏复合终点风险35%（HR 0.65, 95% CI 0.58-0.72），适用于糖尿病肾病的预防和延缓。",
      "clinical_significance": "强推荐：对于eGFR≥30的2型糖尿病患者，建议使用SGLT2抑制剂以保护肾功能。",
      "doi": "10.1016/S0140-6736(25)01234-5"
    }
  ]
}
```

#### 示例2：循证等级筛选

**输入**：
```
查找关于"新冠疫苗心肌炎风险"的高等级证据（仅RCT和队列研究）
```

**输出**：
```json
{
  "query": "COVID-19 vaccine myocarditis risk",
  "filter": "evidence_level:[1 TO 2]",
  "results_count": 18,
  "high_level_evidence": [
    {
      "evidence_level": "Level 1 - 大规模队列研究",
      "study_type": "Population-based cohort study",
      "sample_size": "2,400,000 vaccinated individuals",
      "key_finding": "mRNA疫苗后心肌炎发生率：每10万剂3.2例（95% CI 2.8-3.7）",
      "risk_comparison": "低于COVID-19感染导致的心肌炎风险（每10万剂16.5例）"
    }
  ],
  "clinical_takeaway": "疫苗相关心肌炎风险虽存在，但显著低于感染COVID-19本身的心肌炎风险。临床决策应基于风险-收益比进行综合评估。"
}
```

### 演示视频

📺 **完整演示视频**：[Bilibili/YouTube链接] (待上传)

---

## 5. 局限性与未来规划

### ⚠️ 当前版本局限性

**请务必了解以下限制，本工具不可替代专业医疗决策：**

1. **仅作参考，不做诊断**：本Skill提供的文献摘要和循证信息仅供医学专业人士参考，不构成诊断或治疗建议
2. **时效性限制**：文献更新可能存在延迟，最新研究可能尚未纳入数据库
3. **语言局限**：中文摘要由AI生成，可能存在翻译偏差，建议对照原文阅读
4. **循证分级自动化**：基于期刊影响因子、研究设计等自动判断，可能与人工专家判断存在差异
5. **数据库覆盖**：目前主要支持PubMed和KnowS数据库，中文文献覆盖有限

### 医疗合规声明

> **⚕️ 重要声明**：MedEvidence AI仅用于协助医学文献检索和信息整理，其输出不作为最终医疗诊断依据。临床决策应基于患者的具体情况、专业医生的判断和最新的临床指南。对于诊断和治疗方案，请务必咨询具有执业资质的医疗机构和医生。

### 🚀 未来规划

- **v2.0**（计划8月）：增加中文文献库（知网、万方）支持
- **v2.1**（计划9月）：引入知识图谱，支持疾病-药物-机制关联检索
- **v3.0**（计划10月）：增加个性化推荐，基于用户历史检索习惯优化结果
- **v3.5**（计划11月）：支持系统性综述半自动化生成

---

## 6. 团队与致谢

### 开发团队

- **核心开发者**：[你的名字]
- **医疗顾问**：[如有医生顾问，可添加]
- **测试志愿者**：[感谢社区贡献者]

### 特别致谢

- 🙏 **KnowS**：提供医学循证证据检索API支持
- 🙏 **阶跃星辰StepFun**：提供Flash Max/Pro大模型算力支持
- 🙏 **魔搭ModelScope社区**：提供Skill部署平台和赛事组织
- 🙏 **小X宝开源医疗社区**：提供医疗场景洞察和开源平台
- 🙏 **Sealos(FastGPT)**：提供RAG技术支持

### 开源协议

本项目采用 [Apache License 2.0](LICENSE) 开源协议。

### 联系我们

- 📧 Email: [your-email@example.com]
- 💬 微信/Discord: [联系方式]
- 🐛 Issue反馈: https://github.com/your-username/MedEvidence-AI/issues

### 引用本项目

如果您在学术工作中使用了本项目，请考虑引用：

```bibtex
@software{medevidence_ai_2026,
  title = {MedEvidence AI: Medical Evidence-Based Intelligent Search Skill},
  author = {[Your Name]},
  year = {2026},
  url = {https://github.com/your-username/MedEvidence-AI}
}
```

---

<div align="center">

**⭐ 如果本项目对您有帮助，请给我们一个Star！**

[GitHub Stars](https://github.com/your-username/MedEvidence-AI) | [问题反馈](https://github.com/your-username/MedEvidence-AI/issues)

---

🕯️ *光已成炬，照亮崎岖 | Light Turns Into Torches, Illuminating the Rugged Path*

</div>
