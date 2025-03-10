import psutil
import time
import torch
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GPUMonitor:
    def __init__(self):
        self.cuda_available = torch.cuda.is_available()
        
    def get_gpu_stats(self) -> Dict[str, Any]:
        if not self.cuda_available:
            return {"error": "CUDA not available"}
            
        try:
            return {
                "memory_used": torch.cuda.memory_allocated() / 1024**2,  # MB
                "memory_cached": torch.cuda.memory_reserved() / 1024**2,
                "device_name": torch.cuda.get_device_name(),
                "device_count": torch.cuda.device_count()
            }
        except Exception as e:
            logger.error(f"GPU stats error: {e}")
            return {"error": str(e)}

import psutil
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    return psutil.virtual_memory().percent

def measure_performance():
    return {
        'cpu': get_cpu_usage(),
        'memory': get_memory_usage(),
        'timestamp': time.time()
    }
