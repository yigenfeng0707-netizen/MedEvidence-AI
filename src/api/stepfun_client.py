"""
阶跃星辰 StepFun API客户端
StepFun API兼容OpenAI格式
文档: https://platform.stepfun.com/docs
"""
import os
from typing import Optional, List, Dict, Any
from openai import AsyncOpenAI


class StepFunClient:
    """StepFun大模型API客户端"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, 
                 model: Optional[str] = None):
        self.api_key = api_key or os.getenv("STEPFUN_API_KEY")
        self.base_url = base_url or os.getenv("STEPFUN_API_BASE", "https://api.stepfun.com/v1")
        self.model = model or os.getenv("STEPFUN_MODEL", "step-1-flash")
        
        if not self.api_key:
            raise ValueError("STEPFUN_API_KEY is required. Get it from https://platform.stepfun.com/")
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    async def translate_and_summarize(self, 
                                      title: str, 
                                      abstract: str,
                                      language: str = "zh") -> Dict[str, str]:
        """
        翻译并生成智能摘要
        
        Args:
            title: 文献标题
            abstract: 文献摘要
            language: 目标语言（默认中文）
            
        Returns:
            包含翻译标题、翻译摘要和临床意义摘要的字典
        """
        prompt = f"""你是一位专业的医学翻译和循证医学专家。请将以下医学文献标题和摘要翻译成中文，并生成临床意义摘要。

【原文标题】
{title}

【原文摘要】
{abstract}

请按以下格式输出：

【中文标题】
（翻译后的标题）

【中文摘要】
（翻译后的摘要，保持医学术语的准确性）

【临床意义】
（用2-3句话总结该研究对临床实践的启示，包括：1.主要发现 2.临床适用人群 3.实践建议）
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位精通医学英语和临床医学的资深医学专家，擅长翻译医学文献并提炼临床价值。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            return self._parse_response(content)
        except Exception:
            return {
                "title_zh": title,
                "abstract_zh": abstract,
                "clinical_significance": ""
            }
    
    def _parse_response(self, content: str) -> Dict[str, str]:
        """解析模型输出"""
        result = {
            "title_zh": "",
            "abstract_zh": "",
            "clinical_significance": ""
        }
        
        # 简单解析
        if "【中文标题】" in content:
            parts = content.split("【中文标题】")
            if len(parts) > 1:
                result["title_zh"] = parts[1].split("【")[0].strip()
        
        if "【中文摘要】" in content:
            parts = content.split("【中文摘要】")
            if len(parts) > 1:
                next_section = parts[1].find("【")
                if next_section > 0:
                    result["abstract_zh"] = parts[1][:next_section].strip()
                else:
                    result["abstract_zh"] = parts[1].strip()
        
        if "【临床意义】" in content:
            parts = content.split("【临床意义】")
            if len(parts) > 1:
                result["clinical_significance"] = parts[1].strip()
        
        return result
    
    async def generate_overall_summary(self, query: str, results: List[Dict[str, Any]]) -> str:
        """
        生成整体检索结果摘要
        
        Args:
            query: 用户查询
            results: 检索结果列表
            
        Returns:
            整体摘要文本
        """
        try:
            titles_and_abstracts = "\n\n".join([
                f"文献{i+1}: {r.get('title', '无标题')}\n摘要: {(r.get('abstract') or '无')[:300]}"
                for i, r in enumerate(results[:5])  # 只取前5篇
            ])
            
            prompt = f"""用户查询：{query}

检索到以下相关文献，请生成一个简洁的循证医学综述摘要：

{titles_and_abstracts}

请用2-3段话总结：
1. 当前证据的整体水平和质量
2. 主要研究发现和共识
3. 证据空白或争议点
4. 对临床实践的建议

要求：专业、简洁、基于证据，不超过300字。"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位循证医学专家，擅长系统综述和证据综合。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            return response.choices[0].message.content
        except Exception:
            return ""
    
    async def generate_clinical_takeaway(self, query: str, top_results: List[Dict[str, Any]]) -> str:
        """生成临床要点"""
        try:
            evidence_summary = "\n".join([
                f"- {(r.get('evidence_info') or {}).get('level', '未知')}: {r.get('title', '无标题')}"
                for r in top_results[:3]
            ])
            
            prompt = f"""基于以下高等级证据，生成临床决策要点：

查询主题：{query}

主要证据：
{evidence_summary}

请用1-2句话总结临床要点，格式如：
"推荐等级：强/中等/弱。临床决策建议：..."
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位临床医学专家，擅长循证医学和临床决策。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception:
            return ""
