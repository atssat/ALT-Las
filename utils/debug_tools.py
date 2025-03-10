import cProfile
import pstats
import logging
import line_profiler
import traceback
from functools import wraps
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from typing import Optional, Callable
import os

logger = logging.getLogger(__name__)

class DebugTools:
    def __init__(self, sentry_dsn: Optional[str] = None):
        self.debug_mode = False
        self.profiler = line_profiler.LineProfiler()
        
        if sentry_dsn:
            sentry_logging = LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[sentry_logging],
                traces_sample_rate=1.0,
                environment=os.getenv('ENV', 'development')
            )
    
    def set_debug_mode(self, enabled: bool):
        self.debug_mode = enabled
        if enabled:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
    
    def profile_function(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.debug_mode:
                return func(*args, **kwargs)
                
            profiler = cProfile.Profile()
            try:
                result = profiler.runcall(func, *args, **kwargs)
                stats = pstats.Stats(profiler)
                stats.sort_stats('cumulative')
                stats.print_stats()
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                logger.error(traceback.format_exc())
                sentry_sdk.capture_exception(e)
                raise
        return wrapper

    def line_profile(self, func: Callable) -> Callable:
        return self.profiler(func)
