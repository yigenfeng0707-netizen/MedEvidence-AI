"""
KnowS医学循证API客户端
文档: https://developers.nullht.com/api/docs
真实端点:
  - POST /v1/evidences/ai_search_paper_en  英文文献检索
  - POST /v1/evidences/ai_search_paper_cn  中文文献检索
  - POST /v1/evidences/ai_search_guide    指南检索
"""
import os
import re
import asyncio
import httpx
from typing import List, Optional, Dict, Any, Tuple
from ..models.schemas import EvidenceLevel, LiteratureResult, EvidenceInfo, AuthorInfo


def detect_language(text: str) -> str:
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    return "zh" if chinese_chars > 0 else "en"


def extract_keywords(query: str) -> List[str]:
    text = query.lower()
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
    words = [w for w in text.split() if len(w) > 1]
    chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', query)
    return list(set(words + chinese_words))


def calc_relevance_score(title: str, abstract: str, keywords: List[str]) -> float:
    if not keywords:
        return 0.5
    title_lower = (title or "").lower()
    abstract_lower = (abstract or "").lower()
    score = 0.0
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in title_lower:
            score += 3.0
        elif kw_lower in abstract_lower:
            score += 1.0
    for i, kw in enumerate(keywords):
        for kw2 in keywords[i+1:]:
            if kw.lower() in title_lower and kw2.lower() in title_lower:
                score += 2.0
    return score


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
        keywords = extract_keywords(query)
        lang = detect_language(query)
        all_evidences: List[Tuple[float, Dict[str, Any]]] = []
        question_id = ""
        seen_titles = set()

        async def collect(endpoint: str, search_query: str, limit: int, weight: float):
            nonlocal question_id
            try:
                resp = await self.client.post(endpoint, json={"query": search_query, "limit": limit})
                resp.raise_for_status()
                data = resp.json()
                if not question_id:
                    question_id = data.get("question_id", "")
                for ev in data.get("evidences", []):
                    title = (ev.get("title") or "").strip()
                    if not title or title in seen_titles:
                        continue
                    seen_titles.add(title)
                    abstract = ev.get("abstract") or ""
                    rel = calc_relevance_score(title, abstract, keywords)
                    if_factor = ev.get("impact_factor")
                    try:
                        if_val = float(if_factor) if if_factor is not None else 0.0
                    except (ValueError, TypeError):
                        if_val = 0.0
                    pub_date = ev.get("publish_date", "")
                    try:
                        year = int(pub_date[:4]) if pub_date and len(pub_date) >= 4 else 0
                    except (ValueError, TypeError):
                        year = 0
                    year_score = min(1.0, year / 2026.0) if year > 0 else 0
                    org_bonus = 1.0 if ev.get("organizations") else 0.0
                    total_score = rel * (1.0 + if_val / 20.0) * (0.8 + 0.2 * year_score) + weight + org_bonus
                    all_evidences.append((total_score, ev))
            except Exception:
                pass

        tasks = []
        per_limit = max(max_results * 2, 10)
        guide_limit = max(5, max_results)
        if lang == "zh":
            tasks.append(collect("/evidences/ai_search_paper_cn", query, per_limit, 2.0))
            tasks.append(collect("/evidences/ai_search_guide", query, guide_limit, 2.5))
        tasks.append(collect("/evidences/ai_search_paper_en", query, per_limit, 1.0))
        if lang != "zh":
            tasks.append(collect("/evidences/ai_search_guide", query, guide_limit, 1.5))

        await asyncio.gather(*tasks, return_exceptions=True)

        all_evidences.sort(key=lambda x: -x[0])

        results = []
        for score, item in all_evidences:
            lit = self._parse_literature(item)
            if score <= 0 and not item.get("organizations"):
                continue
            if year_from and lit.year and lit.year < year_from:
                continue
            if year_to and lit.year and lit.year > year_to:
                continue
            if evidence_levels and lit.evidence_info.level.value not in evidence_levels:
                continue
            results.append(lit)
            if len(results) >= max_results:
                break

        if not results and all_evidences:
            for _, item in all_evidences[:max_results]:
                results.append(self._parse_literature(item))

        return {"results": results, "question_id": question_id}

    def _determine_evidence_level(self, item: Dict) -> EvidenceInfo:
        study_type_raw = item.get("study_type") or ""
        study_type = study_type_raw.lower()
        title = item.get("title") or ""
        title_lower = title.lower()
        journal = (item.get("journal") or "").lower()
        organizations = item.get("organizations")

        if organizations:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_4_EXPERT,
                study_type="临床指南/专家共识"
            )

        cn_meta_keywords = ["meta分析", "荟萃分析", "系统评价", "系统综述", "meta 分析"]
        en_meta_keywords = ["meta-analysis", "meta analysis", "systematic review", "systematic overview", "evidence map", "evidence mapping"]
        if any(kw in title for kw in cn_meta_keywords) or any(kw in title_lower for kw in en_meta_keywords) or \
           "meta" in study_type or "meta分析" in study_type_raw:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_1_META,
                study_type="Meta分析/系统评价",
                sample_size=None
            )

        cn_guide_keywords = ["指南", "共识", "规范"]
        en_guide_keywords = ["clinical practice guideline", "practice guideline", "consensus statement", "clinical guideline"]
        if any(kw in title for kw in cn_guide_keywords) or any(kw in title_lower for kw in en_guide_keywords):
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_4_EXPERT,
                study_type="临床指南/专家共识"
            )

        cn_rct_keywords = ["随机对照", "随机双盲", "随机试验", "rct研究"]
        en_rct_keywords = ["randomized controlled", "randomised controlled", "randomized trial", "randomised trial", "rct"]
        if any(kw in title for kw in cn_rct_keywords) or any(kw in title_lower for kw in en_rct_keywords) or \
           "randomized" in study_type or "rct" in study_type or "随机对照" in study_type_raw:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_1_RCT,
                study_type="随机对照试验",
                sample_size=None
            )

        cn_cohort_keywords = ["队列研究", "前瞻性研究", "随访研究", "纵向研究"]
        en_cohort_keywords = ["cohort study", "cohort analysis", "prospective study", "longitudinal study", "follow-up study"]
        if any(kw in title for kw in cn_cohort_keywords) or any(kw in title_lower for kw in en_cohort_keywords) or \
           "cohort" in study_type or "队列" in study_type_raw:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_2_COHORT,
                study_type="队列研究",
                follow_up=None
            )

        cn_case_control_keywords = ["病例对照", "回顾性研究"]
        en_case_control_keywords = ["case-control", "case control", "retrospective study"]
        if any(kw in title for kw in cn_case_control_keywords) or any(kw in title_lower for kw in en_case_control_keywords) or \
           "case-control" in study_type or "病例对照" in study_type_raw:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_2_CASE_CONTROL,
                study_type="病例对照研究"
            )

        cn_review_keywords = ["综述", "研究进展", "进展", "回顾"]
        en_review_keywords = ["review", "narrative review", "literature review", "state of the art", "update"]
        top_review_journals = ["nature reviews", "cochrane", "annual review", "bmj", "lancet", "new england journal", "jama"]
        is_review_journal = any(j in journal for j in top_review_journals)
        if (any(kw in title for kw in cn_review_keywords) or any(kw in title_lower for kw in en_review_keywords) or
            "review" in study_type or "综述" in study_type_raw or is_review_journal):
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_3_CASE_SERIES,
                study_type="文献综述"
            )

        cn_case_keywords = ["病例报告", "病例分析", "个案"]
        en_case_keywords = ["case report", "case series", "case study"]
        if any(kw in title for kw in cn_case_keywords) or any(kw in title_lower for kw in en_case_keywords) or \
           "case" in study_type or "病例" in study_type_raw:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_3_CASE_SERIES,
                study_type="病例系列"
            )

        if "观察性研究" in study_type_raw:
            return EvidenceInfo(
                level=EvidenceLevel.LEVEL_5_ANECDOTAL,
                study_type="观察性研究/其他"
            )

        return EvidenceInfo(
            level=EvidenceLevel.LEVEL_5_ANECDOTAL,
            study_type="其他"
        )

    def _parse_literature(self, item: Dict) -> LiteratureResult:
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

        journal = item.get("journal", "")
        if not journal and item.get("organizations"):
            orgs = item.get("organizations")
            if isinstance(orgs, list) and orgs:
                journal = orgs[0] if isinstance(orgs[0], str) else str(orgs[0])
            elif isinstance(orgs, str):
                journal = orgs

        return LiteratureResult(
            pmid=str(item.get("id", "")),
            title=item.get("title", ""),
            authors=authors,
            journal=journal,
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
        await self.client.aclose()
