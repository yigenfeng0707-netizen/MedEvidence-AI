"""
阶跃星辰 StepFun API客户端 - 模拟版本（用于测试）
实际使用时请替换为 stepfun_client.py
"""
from typing import Dict, List, Any
import random


class StepFunClientMock:
    """StepFun大模型API客户端 - 模拟版本"""
    
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or "mock_key"
        self.model = model or "step-1-flash"
        print("[MOCK] StepFun Client initialized (模拟模式)")
    
    async def translate_and_summarize(self, title: str, abstract: str, language: str = "zh") -> Dict[str, str]:
        """模拟翻译和摘要生成"""
        # 生成模拟的中文标题
        title_keywords = {
            "diabetes": "糖尿病",
            "treatment": "治疗",
            "efficacy": "疗效",
            "safety": "安全性",
            "clinical": "临床",
            "trial": "试验",
            "meta-analysis": "Meta分析",
            "review": "综述",
            "patients": "患者",
            "study": "研究",
            "renal": "肾脏",
            "protection": "保护",
            "cardiovascular": "心血管",
            "outcomes": "结局",
            "inhibitors": "抑制剂"
        }
        
        # 简单的关键词替换模拟翻译
        title_zh = title
        for en, zh in title_keywords.items():
            title_zh = title_zh.replace(en, zh)
        
        # 生成模拟摘要（取前100字+省略号）
        abstract_zh = f"本研究探讨了相关医学问题。研究纳入了大量患者，经过统计分析发现显著的治疗效果。结论支持该治疗方案在临床实践中的应用。"
        
        # 生成模拟临床意义
        clinical_significance = f"临床意义：本研究为临床实践提供了重要证据。建议医生在合适的患者中考虑使用该治疗方案，同时注意监测不良反应。"
        
        print(f"[MOCK] Generated translation for: {title[:50]}...")
        
        return {
            "title_zh": title_zh if title_zh != title else f"【中文标题】{title[:50]}...",
            "abstract_zh": abstract_zh,
            "clinical_significance": clinical_significance
        }
    
    async def generate_overall_summary(self, query: str, results: List[Dict[str, Any]]) -> str:
        """模拟生成整体摘要"""
        summaries = [
            f"基于检索结果，当前关于「{query}」的证据主要来自高质量研究。证据显示该领域已有较为充分的临床研究支持，但仍需更多长期随访数据。",
            f"检索到多项相关研究，证据等级以RCT和Meta分析为主。整体而言，该治疗方案显示出良好的疗效和可接受的安全性 profile。",
            f"现有证据表明，该主题在医学界受到广泛关注。多项高质量研究支持其临床应用，但个体差异和长期效果仍需进一步研究。"
        ]
        return random.choice(summaries)
    
    async def generate_clinical_takeaway(self, query: str, top_results: List[Dict[str, Any]]) -> str:
        """模拟生成临床要点"""
        takeaways = [
            "推荐等级：强。基于现有高质量证据，建议在符合条件的患者中优先使用该治疗方案。",
            "推荐等级：中等。现有证据支持该方案的有效性，但需结合患者个体情况综合考虑。",
            "推荐等级：弱。初步证据显示潜在获益，建议在有经验的医生指导下谨慎使用。"
        ]
        return random.choice(takeaways)


# 别名，方便切换
StepFunClient = StepFunClientMock
