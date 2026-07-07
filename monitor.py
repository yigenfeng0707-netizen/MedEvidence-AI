"""
MedEvidence-AI 健康监控脚本
用法: python monitor.py
功能: 检查服务健康状态，失败时自动尝试重启魔搭创空间
"""
import json
import os
import pickle
import time
import urllib.request

SERVICE_URL = "https://gsym236998-medevidence-ai.ms.show"
OWNER = "gsym236998"
NAME = "MedEvidence-AI"


def load_cookie() -> str:
    """读取魔搭cookie：优先环境变量，其次本地文件"""
    env_cookie = os.getenv("MODELSCOPE_COOKIE", "").strip()
    if env_cookie:
        return env_cookie

    cookie_path = os.path.expanduser("~/.modelscope/credentials/cookies")
    if not os.path.exists(cookie_path):
        return ""
    with open(cookie_path, "rb") as f:
        content = f.read()
    try:
        decoded = content.decode("utf-8").strip()
        if decoded:
            return decoded
    except Exception:
        pass
    try:
        cookies = pickle.loads(content)
        return "; ".join([f"{k}={v}" for k, v in cookies.items()])
    except Exception:
        return ""


def http_get(path: str, timeout: int = 30) -> tuple:
    """返回 (status, body)"""
    url = f"{SERVICE_URL}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        return r.status, r.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return -1, str(e)


def http_post(path: str, payload: dict, timeout: int = 60) -> tuple:
    """返回 (status, body)"""
    url = f"{SERVICE_URL}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        return r.status, r.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return -1, str(e)


def check_health() -> tuple:
    status, body = http_get("/health")
    if status == 200:
        try:
            data = json.loads(body)
            return True, data.get("status", "unknown")
        except Exception:
            return True, body[:100]
    return False, f"HTTP {status}: {body[:200]}"


def check_search(generate_summary: bool = False) -> tuple:
    payload = {
        "query": "SGLT2 inhibitors renal protection",
        "max_results": 3,
        "generate_summary": generate_summary,
    }
    status, body = http_post("/api/v1/search", payload, timeout=120)
    if status == 200:
        try:
            data = json.loads(body)
            return True, f"结果数={data.get('results_count')}, 摘要={bool(data.get('summary'))}"
        except Exception:
            return True, body[:100]
    return False, f"HTTP {status}: {body[:300]}"


def restart_modelscope() -> tuple:
    """调用魔搭restart API"""
    cookie = load_cookie()
    if not cookie:
        return False, "无法读取魔搭cookie，跳过自动重启"

    url = f"https://www.modelscope.cn/api/v1/studio/{OWNER}/{NAME}/restart"
    req = urllib.request.Request(
        url,
        data=json.dumps({}).encode(),
        headers={
            "Cookie": cookie,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": f"https://www.modelscope.cn/studios/{OWNER}/{NAME}/summary",
        },
        method="PUT",
    )
    try:
        r = urllib.request.urlopen(req, timeout=15)
        result = json.loads(r.read().decode())
        if result.get("Success"):
            return True, result.get("Message", "success")
        return False, result.get("Message", "unknown")
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return False, str(e)


def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] MedEvidence-AI 健康检查\n")

    results = []

    # 1. health
    ok, msg = check_health()
    results.append(("Health", ok, msg))
    print(f"1. Health: {'OK' if ok else 'FAIL'} - {msg}")

    # 2. search without summary
    ok, msg = check_search(generate_summary=False)
    results.append(("Search", ok, msg))
    print(f"2. Search: {'OK' if ok else 'FAIL'} - {msg}")

    # 3. search with summary
    ok, msg = check_search(generate_summary=True)
    results.append(("Search+Summary", ok, msg))
    print(f"3. Search+Summary: {'OK' if ok else 'FAIL'} - {msg}")

    all_ok = all(r[1] for r in results)

    if all_ok:
        print("\n✅ 所有检查通过，服务运行正常。")
        return 0

    print("\n⚠️ 检查失败，尝试自动重启魔搭创空间...")
    restarted, restart_msg = restart_modelscope()
    print(f"   自动重启: {'成功' if restarted else '失败'} - {restart_msg}")

    if restarted:
        print("   等待3分钟后重新检查...")
        time.sleep(180)
        print("\n--- 重新检查 ---")
        ok1, msg1 = check_health()
        print(f"Health: {'OK' if ok1 else 'FAIL'} - {msg1}")
        ok2, msg2 = check_search(generate_summary=False)
        print(f"Search: {'OK' if ok2 else 'FAIL'} - {msg2}")
        ok3, msg3 = check_search(generate_summary=True)
        print(f"Search+Summary: {'OK' if ok3 else 'FAIL'} - {msg3}")

        if ok1 and ok2 and ok3:
            print("\n✅ 自动修复成功，服务已恢复正常。")
            return 0

    print("\n❌ 自动修复失败，请手动访问以下链接点击"重新部署":")
    print(f"   https://www.modelscope.cn/studios/{OWNER}/{NAME}/summary")
    return 1


if __name__ == "__main__":
    exit(main())
