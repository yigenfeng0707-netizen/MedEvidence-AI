"""
MedEvidence AI - 医学循证智能检索助手
FastAPI主应用入口
"""
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# 加载 .env 环境变量
load_dotenv()
from datetime import datetime
from typing import Dict
import json
import threading
import urllib.request as urllib_req
from http.server import BaseHTTPRequestHandler, HTTPServer

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

from .models.schemas import (
    QueryRequest, SearchResponse, 
    HealthResponse, ErrorResponse
)
from .services.search_service import SearchService


# 全局服务实例
search_service = SearchService()


def _start_health_proxy():
    """
    仅在应用端口与健康检查端口不一致时启动代理（历史兼容）。
    当前配置已统一为7860，默认跳过。
    """
    target_port = int(os.getenv("APP_PORT", os.getenv("PORT", "7860")))
    proxy_port = int(os.getenv("HEALTH_PROXY_PORT", "7860"))
    if target_port == proxy_port:
        return

    class ProxyHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self._proxy("GET", None)

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else None
            self._proxy("POST", body)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def _proxy(self, method, body):
            try:
                url = f"http://127.0.0.1:{target_port}{self.path}"
                req = urllib_req.Request(
                    url,
                    data=body,
                    method=method,
                    headers={"Content-Type": self.headers.get("Content-Type", "application/json")}
                )
                with urllib_req.urlopen(req, timeout=30) as resp:
                    content = resp.read()
                    self.send_response(resp.status)
                    for key, value in resp.headers.items():
                        if key.lower() in ("content-type", "content-length"):
                            self.send_header(key, value)
                    self.end_headers()
                    self.wfile.write(content)
            except Exception as e:
                self.send_response(503)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"detail": f"upstream error: {str(e)}"}).encode())

        def log_message(self, format, *args):
            pass

    def run_server():
        server = HTTPServer(("0.0.0.0", proxy_port), ProxyHandler)
        server.serve_forever()

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    print(f"[HealthProxy] Started on port {proxy_port} -> {target_port}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    await search_service.initialize()
    # 启动7860端口健康检查代理
    _start_health_proxy()
    yield
    # 关闭时清理
    await search_service.close()


# 创建FastAPI应用
app = FastAPI(
    title="MedEvidence AI",
    description="医学循证智能检索助手 - 用AI照亮医学研究的每一个角落",
    version="1.0.0",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
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
    """根路径 - 返回前端页面"""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "name": "MedEvidence AI",
        "version": "1.0.0",
        "description": "医学循证智能检索助手",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    services_status = {
        "api": True,
        "knows_api": search_service.knows_client is not None,
        "stepfun_api": search_service.stepfun_client is not None
    }
    
    return HealthResponse(
        status="healthy" if all(services_status.values()) else "degraded",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
        services=services_status
    )


@app.post("/api/v1/search", response_model=SearchResponse)
async def search_literature(request: QueryRequest):
    """
    医学文献检索接口
    
    示例请求：
    ```json
    {
        "query": "SGLT2 inhibitors renal protection",
        "max_results": 10,
        "generate_summary": true
    }
    ```
    """
    try:
        result = await search_service.search(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"检索失败: {str(e)}"
        )


@app.post("/api/v1/search/quick")
async def quick_search(query: str, max_results: int = 5):
    """
    快速检索接口（简化版）
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    """
    request = QueryRequest(
        query=query,
        max_results=max_results,
        generate_summary=True
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
        reload=debug
    )
