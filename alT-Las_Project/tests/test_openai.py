# -*- coding: utf-8 -*-
import unittest
from ai_models.openai_py import OpenAI
import aiohttp
import asyncio

class TestOpenAI(unittest.TestCase):
    def setUp(self):
        self.ai = OpenAI(api_key="test_key", api_settings={"endpoint": "", "model": "gpt-3.5-turbo"})

    def test_response(self):
        async def get():
            async with aiohttp.ClientSession() as session:
                return await self.ai.get_response(session, "Merhaba")
        response = asyncio.run(get())
        self.assertIsInstance(response, str)

if __name__ == "__main__":
    unittest.main()
