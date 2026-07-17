---
name: "modelscope-studio-manager"
description: "Manage ModelScope studios: read cookies, check status, restart, force rebuild, and health check. Invoke when automating ModelScope deployment, debugging 'no healthy upstream', or scheduling health checks for a ModelScope studio."
---

# ModelScope Studio Manager

管理魔搭创空间（ModelScope Studio）的完整工具链：读取本地 cookie、查询状态、调用 restart、强制重建、健康检查。适用于自动化部署、定时巡检、排查服务异常。

## 适用场景

出现以下情况时调用本 Skill：

- 需要自动化重启魔搭创空间
- 需要查询创空间当前状态（Running / Creating / Expired / Failed）
- 服务报 `no healthy upstream` 或 401，需要重新部署
- 需要把健康检查放到 GitHub Actions 等云端定时执行
- 需要读取 `~/.modelscope/credentials/cookies` 调用魔搭私有 API

## 核心能力

### 1. 读取魔搭 Cookie

魔搭 cookie 文件可能是 base64 文本或 pickle 二进制，必须兼容处理：

```python
import os
import base64
import pickle


def load_modelscope_cookie() -> str:
    """读取 ~/.modelscope/credentials/cookies，返回 'k=v; k2=v2' 字符串"""
    cookie_path = os.path.expanduser("~/.modelscope/credentials/cookies")
    if not os.path.exists(cookie_path):
        # 云端环境可从环境变量读取
        return os.getenv("MODELSCOPE_COOKIE", "")

    with open(cookie_path, "rb") as f:
        content = f.read()

    # 尝试 base64 文本
    try:
        decoded = base64.b64decode(content).decode("utf-8").strip()
        if decoded:
            return decoded
    except Exception:
        pass

    # 尝试 pickle 格式
    try:
        cookies = pickle.loads(content)
        return "; ".join([f"{k}={v}" for k, v in cookies.items()])
    except Exception:
        pass

    # 纯文本
    try:
        return content.decode("utf-8").strip()
    except Exception:
        return ""
```

### 2. 查询创空间状态

```python
import urllib.request
import json


def get_studio_status(owner: str, name: str, cookie: str) -> dict:
    url = f"https://www.modelscope.cn/api/v1/studio/{owner}/{name}"
    req = urllib.request.Request(
        url,
        headers={
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
    return data.get("Data", {})


def print_status(data: dict):
    print(f"Status: {data.get('Status')}")
    print(f"FailedMessage: {data.get('FailedMessage')}")
    print(f"DeployedTime: {data.get('DeployedTime')}")
    print(f"LastUpdatedTime: {data.get('LastUpdatedTime')}")
    print(f"ImageId: {data.get('ImageId')}")
    print(f"SdkVersion: {data.get('SdkVersion')}")
    print(f"Revision: {data.get('Revision')}")
```

### 3. 调用 Restart 重新部署

```python
def restart_studio(owner: str, name: str, cookie: str) -> dict:
    url = f"https://www.modelscope.cn/api/v1/studio/{owner}/{name}/restart"
    req = urllib.request.Request(
        url,
        data=json.dumps({}).encode(),
        headers={
            "Cookie": cookie,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": f"https://www.modelscope.cn/studios/{owner}/{name}/summary",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())
```

### 4. 强制重建（修改 SdkVersion / Revision）

当实例卡在 Creating 或需要强制拉取最新 GitHub commit 时使用：

```python
def force_rebuild(owner: str, name: str, cookie: str, revision: str, sdk_version: str = "6.17.3") -> dict:
    put_data = {
        "Name": name,
        "Owner": owner,
        "Visibility": 5,
        "DeployedByUser": True,
        "InstanceTypeName": "ecs.r7.large",
        "InstanceTypeId": 1,
        "InstanceNumber": 1,
        "DiskSize": 50,
        "SupportMobile": 0,
        "SdkVersion": sdk_version,
        "Revision": revision,
        "ExpiredMinutes": 0,
        "SupportWxMiniprogram": True,
        "ProtectedMode": 0,
        "ServerSideRender": False,
        "McpServer": False,
        "NeedLogin": False,
        "Type": "programmatic",
        "SdkType": "docker",
    }
    url = f"https://www.modelscope.cn/api/v1/studio/{owner}/{name}"
    req = urllib.request.Request(
        url,
        data=json.dumps(put_data).encode(),
        headers={
            "Cookie": cookie,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/0.5",
            "Accept": "application/json",
            "Referer": f"https://www.modelscope.cn/studios/{owner}/{name}/summary",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())
```

### 5. 获取 GitHub 最新 commit SHA

```python
def get_github_latest_commit(repo: str, token: str) -> str:
    url = f"https://api.github.com/repos/{repo}/commits/master"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
    return data["sha"]
```

### 6. 健康检查

```python
def health_check(service_url: str) -> bool:
    req = urllib.request.Request(
        f"{service_url}/health",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


def search_check(service_url: str, query: str = "diabetes", generate_summary: bool = False) -> bool:
    payload = json.dumps({
        "query": query,
        "max_results": 3,
        "generate_summary": generate_summary,
    }).encode()
    req = urllib.request.Request(
        f"{service_url}/api/v1/search",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status == 200
    except Exception:
        return False
```

## 完整示例：自动修复脚本

```python
"""
ModelScope Studio 自动巡检 + 修复脚本
用法: python modelscope_manager.py
"""
import json
import os
import time
import urllib.request
import urllib.error

OWNER = "your-owner"
NAME = "your-studio-name"
SERVICE_URL = f"https://{OWNER}-{NAME.lower()}.ms.show"


def load_cookie() -> str:
    """优先环境变量，其次本地文件"""
    env = os.getenv("MODELSCOPE_COOKIE", "").strip()
    if env:
        return env
    try:
        import base64, pickle
        path = os.path.expanduser("~/.modelscope/credentials/cookies")
        if not os.path.exists(path):
            return ""
        with open(path, "rb") as f:
            content = f.read()
        try:
            return base64.b64decode(content).decode("utf-8").strip()
        except Exception:
            cookies = pickle.loads(content)
            return "; ".join([f"{k}={v}" for k, v in cookies.items()])
    except Exception:
        return ""


def http_json(url: str, method: str = "GET", data: dict = None, headers: dict = None, timeout: int = 15) -> dict:
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("User-Agent", "Mozilla/5.0")
    req.add_header("Accept", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode("utf-8", errors="ignore")[:300]}


def main():
    cookie = load_cookie()
    if not cookie:
        print("无法获取魔搭 cookie")
        return 1

    # 1. 检查状态
    data = http_json(f"https://www.modelscope.cn/api/v1/studio/{OWNER}/{NAME}", headers={"Cookie": cookie})
    status = data.get("Data", {}).get("Status")
    print(f"当前状态: {status}")

    # 2. 检查服务健康
    healthy = health_check(SERVICE_URL)
    print(f"服务健康: {healthy}")

    if healthy and status == "Running":
        print("一切正常")
        return 0

    # 3. 调用 restart
    print("调用 restart...")
    result = http_json(
        f"https://www.modelscope.cn/api/v1/studio/{OWNER}/{NAME}/restart",
        method="PUT",
        data={},
        headers={
            "Cookie": cookie,
            "Content-Type": "application/json",
            "Referer": f"https://www.modelscope.cn/studios/{OWNER}/{NAME}/summary",
        },
    )
    print(f"restart 结果: {result}")
    return 0


if __name__ == "__main__":
    exit(main())
```

## GitHub Actions 云端巡检

将 `MODELSCOPE_COOKIE` 设为 GitHub Secret，每天自动巡检：

```yaml
name: ModelScope Studio Health Check

on:
  schedule:
    - cron: '0 1 * * *'  # 北京时间 09:00
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python modelscope_manager.py
        env:
          MODELSCOPE_COOKIE: ${{ secrets.MODELSCOPE_COOKIE }}
```

## 常见状态说明

| 状态 | 含义 | 处理方式 |
|------|------|----------|
| Running | 运行中 | 检查 /health 和 /api/v1/search |
| Creating | 正在创建 | 无法 stop/restart，只能等待或等 Expired 后重建 |
| Expired | 已过期 | 调用 restart 重新部署 |
| Failed | 部署失败 | 查看 FailedMessage 和日志，修正代码后 force rebuild |

## 注意事项

1. **Cookie 时效**：魔搭 cookie 会过期，需定期更新 GitHub Secret 或本地 cookie 文件
2. **不要泄露 cookie**：GitHub Secret 或本地文件保管，不要写进代码
3. **restart 对 Creating 无效**：实例在 Creating 状态时 API 无法操作，需等过期或联系平台
4. **端口问题**：ModelScope SDK 默认探活 7860，确保服务监听 7860
5. **GitHub token**：force rebuild 需要 GitHub token 读取最新 commit
