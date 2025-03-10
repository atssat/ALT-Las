# -*- coding: utf-8 -*-
import unittest
from ai_models.multi_api_manager import MultiAPIManager

class DummyAPI:
    def __init__(self, api_key):
        self.api_key = api_key
    async def get_response(self, session, prompt):
        return f"Dummy response for {prompt}"

class TestMultiAPIManager(unittest.TestCase):
    def setUp(self):
        config = {
            "enabled": True,
            "primary": {"type": "dummy", "api_key": "primary_key"},
            "task": {"type": "dummy", "api_key": "task_key"},
            "integration": {"type": "dummy", "api_key": "integration_key"}
        }
        class DummyMultiAPIManager(MultiAPIManager):
            def initialize_api(self, api_config):
                return DummyAPI(api_config.get("api_key", ""))
        self.manager = DummyMultiAPIManager(config)

    def test_process_input(self):
        responses = self.manager.process_input("Test")
        self.assertIn("Dummy response", responses["primary"])
        self.assertIn("Test", responses["task"])
        self.assertIn("Test", responses["integration"])

if __name__ == "__main__":
    unittest.main()
