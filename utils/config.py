import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Config:
    _instance = None
    _config = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config:
            self.load_config()
    
    def load_config(self):
        try:
            config_path = Path(__file__).parent.parent / 'config.json'
            if config_path.exists():
                with open(config_path) as f:
                    self._config = json.load(f)
        except Exception as e:
            logger.error(f"Config load error: {e}")
            self._config = {}
            
    @property
    def debug_mode(self):
        return self._config.get('debug', False)
        
    @property
    def performance_mode(self):
        return self._config.get('performance_mode', 'balanced')
