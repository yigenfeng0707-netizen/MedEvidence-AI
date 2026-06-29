"""
MedEvidence AI - 医学循证智能检索助手
FastAPI主应用入口
"""
import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .models.schemas import (
    QueryRequest,
    SearchResponse,
    HealthResponse,
    ErrorResponse,
)
from .services.search_service import SearchService

load_dotenv()

search_service = SearchService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：探活接口立即可用，客户端初始化放后台。"""
    init_task = asyncio.create_task(search_service.initialize())
    yield
    init_task.cancel()
    await search_service.close()


app = FastAPI(
    title="MedEvidence AI",
    description="医学循证智能检索助手 - 用AI照亮医学研究的每一个角落",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_ERROR",
            message=str(exc),
            details={"path": str(request.url)},
        ).model_dump(),
    )


@app.get("/")
async def root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "name": "MedEvidence AI",
        "version": "1.0.0",
        "description": "医学循证智能检索助手",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """魔搭探活接口：始终快速返回 200，避免启动期被判定失败。"""
    ready = search_service.is_ready()
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
        services={
            "api": True,
            "knows_api": ready and search_service.knows_client is not None,
            "stepfun_api": ready and search_service.stepfun_client is not None,
        },
    )


@app.post("/api/v1/search", response_model=SearchResponse)
async def search_literature(request: QueryRequest):
    try:
        return await search_service.search(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检索失败: {str(e)}")


@app.post("/api/v1/search/quick")
async def quick_search(query: str, max_results: int = 5):
    request = QueryRequest(
        query=query,
        max_results=max_results,
        generate_summary=True,
    )
    return await search_service.search(request)


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "7860"))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=debug,
    )
