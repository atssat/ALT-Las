import torch
import logging
from typing import Dict, Any, List
import GPUtil
from threading import Thread
import time

logger = logging.getLogger(__name__)

class GPUMonitor:
    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.running = False
        self.stats: Dict[str, Any] = {}
        self._monitor_thread = None
        self._callbacks: List = []
        
    def start(self):
        if not self.running:
            self.running = True
            self._monitor_thread = Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
    
    def stop(self):
        self.running = False
        if self._monitor_thread:
            self._monitor_thread.join()
    
    def add_callback(self, callback):
        self._callbacks.append(callback)
        
    def _monitor_loop(self):
        while self.running:
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    self.stats.update({
                        f'gpu_{gpu.id}': {
                            'load': gpu.load * 100,
                            'memory_used': gpu.memoryUsed,
                            'memory_total': gpu.memoryTotal,
                            'temperature': gpu.temperature,
                            'uuid': gpu.uuid
                        }
                    })
                
                if torch.cuda.is_available():
                    for i in range(torch.cuda.device_count()):
                        self.stats[f'gpu_{i}'].update({
                            'torch_memory_allocated': torch.cuda.memory_allocated(i) / 1024**2,
                            'torch_memory_cached': torch.cuda.memory_reserved(i) / 1024**2
                        })
                
                for callback in self._callbacks:
                    callback(self.stats)
                    
            except Exception as e:
                logger.error(f"GPU monitoring error: {e}")
            
            time.sleep(self.update_interval)
