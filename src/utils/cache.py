"""
缓存工具 - 使用内存缓存加速重复查询
"""
import hashlib
import json
import time
from typing import Optional, Any, Dict
from functools import wraps


class SimpleCache:
    """简单内存缓存"""
    
    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
    
    def _generate_key(self, *args, **kwargs) -> str:
        """生成缓存键"""
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key not in self.cache:
            return None
        
        item = self.cache[key]
        if time.time() - item["timestamp"] > self.ttl:
            del self.cache[key]
            return None
        
        return item["value"]
    
    def set(self, key: str, value: Any):
        """设置缓存值"""
        self.cache[key] = {
            "value": value,
            "timestamp": time.time()
        }
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
    
    def cached(self, ttl: Optional[int] = None):
        """缓存装饰器"""
        cache_ttl = ttl or self.ttl
        
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = self._generate_key(func.__name__, *args, **kwargs)
                
                # 尝试从缓存获取
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return {**cached_value, "cached": True}
                
                # 执行函数
                result = await func(*args, **kwargs)
                
                # 存入缓存
                if isinstance(result, dict):
                    self.set(cache_key, result)
                
                return result
            
            return wrapper
        return decorator


# 全局缓存实例
cache = SimpleCache(ttl=3600)  # 默认1小时缓存
