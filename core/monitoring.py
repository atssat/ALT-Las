import psutil
import numpy as np
from threading import Thread
from queue import Queue
import logging
import torch
import GPUtil

logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self, update_callback=None):
        self._running = False
        self._callback = update_callback
        self._data_queue = Queue(maxsize=100)
        self._gpu_monitor = GPUMonitor()
        
    def start(self):
        if not self._running:
            self._running = True
            Thread(target=self._monitor_loop, daemon=True).start()
            self._gpu_monitor.start()
            
    def stop(self):
        self._running = False
        self._gpu_monitor.stop()
        
    def _monitor_loop(self):
        while self._running:
            try:
                cpu = psutil.cpu_percent()
                mem = psutil.virtual_memory().percent
                gpu_stats = self._gpu_monitor.stats
                
                if self._data_queue.full():
                    self._data_queue.get()
                self._data_queue.put((cpu, mem, gpu_stats))
                
                if self._callback:
                    self._callback(cpu, mem, gpu_stats)
                    
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                
            time.sleep(1)

class GPUMonitor:
    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.running = False
        self.stats: Dict[str, Any] = {}
        self._monitor_thread = None
        
    def start(self):
        if not self.running:
            self.running = True
            self._monitor_thread = Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
    
    def stop(self):
        self.running = False
        if self._monitor_thread:
            self._monitor_thread.join()
    
    def _monitor_loop(self):
        while self.running:
            try:
                if torch.cuda.is_available():
                    self.stats = {
                        'gpu_util': GPUtil.getGPUs()[0].load * 100,
                        'memory_used': torch.cuda.memory_allocated() / 1024**2,
                        'memory_cached': torch.cuda.memory_reserved() / 1024**2,
                        'device_name': torch.cuda.get_device_name()
                    }
                    logger.debug(f"GPU Stats: {self.stats}")
            except Exception as e:
                logger.error(f"GPU monitoring error: {e}")
            
            time.sleep(self.update_interval)
