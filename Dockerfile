FROM python:3.11-slim

WORKDIR /app

# 强制设置uvicorn端口环境变量（uvicorn只认UVICORN_PORT，不认PORT）
ENV UVICORN_PORT=7860
ENV UVICORN_HOST=0.0.0.0
ENV PORT=7860
ENV HOST=0.0.0.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
