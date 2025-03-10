# -*- coding: utf-8 -*-
import openai
from utils.logger import log_error

class OpenAIModel:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_response(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                api_key=self.api_key
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            log_error(f"OpenAI Hatası: {e}")
            return "AI işleminde hata oluştu."
