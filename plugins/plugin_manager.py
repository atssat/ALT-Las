import importlib.util
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.plugin_dir = Path(__file__).parent / 'modules'
        self.plugin_dir.mkdir(exist_ok=True)
        
    def load_plugin(self, name: str, path: str) -> bool:
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'setup') and hasattr(module, 'process'):
                    self.plugins[name] = module
                    module.setup()
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to load plugin {name}: {e}")
            return False
