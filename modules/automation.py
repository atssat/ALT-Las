import pyautogui
import keyboard
import json
import logging
from threading import Thread
from typing import List, Dict

logger = logging.getLogger(__name__)

class AutomationController:
    def __init__(self):
        self.recording = False
        self.macro_data: List[Dict] = []
        self.current_macro = None
        
    def start_macro_recording(self):
        self.recording = True
        self.macro_data = []
        keyboard.hook(self._keyboard_callback)
        Thread(target=self._mouse_recorder, daemon=True).start()
        
    def stop_macro_recording(self):
        self.recording = False
        keyboard.unhook_all()
        
    def _keyboard_callback(self, event):
        if self.recording:
            self.macro_data.append({
                'type': 'keyboard',
                'key': event.name,
                'event': event.event_type
            })
            
    def _mouse_recorder(self):
        last_pos = pyautogui.position()
        while self.recording:
            pos = pyautogui.position()
            if pos != last_pos:
                self.macro_data.append({
                    'type': 'mouse',
                    'position': (pos.x, pos.y)
                })
                last_pos = pos
                
    def save_macro(self, name: str):
        try:
            with open(f'macros/{name}.json', 'w') as f:
                json.dump(self.macro_data, f)
            return True
        except Exception as e:
            logger.error(f"Failed to save macro: {e}")
            return False
            
    def load_macro(self, name: str):
        try:
            with open(f'macros/{name}.json', 'r') as f:
                self.current_macro = json.load(f)
            return True
        except Exception as e:
            logger.error(f"Failed to load macro: {e}")
            return False
