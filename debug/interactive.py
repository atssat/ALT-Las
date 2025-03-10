import pdb
import ipdb
from functools import wraps
import logging
import traceback
import sys

logger = logging.getLogger(__name__)

def debug_on_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            if '--debug' in sys.argv:
                print(f"Debug session for error in {func.__name__}")
                ipdb.post_mortem()
            raise
    return wrapper

def set_trace():
    """Start interactive debugging session"""
    if '--debug' in sys.argv:
        ipdb.set_trace()
    return None
