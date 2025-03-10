import torch
import logging

logger = logging.getLogger(__name__)

def is_cuda_available() -> bool:
    return torch.cuda.is_available()

def get_gpu_info() -> dict:
    info = {
        "cuda_available": is_cuda_available()
    }
    if is_cuda_available():
        info.update({
            "device_count": torch.cuda.device_count(),
            "current_device": torch.cuda.current_device(),
            "device_name": torch.cuda.get_device_name(),
            "memory_allocated": torch.cuda.memory_allocated() / (1024**2),  # MB
            "memory_cached": torch.cuda.memory_reserved() / (1024**2)  # MB
        })
    return info
