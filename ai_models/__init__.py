"""AI Models package initialization"""
import logging
from typing import Dict, Any
import importlib

logger = logging.getLogger(__name__)

AVAILABLE_MODELS = {
    'openai': 'openai_py.OpenAIClient',
    'google': 'google_ai.GoogleAIClient',
    'cohere': 'cohere_ai.CohereClient',
    'ai21': 'ai21labs_ai.AI21Client',
    'deepseek': 'deepseek_ai.DeepSeekClient'
}

class AIModelFactory:
    _instances: Dict[str, Any] = {}
    
    @classmethod
    def get_model(cls, model_name: str):
        if model_name not in cls._instances:
            try:
                if model_name in AVAILABLE_MODELS:
                    module_path, class_name = AVAILABLE_MODELS[model_name].split('.')
                    module = importlib.import_module(f'.{module_path}', package='ai_models')
                    model_class = getattr(module, class_name)
                    cls._instances[model_name] = model_class()
                    logger.info(f"Successfully initialized {model_name} model")
            except ImportError as e:
                logger.error(f"Failed to import {model_name} model: {e}")
                return None
            except Exception as e:
                logger.error(f"Error initializing {model_name} model: {e}")
                return None
                
        return cls._instances.get(model_name)

# Initialize available models
available_models = {name: AIModelFactory.get_model(name) is not None 
                   for name in AVAILABLE_MODELS}

logger.info(f"Available AI models: {[k for k,v in available_models.items() if v]}")
