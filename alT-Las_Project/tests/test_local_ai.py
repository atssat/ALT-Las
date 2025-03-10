# -*- coding: utf-8 -*-
import unittest
from ai_models.local_ai import LocalAIAssistant

class TestLocalAI(unittest.TestCase):
    def setUp(self):
        self.ai = LocalAIAssistant(api_key="dummy_key")

    def test_response(self):
        response = self.ai.get_response("Test")
        self.assertIn("Yerel AI yanıtı", response)

if __name__ == "__main__":
    unittest.main()
