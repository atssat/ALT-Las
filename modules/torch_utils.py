import torch
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models: Dict[str, Any] = {}
        
    def load_model(self, name: str, model_path: str) -> Optional[torch.nn.Module]:
        try:
            model = torch.load(model_path, map_location=self.device)
            self.models[name] = model
            return model
        except Exception as e:
            logger.error(f"Model load error: {e}")
            return None
            
    def get_device_info(self) -> Dict[str, Any]:
        info = {
            "device": str(self.device),
            "cuda_available": torch.cuda.is_available(),
        }
        if torch.cuda.is_available():
            info.update({
                "gpu_count": torch.cuda.device_count(),
                "current_device": torch.cuda.current_device(),
                "device_name": torch.cuda.get_device_name(),
                "memory_allocated": torch.cuda.memory_allocated(),
                "memory_cached": torch.cuda.memory_reserved()
            })
        return info
