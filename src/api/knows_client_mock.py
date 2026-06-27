"""
KnowS API客户端 - 模拟版本（用于测试）
实际使用时请替换为 knows_client.py
"""
from typing import List, Optional, Dict, Any
import random
from ..models.schemas import EvidenceLevel, LiteratureResult, EvidenceInfo, AuthorInfo


class KnowsClientMock:
    """KnowS API客户端 - 模拟版本"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or "mock_key"
        self.base_url = base_url or "https://api.nullht.com/v1"
        print("[MOCK] KnowS Client initialized (模拟模式)")
    
    async def search(self, 
                     query: str,
                     max_results: int = 10,
                     year_from: Optional[int] = None,
                     year_to: Optional[int] = None,
                     evidence_levels: Optional[List[str]] = None) -> Dict[str, Any]:
        """模拟搜索医学文献"""
        
        # 根据查询关键词生成模拟结果
        sample_titles = [
            "Efficacy and safety of novel treatments in type 2 diabetes: A systematic review and meta-analysis",
            "Long-term outcomes of SGLT2 inhibitors in patients with chronic kidney disease: A randomized controlled trial",
            "Comparative effectiveness of different antihypertensive regimens: A multicenter cohort study",
            "Impact of lifestyle interventions on cardiovascular outcomes: Evidence from clinical trials",
            "Novel biomarkers for early detection of Alzheimer's disease: A prospective case-control study",
            "Safety profile of mRNA vaccines in elderly populations: Real-world evidence analysis",
            "Cost-effectiveness analysis of targeted therapy in oncology: A Markov model study",
            "Machine learning approaches for predicting hospital readmission: A retrospective cohort study"
        ]
        
        results = []
        for i in range(min(max_results, len(sample_titles))):
            # 随机确定证据等级
            level_types = [
                (EvidenceLevel.LEVEL_1_META, "Meta分析"),
                (EvidenceLevel.LEVEL_1_RCT, "随机对照试验"),
                (EvidenceLevel.LEVEL_2_COHORT, "队列研究"),
                (EvidenceLevel.LEVEL_2_CASE_CONTROL, "病例对照研究"),
                (EvidenceLevel.LEVEL_3_CASE_SERIES, "病例系列")
            ]
            level, study_type = random.choice(level_types)
            
            # 构建模拟文献数据
            item = {
                "pmid": f"1234567{i}",
                "title": sample_titles[i],
                "authors": [
                    {"name": f"Author {j}", "affiliation": f"University {j}"} 
                    for j in range(random.randint(2, 5))
                ],
                "journal": random.choice(["The Lancet", "NEJM", "JAMA", "BMJ", "Nature Medicine"]),
                "year": year_from or random.randint(2020, 2025),
                "doi": f"10.1000/example.{i}",
                "abstract": f"This study investigates {query}. A total of {random.randint(100, 1000)} patients were enrolled. Results showed significant improvements in primary outcomes (p<0.05). These findings support the clinical application of the intervention.",
                "keywords": query.split()[:5],
                "study_type": study_type,
                "sample_size": f"{random.randint(100, 5000)}",
                "publication_types": [study_type],
                "citation_count": random.randint(5, 500),
                "relevance_score": round(random.uniform(0.7, 0.95), 2),
                "full_text_url": f"https://pubmed.ncbi.nlm.nih.gov/1234567{i}/"
            }
            results.append(item)
        
        print(f"[MOCK] Search returned {len(results)} results for query: {query[:50]}...")
        
        return {"results": results, "total": len(results)}
    
    def _determine_evidence_level(self, item: Dict) -> EvidenceInfo:
        """确定证据等级"""
        study_type = item.get("study_type", "").lower()
        
        if "meta" in study_type:
            return EvidenceInfo(level=EvidenceLevel.LEVEL_1_META, study_type="Meta分析")
        elif "rct" in study_type or "randomized" in study_type:
            return EvidenceInfo(level=EvidenceLevel.LEVEL_1_RCT, study_type="随机对照试验", sample_size=item.get("sample_size"))
        elif "cohort" in study_type:
            return EvidenceInfo(level=EvidenceLevel.LEVEL_2_COHORT, study_type="队列研究", sample_size=item.get("sample_size"))
        elif "case-control" in study_type:
            return EvidenceInfo(level=EvidenceLevel.LEVEL_2_CASE_CONTROL, study_type="病例对照研究", sample_size=item.get("sample_size"))
        else:
            return EvidenceInfo(level=EvidenceLevel.LEVEL_3_CASE_SERIES, study_type="病例系列")
    
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
            year=item.get("year", 2020),
            doi=item.get("doi"),
            abstract=item.get("abstract"),
            keywords=item.get("keywords", []),
            evidence_info=self._determine_evidence_level(item),
            citation_count=item.get("citation_count"),
            relevance_score=item.get("relevance_score", 0.0),
            full_text_url=item.get("full_text_url")
        )
    
    async def close(self):
        """关闭客户端"""
        pass


# 别名，方便切换
KnowsClient = KnowsClientMock
