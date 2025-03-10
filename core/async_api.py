import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)

class AsyncAPIHandler:
    def __init__(self, timeout: int = 30):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        self.queue = asyncio.Queue()
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context")
            
        try:
            async with self.session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"API request error: {e}", exc_info=True)
            raise
