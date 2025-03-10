"""Fallback functions for missing dependencies"""

def dummy_cpu_usage():
    return 0

def dummy_memory_usage():
    return 0

def dummy_cuda_available():
    return False
