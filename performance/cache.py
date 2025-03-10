import time
from typing import Dict, Any, Optional
import logging
from threading import Lock

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, max_size: int = 1000, cleanup_interval: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()
        self._lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if self._should_cleanup():
                self._cleanup()
                
            if key in self._cache:
                item = self._cache[key]
                if time.time() < item['expires']:
                    return item['value']
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        with self._lock:
            if len(self._cache) >= self._max_size:
                self._cleanup()
                
            self._cache[key] = {
                'value': value,
                'expires': time.time() + ttl,
                'created': time.time()
            }
    
    def _should_cleanup(self) -> bool:
        return time.time() - self._last_cleanup > self._cleanup_interval
    
    def _cleanup(self):
        now = time.time()
        expired = [k for k, v in self._cache.items() if v['expires'] <= now]
        for key in expired:
            del self._cache[key]
        self._last_cleanup = now
        
        logger.debug(f"Cache cleanup: removed {len(expired)} items")
