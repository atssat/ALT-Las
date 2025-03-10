import openai
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
            
    def initialize(self):
        if not self.api_key:
            raise ValueError("OpenAI API key not found")
        
    async def process(self, text: str, model: str = "gpt-4") -> str:
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[{"role": "user", "content": text}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Error: {str(e)}"

    def test_connection(self) -> bool:
        try:
            openai.Model.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False
