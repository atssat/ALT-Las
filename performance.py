import psutil
import numpy as np
from typing import Tuple

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent

def measure_array_performance(size: int) -> Tuple[float, float]:
    start_mem = psutil.Process().memory_info().rss
    arr = np.random.rand(size)
    end_mem = psutil.Process().memory_info().rss
    mem_used = (end_mem - start_mem) / 1024 / 1024  # MB
    
    cpu_usage = get_cpu_usage()
    return cpu_usage, mem_used

def get_performance_summary() -> dict:
    return {
        'cpu': get_cpu_usage(),
        'memory': get_memory_usage(),
        'timestamp': psutil.time.time()
    }

if __name__ == "__main__":
    print(f"CPU Usage: {get_cpu_usage()}%")
    print(f"Memory Usage: {get_memory_usage()}%")
    cpu, mem = measure_array_performance(1000000)
    print(f"Array Operation CPU Usage: {cpu}%")
    print(f"Array Operation Memory Usage: {mem:.2f} MB")
