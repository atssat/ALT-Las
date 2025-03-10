import cProfile
import io
import pstats
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def profile_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        try:
            return profiler.runcall(func, *args, **kwargs)
        finally:
            s = io.StringIO()
            stats = pstats.Stats(profiler, stream=s)
            stats.strip_dirs().sort_stats('cumulative').print_stats(20)
            logger.debug(f"Performance profile for {func.__name__}:\n{s.getvalue()}")
    return wrapper

class MemoryOptimizer:
    @staticmethod
    def clear_image_cache(widget):
        """Clear image references to prevent memory leaks"""
        if hasattr(widget, 'image'):
            del widget.image
            
    @staticmethod
    def optimize_data_storage(data_list, max_size=1000):
        """Keep data structures within reasonable limits"""
        while len(data_list) > max_size:
            data_list.pop(0)
