"""
MedEvidence AI - 测试版本（使用模拟API）
用于本地测试和演示，无需真实API Key
"""
import os
import sys

# 强制使用模拟客户端
os.environ["USE_MOCK_API"] = "true"

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.models.schemas import QueryRequest, SearchResponse, HealthResponse, ErrorResponse
from src.api.knows_client_mock import KnowsClientMock
from src.api.stepfun_client_mock import StepFunClientMock


# 全局客户端
knows_client = None
stepfun_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global knows_client, stepfun_client
    knows_client = KnowsClientMock()
    stepfun_client = StepFunClientMock()
    print("\n" + "="*50)
    print("🩺 MedEvidence AI - 测试模式已启动")
    print("📌 使用模拟API，无需真实API Key")
    print("📖 访问 http://localhost:8000/docs 查看API文档")
    print("="*50 + "\n")
    yield
    print("\n关闭服务...")


app = FastAPI(
    title="MedEvidence AI (Test Mode)",
    description="医学循证智能检索助手 - 测试版本",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_ERROR",
            message=str(exc),
            details={"path": str(request.url)}
        ).model_dump()
    )


@app.get("/")
async def root():
    return {
        "name": "MedEvidence AI (Test Mode)",
        "version": "1.0.0",
        "mode": "MOCK",
        "description": "医学循证智能检索助手 - 模拟测试版本",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
        services={
            "api": True,
            "knows_api": knows_client is not None,
            "stepfun_api": stepfun_client is not None
        }
    )


@app.post("/api/v1/search", response_model=SearchResponse)
async def search_literature(request: QueryRequest):
    """
    医学文献检索接口（模拟版本）
    """
    import time
    start_time = time.time()
    
    try:
        # 1. 模拟KnowS检索
        knows_result = await knows_client.search(
            query=request.query,
            max_results=request.max_results,
            year_from=request.year_from,
            year_to=request.year_to,
            evidence_levels=[e.value for e in request.evidence_levels] if request.evidence_levels else None
        )
        
        # 2. 解析结果
        from typing import List, Dict, Any
        from src.models.schemas import LiteratureResult
        
        results: List[LiteratureResult] = []
        evidence_distribution: Dict[str, int] = {}
        
        for item in knows_result.get("results", []):
            lit = knows_client._parse_literature(item)
            results.append(lit)
            level = lit.evidence_info.level.value
            evidence_distribution[level] = evidence_distribution.get(level, 0) + 1
        
        # 3. 模拟StepFun摘要生成
        summary = None
        clinical_takeaway = None
        
        if request.generate_summary and results:
            for lit in results[:3]:
                if lit.abstract:
                    translation = await stepfun_client.translate_and_summarize(
                        title=lit.title,
                        abstract=lit.abstract
                    )
                    lit.title_zh = translation.get("title_zh")
                    lit.abstract_zh = translation.get("abstract_zh")
                    lit.clinical_significance = translation.get("clinical_significance")
            
            results_dict = [r.model_dump() for r in results[:5]]
            summary = await stepfun_client.generate_overall_summary(
                query=request.query,
                results=results_dict
            )
            clinical_takeaway = await stepfun_client.generate_clinical_takeaway(
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
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"检索失败: {str(e)}"
        )


@app.post("/api/v1/search/quick")
async def quick_search(query: str, max_results: int = 5):
    """快速检索接口"""
    request = QueryRequest(
        query=query,
        max_results=max_results,
        generate_summary=True
    )
    return await search_literature(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_main:app", host="0.0.0.0", port=8000, reload=True)
