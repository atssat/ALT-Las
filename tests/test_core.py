import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.performance import get_cpu_usage, get_memory_usage, GPUMonitor
from modules.cuda_helper import is_cuda_available
from modules.torch_utils import ModelManager

class TestCore(unittest.TestCase):
    def test_performance_monitoring(self):
        cpu = get_cpu_usage()
        mem = get_memory_usage()
        self.assertIsInstance(cpu, (int, float))
        self.assertIsInstance(mem, (int, float))
        
    def test_gpu_monitoring(self):
        gpu_monitor = GPUMonitor()
        stats = gpu_monitor.get_gpu_stats()
        self.assertIsInstance(stats, dict)
        
    def test_cuda_availability(self):
        cuda_available = is_cuda_available()
        self.assertIsInstance(cuda_available, bool)

if __name__ == '__main__':
    unittest.main(verbosity=2)
