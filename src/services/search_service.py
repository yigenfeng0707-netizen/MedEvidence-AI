"""
医学文献检索核心服务
整合KnowS API + StepFun大模型能力
"""
import time
import logging
from typing import List, Dict, Any, Optional
from ..models.schemas import QueryRequest, SearchResponse, LiteratureResult
from ..utils.cache import cache

logger = logging.getLogger(__name__)


class SearchService:
    """检索服务"""
    
    def __init__(self):
        self.knows_client = None
        self.stepfun_client = None
    
    async def initialize(self):
        """初始化API客户端，支持mock模式降级"""
        try:
            from ..api.knows_client import KnowsClient
            self.knows_client = KnowsClient()
            logger.info("KnowS API客户端初始化成功")
        except Exception as e:
            logger.warning(f"KnowS API初始化失败，使用mock模式: {e}")
            from ..api.knows_client_mock import KnowsClientMock
            self.knows_client = KnowsClientMock()
        
        try:
            from ..api.stepfun_client import StepFunClient
            self.stepfun_client = StepFunClient()
            logger.info("StepFun API客户端初始化成功")
        except Exception as e:
            logger.warning(f"StepFun API初始化失败，使用mock模式: {e}")
            from ..api.stepfun_client_mock import StepFunClientMock
            self.stepfun_client = StepFunClientMock()
    
    async def search(self, request: QueryRequest) -> SearchResponse:
        """
        执行文献检索
        
        Args:
            request: 检索请求
            
        Returns:
            检索响应
        """
        start_time = time.time()
        
        knows_result = {}
        try:
            knows_result = await self.knows_client.search(
                query=request.query,
                max_results=request.max_results,
                year_from=request.year_from,
                year_to=request.year_to,
                evidence_levels=[e.value for e in request.evidence_levels] if request.evidence_levels else None
            )
        except Exception as e:
            logger.error(f"KnowS API error: {e}")
            knows_result = {"results": []}
        
        results: List[LiteratureResult] = knows_result.get("results", [])
        evidence_distribution: Dict[str, int] = {}
        
        for lit in results:
            try:
                level = lit.evidence_info.level.value
                evidence_distribution[level] = evidence_distribution.get(level, 0) + 1
            except Exception:
                evidence_distribution["未知"] = evidence_distribution.get("未知", 0) + 1
        
        summary = None
        clinical_takeaway = None
        
        if request.generate_summary and results and self.stepfun_client:
            try:
                for lit in results[:5]:
                    if lit.abstract:
                        try:
                            translation = await self.stepfun_client.translate_and_summarize(
                                title=lit.title,
                                abstract=lit.abstract
                            )
                            lit.title_zh = translation.get("title_zh")
                            lit.abstract_zh = translation.get("abstract_zh")
                            lit.clinical_significance = translation.get("clinical_significance")
                        except Exception as e:
                            logger.warning(f"Failed to translate/summarize article: {e}")
                
                results_dict = [r.model_dump() for r in results[:10]]
                
                try:
                    summary = await self.stepfun_client.generate_overall_summary(
                        query=request.query,
                        results=results_dict
                    )
                except Exception as e:
                    logger.warning(f"Failed to generate overall summary: {e}")
                
                try:
                    clinical_takeaway = await self.stepfun_client.generate_clinical_takeaway(
                        query=request.query,
                        top_results=results_dict[:3]
                    )
                except Exception as e:
                    logger.warning(f"Failed to generate clinical takeaway: {e}")
            
            except Exception as e:
                logger.error(f"StepFun API error during search: {e}")
        
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
