"""Module initialization"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
MODULES_DIR = Path(__file__).parent

# Core module imports
try:
    from .performance import get_cpu_usage, get_memory_usage, GPUMonitor
    from .screen_capture import ScreenCapture
    from .cuda_helper import is_cuda_available, get_gpu_info
    from .audio import AudioManager
    from .vision import VisionProcessor
    from .torch_utils import ModelManager
    from .fallbacks import *
except ImportError as e:
    logger.error(f"Module import error: {e}")
    from .fallbacks import *

__all__ = [
    'get_cpu_usage',
    'get_memory_usage',
    'GPUMonitor',
    'ScreenCapture',
    'is_cuda_available',
    'get_gpu_info',
    'AudioManager',
    'VisionProcessor',
    'ModelManager'
]
