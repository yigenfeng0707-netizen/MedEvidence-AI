# MedEvidence AI - 演示数据与素材包

本文档包含演示视频所需的所有真实数据和素材说明。

---

## 📊 真实演示数据（线上API获取）

### 示例1：中文查询 "Meta分析 抗生素"

**请求：**
```json
{
  "query": "Meta分析 抗生素",
  "max_results": 5,
  "generate_summary": false
}
```

**结果统计：**
- 总结果数：5篇
- Level 1 (Meta分析/系统评价)：5篇 (100%)
- 响应时间：约 1.8s
- 语言：中文

**文献列表：**
1. 抗生素对免疫检查点抑制剂治疗非小细胞肺癌疗效影响的Meta分析 (Level 1)
2. 抗生素在种植治疗中的应用:早期种植失败的系统回顾和Meta分析与试验序贯分析 (Level 1)
3. 单一及联合应用抗生素治疗呼吸机相关性肺炎效果Meta分析 (Level 1)
4. 抗生素人工骨治疗慢性骨髓炎疗效和安全性的Meta分析 (Level 1)
5. 围手术期抗生素预防假体关节感染效果的Meta分析 (Level 1)

---

### 示例2：英文查询 "COVID-19 vaccine randomized trial"

**请求：**
```json
{
  "query": "COVID-19 vaccine randomized trial",
  "max_results": 5,
  "generate_summary": false
}
```

**结果统计：**
- 总结果数：5篇
- Level 1 (随机对照试验)：5篇 (100%)
- 响应时间：约 3.7s
- 语言：英文

**文献列表：**
1. Randomized Trial of BCG Vaccine to Protect against Covid-19 (Level 1 - RCT)
2. Effect of 2 Inactivated SARS-CoV-2 Vaccines on Symptomatic COVID-19 (Level 1 - RCT)
3. Efficacy of the adjuvanted subunit protein COVID-19 vaccine, SCB-2019 (Level 1 - RCT)
4. Safety and Efficacy of the BNT162b2 mRNA Covid-19 Vaccine (Level 1 - RCT)
5. Efficacy and Safety of the mRNA-1273 SARS-CoV-2 Vaccine (Level 1 - RCT)

---

### 示例3：中文查询 "高血压治疗"

**结果统计：**
- 总结果数：5篇
- Level 3 (文献综述)：1篇
- Level 4 (临床指南/专家共识)：4篇
- 响应时间：约 2.7s

---

### 示例4：英文查询 "statins cardiovascular disease"

**结果统计：**
- 总结果数：5篇
- Level 1 (Meta分析)：5篇 (100%)
- 响应时间：约 4.9s

---

## 🏆 证据等级配色方案

| 等级 | 中文名称 | 颜色HEX | 用途 |
|------|----------|---------|------|
| Level 1 | Meta分析/高质量RCT | #059669 | 绿色，金标准 |
| Level 2 | 低质量RCT | #10B981 | 绿色，高等级 |
| Level 3 | 队列研究/病例对照 | #F59E0B | 橙色，中等等级 |
| Level 4 | 病例系列/指南 | #F97316 | 深橙色，较低 |
| Level 5 | 个案报道/专家意见 | #EF4444 | 红色，最低 |

---

## 🎨 设计规范

### 主色调
- 主色（医疗蓝）：#2563EB
- 辅助色（浅蓝）：#60A5FA
- 强调色（青色）：#06B6D4
- 背景色（深色）：#0F172A
- 卡片背景：rgba(30, 41, 59, 0.8)

### 字体
- 中文：Noto Sans SC（思源黑体）
- 英文/代码：JetBrains Mono
- 标题字重：700-900
- 正文字重：400-500

### 动效
- 入场动画：fadeUp (0.6-1s, cubic-bezier)
- 卡片悬停：上移5px + 发光边框
- 加载：旋转环形进度条
- 转场：淡入淡出 / 滑动

---

## 📁 文件清单

| 文件 | 位置 | 用途 |
|------|------|------|
| demo-video-page.html | docs/ | 电影级演示页面（录屏用） |
| VIDEO_SCRIPT.md | docs/ | 逐字稿+分镜脚本 |
| subtitles_zh.srt | docs/ | 中文字幕 |
| subtitles_en.srt | docs/ | 英文字幕 |
| demo-data.md | docs/ | 本文档（演示数据） |

---

## 🔗 真实API测试命令

```bash
# 健康检查
curl https://gsym236998-medevidence-ai.ms.show/health

# 中文检索
curl -X POST https://gsym236998-medevidence-ai.ms.show/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Meta分析 抗生素","max_results":5,"generate_summary":false}'

# 英文检索
curl -X POST https://gsym236998-medevidence-ai.ms.show/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"COVID-19 vaccine randomized trial","max_results":5,"generate_summary":false}'
```
