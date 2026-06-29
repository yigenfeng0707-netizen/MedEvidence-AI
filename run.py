"""
MedEvidence AI - 强制使用7860端口启动
魔搭SDK启动uvicorn时不带--port参数，uvicorn默认用8000
此脚本确保服务始终监听7860端口
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=7860,
        reload=False,
        log_level="info"
    )
