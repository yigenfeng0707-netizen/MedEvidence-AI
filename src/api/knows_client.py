"""
KnowS医学循证API客户端
文档: https://developers.nullht.com/api/reference/overview
"""
import os
import httpx
from typing import List, Optional, Dict, Any
from ..models.schemas import EvidenceLevel, LiteratureResult, EvidenceInfo, AuthorInfo


class KnowsClient:
    """KnowS API客户端"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("KNOWS_API_KEY")
        self.base_url = base_url or os.getenv("KNOWS_API_BASE", "https://api.nullht.com/v1")
        
        if not self.api_key:
            raise ValueError("KNOWS_API_KEY is required. Get it from https://developers.nullht.com/")
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def search(self, 
                     query: str,
                     max_results: int = 10,
                     year_from: Optional[int] = None,
                     year_to: Optional[int] = None,
                     evidence_levels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        搜索医学文献
        
        Args:
            query: 搜索关键词（支持中文/英文）
            max_results: 最大结果数
            year_from: 起始年份
            year_to: 截止年份
            evidence_levels: 证据等级筛选
            
        Returns:
            搜索结果字典
        """
        payload = {
            "query": query,
            "limit": max_results,
            "sources": ["pubmed", "guidelines", "clinical_trials"],
            "include_abstract": True,
            "include_full_text": False
        }
        
        if year_from:
            payload["year_from"] = year_from
        if year_to:
            payload["year_to"] = year_to
        if evidence_levels:
            payload["evidence_levels"] = evidence_levels
            
        response = await self.client.post("/search", json=payload)
        response.raise_for_status()
        return response.json()
    
    def _determine_evidence_level(self, item: Dict) -> EvidenceInfo:
        """
        根据文献类型确定证据等级
        
        Args:
            item: KnowS返回的文献数据
            
        Returns:
            证据信息
        """
        study_type = item.get("study_type", "").lower()
        pub_types = [pt.lower() for pt in item.get("publication_types", [])]
        
        # Level 1: Meta分析或RCT
        if "meta-analysis" in study_type or "systematic review" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_1_META,
                study_type="Meta分析",
                sample_size=item.get("sample_size")
            )
        
        if "randomized controlled trial" in pub_types or "rct" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_1_RCT,
                study_type="随机对照试验",
                sample_size=item.get("sample_size")
            )
        
        # Level 2: 队列研究或病例对照
        if "cohort" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_2_COHORT,
                study_type="队列研究",
                sample_size=item.get("sample_size"),
                follow_up=item.get("follow_up_duration")
            )
        
        if "case-control" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_2_CASE_CONTROL,
                study_type="病例对照研究",
                sample_size=item.get("sample_size")
            )
        
        # Level 3: 病例系列
        if "case series" in study_type or "case reports" in pub_types:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_3_CASE_SERIES,
                study_type="病例系列"
            )
        
        # Level 4: 专家意见/指南
        if "guideline" in study_type or "consensus" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_4_EXPERT,
                study_type="临床指南/专家共识"
            )
        
        # 默认为个案报道
        return EvidenceInfo(
            level=EvidenceLevel.LEVEL_5_ANECDOTAL,
            study_type="个案报道/观察性研究"
        )
    
    def _parse_literature(self, item: Dict) -> LiteratureResult:
        """解析单篇文献"""
        authors = [
            AuthorInfo(name=a.get("name", ""), affiliation=a.get("affiliation"))
            for a in item.get("authors", [])
        ]
        
        return LiteratureResult(
            pmid=str(item.get("pmid", "")),
            title=item.get("title", ""),
            authors=authors,
            journal=item.get("journal", ""),
            year=item.get("year", 0),
            doi=item.get("doi"),
            abstract=item.get("abstract"),
            keywords=item.get("keywords", []),
            evidence_info=self._determine_evidence_level(item),
            citation_count=item.get("citation_count"),
            relevance_score=item.get("relevance_score", 0.0),
            full_text_url=item.get("full_text_url")
        )
    
    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()
