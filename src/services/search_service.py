"""
医学文献检索核心服务
整合KnowS API + StepFun大模型能力
"""
import time
from typing import List, Dict, Any, Optional
from ..api.knows_client import KnowsClient
from ..api.stepfun_client import StepFunClient
from ..models.schemas import QueryRequest, SearchResponse, LiteratureResult
from ..utils.cache import cache


class SearchService:
    """检索服务"""
    
    def __init__(self):
        self.knows_client: Optional[KnowsClient] = None
        self.stepfun_client: Optional[StepFunClient] = None
    
    async def initialize(self):
        """初始化API客户端"""
        self.knows_client = KnowsClient()
        self.stepfun_client = StepFunClient()
    
    async def search(self, request: QueryRequest) -> SearchResponse:
        """
        执行文献检索
        
        Args:
            request: 检索请求
            
        Returns:
            检索响应
        """
        start_time = time.time()
        
        # 1. 调用KnowS API检索（返回已解析的 LiteratureResult 对象列表 + question_id）
        knows_result = await self.knows_client.search(
            query=request.query,
            max_results=request.max_results,
            year_from=request.year_from,
            year_to=request.year_to,
            evidence_levels=[e.value for e in request.evidence_levels] if request.evidence_levels else None
        )
        
        # 2. 结果整理与分布统计
        results: List[LiteratureResult] = knows_result.get("results", [])
        evidence_distribution: Dict[str, int] = {}
        
        for lit in results:
            level = lit.evidence_info.level.value
            evidence_distribution[level] = evidence_distribution.get(level, 0) + 1
        
        # 3. 生成智能摘要（使用StepFun）
        summary = None
        clinical_takeaway = None
        
        if request.generate_summary and results:
            # 为每篇文献生成中文摘要
            for lit in results[:5]:  # 只为前5篇生成，控制成本
                if lit.abstract:
                    translation = await self.stepfun_client.translate_and_summarize(
                        title=lit.title,
                        abstract=lit.abstract
                    )
                    lit.title_zh = translation.get("title_zh")
                    lit.abstract_zh = translation.get("abstract_zh")
                    lit.clinical_significance = translation.get("clinical_significance")
            
            # 生成整体摘要
            results_dict = [r.model_dump() for r in results[:10]]
            summary = await self.stepfun_client.generate_overall_summary(
                query=request.query,
                results=results_dict
            )
            
            # 生成临床要点
            clinical_takeaway = await self.stepfun_client.generate_clinical_takeaway(
                query=request.query,
                top_results=results_dict[:3]
            )
        
        search_time = int((time.time() - start_time) * 1000)
        
        return SearchResponse(
            query=request.query,
            original_query=request.query,
            results_count=len(results),
            evidence_distribution=evidence_distribution,
            results=results,
            summary=summary,
            clinical_takeaway=clinical_takeaway,
            search_time_ms=search_time,
            cached=False
        )
    
    async def close(self):
        """关闭服务"""
        if self.knows_client:
            await self.knows_client.close()
