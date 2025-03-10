# -*- coding: utf-8 -*-
import unittest
from ai_models.rapidapi_module import RapidAPIManager

class TestRapidAPI(unittest.TestCase):
    def setUp(self):
        config = {
            "default_headers": {"X-RapidAPI-Key": "dummy", "X-RapidAPI-Host": "dummy"},
            "apis": {
                "default": {"endpoint": "https://dummyapi.com", "headers": {}}
            }
        }
        self.api = RapidAPIManager(config)

    def test_call_api(self):
        result = self.api.call_api("default", "/test")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
