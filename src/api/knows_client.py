"""
KnowS医学循证API客户端
文档: https://developers.nullht.com/api/docs
真实端点:
  - POST /v1/evidences/ai_search_paper_en  英文文献检索
  - POST /v1/evidences/ai_search_guide   指南检索
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
            timeout=60.0
        )

    async def search(self,
                     query: str,
                     max_results: int = 10,
                     year_from: Optional[int] = None,
                     year_to: Optional[int] = None,
                     evidence_levels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        搜索医学文献（优先使用 ai_search_paper_en + ai_search_guide

        Args:
            query: 搜索关键词（支持中文/英文）
            max_results: 最大结果数
            year_from: 起始年份
            year_to: 截止年份
            evidence_levels: 证据等级筛选

        Returns:
            搜索结果字典 {results: [...], question_id: str}
        """
        all_evidences = []
        question_id = ""

        try:
            paper_resp = await self._search_papers(query, max_results)
            question_id = paper_resp.get("question_id", "")
            all_evidences.extend(paper_resp.get("evidences", []))
        except Exception:
            pass

        try:
            guide_resp = await self._search_guides(query, max(3, max_results // 5))
            all_evidences.extend(guide_resp.get("evidences", []))
        except Exception:
            pass

        results = []
        for item in all_evidences:
            lit = self._parse_literature(item)

            if year_from and lit.year and lit.year < year_from:
                continue
            if year_to and lit.year and lit.year > year_to:
                continue
            if evidence_levels and lit.evidence_info.level.value not in evidence_levels:
                continue

            results.append(lit)
            if len(results) >= max_results:
                break

        return {"results": results, "question_id": question_id}

    async def _search_papers(self, query: str, limit: int) -> Dict[str, Any]:
        """调用英文文献检索端点"""
        resp = await self.client.post(
            "/evidences/ai_search_paper_en",
            json={"query": query, "limit": limit}
        )
        resp.raise_for_status()
        return resp.json()

    async def _search_guides(self, query: str, limit: int) -> Dict[str, Any]:
        """调用指南检索端点"""
        resp = await self.client.post(
            "/evidences/ai_search_guide",
            json={"query": query, "limit": limit}
        )
        resp.raise_for_status()
        return resp.json()

    def _determine_evidence_level(self, item: Dict) -> EvidenceInfo:
        """
        根据文献类型确定证据等级

        Args:
            item: KnowS返回的文献数据

        Returns:
            证据信息
        """
        study_type = (item.get("study_type") or "").lower()
        title = (item.get("title") or "").lower()
        organizations = item.get("organizations")

        if organizations:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_4_EXPERT,
                study_type="临床指南/专家共识"
            )

        if "meta" in study_type or "meta分析" in study_type or "systematic review" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_1_META,
                study_type=item.get("study_type", "Meta分析"),
                sample_size=None
            )

        if "randomized" in study_type or "rct" in study_type or "随机" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_1_RCT,
                study_type=item.get("study_type", "随机对照试验"),
                sample_size=None
            )

        if "cohort" in study_type or "队列" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_2_COHORT,
                study_type=item.get("study_type", "队列研究"),
                follow_up=None
            )

        if "case-control" in study_type or "病例对照" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_2_CASE_CONTROL,
                study_type=item.get("study_type", "病例对照研究")
            )

        if "review" in study_type or "综述" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_3_CASE_SERIES,
                study_type=item.get("study_type", "文献综述")
            )

        if "case" in study_type or "病例" in study_type:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_3_CASE_SERIES,
                study_type=item.get("study_type", "病例系列")
            )

        return EvidenceInfo(
            level=EvidenceLevel.LEVEL_5_ANECDOTAL,
            study_type=item.get("study_type", "观察性研究")
        )

    def _parse_literature(self, item: Dict) -> LiteratureResult:
        """解析单篇文献"""
        authors = []
        raw_authors = item.get("authors", [])
        if isinstance(raw_authors, list):
            for a in raw_authors:
                if isinstance(a, str):
                    authors.append(AuthorInfo(name=a))
                elif isinstance(a, dict):
                    authors.append(AuthorInfo(
                        name=a.get("name", ""),
                        affiliation=a.get("affiliation")
                    ))

        publish_date = item.get("publish_date", "")
        year = 0
        if publish_date and len(publish_date) >= 4:
            try:
                year = int(publish_date[:4])
            except (ValueError, TypeError):
                year = 0

        impact_factor = item.get("impact_factor")
        evidence_info = self._determine_evidence_level(item)
        if impact_factor and isinstance(impact_factor, (int, float)):
            evidence_info.quality_score = min(10.0, float(impact_factor) / 5.0)

        return LiteratureResult(
            pmid=str(item.get("id", "")),
            title=item.get("title", ""),
            authors=authors,
            journal=item.get("journal", ""),
            year=year,
            doi=item.get("doi"),
            abstract=item.get("abstract"),
            keywords=[],
            evidence_info=evidence_info,
            citation_count=None,
            relevance_score=0.0,
            full_text_url=None
        )

    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()
