import os

project_root = "alT-Las_Project"

files = {
    # Test dosyaları: OpenAI modülü için
    os.path.join(project_root, "tests", "test_openai.py"): r'''# -*- coding: utf-8 -*-
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
''',

    # Test dosyaları: Yerel AI modülü için
    os.path.join(project_root, "tests", "test_local_ai.py"): r'''# -*- coding: utf-8 -*-
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
''',

    # Test dosyaları: RapidAPI modülü için
    os.path.join(project_root, "tests", "test_rapidapi.py"): r'''# -*- coding: utf-8 -*-
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
''',

    # Test dosyaları: Multi API Manager için
    os.path.join(project_root, "tests", "test_multi_api_manager.py"): r'''# -*- coding: utf-8 -*-
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
''',

    # Test dosyaları: Screen Control modülü için
    os.path.join(project_root, "tests", "test_screen_control.py"): r'''# -*- coding: utf-8 -*-
import unittest
from screen_control import capture_screen

class TestScreenControl(unittest.TestCase):
    def test_capture_screen(self):
        img = capture_screen()
        self.assertIsNotNone(img)

if __name__ == "__main__":
    unittest.main()
''',

    # C++ modülü derleme scripti (build.py)
    os.path.join(project_root, "cpp_modules", "screen_capture", "build.py"): r'''# -*- coding: utf-8 -*-
import subprocess
import platform
import os

def compile_cpp_module():
    """
    C++ modülünü derler.
    """
    source_file = "screen_capture.cpp"
    if platform.system() == "Windows":
        output_file = "screen_capture.dll"
        compile_command = [
            "g++",
            "-shared",
            "-o", output_file,
            source_file,
            "-I", ".",
            "-l", "gdiplus"
        ]
    elif platform.system() == "Linux":
        output_file = "screen_capture.so"
        compile_command = [
            "g++",
            "-shared",
            "-fPIC",
            "-o", output_file,
            source_file,
            "-I", ".",
            "-l", "Imlib2"
        ]
    elif platform.system() == "Darwin":
        output_file = "screen_capture.dylib"
        compile_command = [
            "g++",
            "-shared",
            "-o", output_file,
            source_file,
            "-I", ".",
            "-l", "Imlib2"
        ]
    else:
        print("İşletim sistemi desteklenmiyor.")
        return

    try:
        subprocess.run(compile_command, check=True)
        print(f"Derleme başarılı: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Derleme hatası: {e}")

if __name__ == "__main__":
    compile_cpp_module()
''',

    # Requirements.txt
    os.path.join(project_root, "requirements.txt"): r'''aiohttp
requests
PyQt5
opencv-python-headless
pyautogui
Pillow
mss
pybind11
pytest
coverage
'''
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Project")