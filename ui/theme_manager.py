from typing import Dict, Any
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ThemeManager:
    def __init__(self):
        self.themes_dir = Path(__file__).parent / 'themes'
        self.themes_dir.mkdir(exist_ok=True)
        self.current_theme = 'default'
        self.themes: Dict[str, Dict[str, Any]] = {
            'default': {
                'background': '#ffffff',
                'foreground': '#000000',
                'accent': '#007acc',
                'font': 'Segoe UI'
            },
            'dark': {
                'background': '#1e1e1e',
                'foreground': '#ffffff',
                'accent': '#0098ff',
                'font': 'Segoe UI'
            }
        }
        
    def load_theme(self, name: str) -> Dict[str, Any]:
        try:
            theme_file = self.themes_dir / f'{name}.json'
            if theme_file.exists():
                with open(theme_file) as f:
                    return json.load(f)
            return self.themes.get(name, self.themes['default'])
        except Exception as e:
            logger.error(f"Failed to load theme {name}: {e}")
            return self.themes['default']
