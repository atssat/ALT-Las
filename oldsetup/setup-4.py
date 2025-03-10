import os

def create_project():
    project_root = "alT-Las_Project"

    # 📂 Gerekli dizinleri oluştur
    directories = [
        os.path.join(project_root, "ai_models"),
        os.path.join(project_root, "gui"),
        os.path.join(project_root, "api_management"),
        os.path.join(project_root, "automation"),
        os.path.join(project_root, "logs"),
        os.path.join(project_root, "cpp_modules"),
        os.path.join(project_root, "plugins"),
        os.path.join(project_root, "docs")
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # 📌 Ana Uygulama Dosyası
    alT_Las_content = r'''# -*- coding: utf-8 -*-
"""
Ana uygulama dosyası: alT-Las
Python tabanlı AI destekli masaüstü asistanı.
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.interface import MainWindow
from api_management.api_handler import APIHandler
from automation.macro_manager import MacroManager
from ai_models.openai_model import OpenAIModel
from utils.logger import log_info

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    log_info("alT-Las başlatıldı.")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
'''
    with open(os.path.join(project_root, "alT_Las.py"), "w", encoding="utf-8") as f:
        f.write(alT_Las_content)

    # 📌 Yapay Zeka Modülü (OpenAI Örneği)
    openai_model_content = r'''# -*- coding: utf-8 -*-
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
'''
    with open(os.path.join(project_root, "ai_models", "openai_model.py"), "w", encoding="utf-8") as f:
        f.write(openai_model_content)

    # 📌 Debug Arayüzü
    debug_ui_content = r'''# -*- coding: utf-8 -*-
"""
Gelişmiş Debug Arayüzü (Ekran Görüntüsü, API Logları, Mikrofon Kaydı)
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class DebugUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.log_label = QLabel("Loglar buraya gelecek...")
        self.screenshot_button = QPushButton("Ekran Görüntüsü Al")
        self.api_log_button = QPushButton("API Loglarını Gör")

        layout.addWidget(self.log_label)
        layout.addWidget(self.screenshot_button)
        layout.addWidget(self.api_log_button)

        self.setLayout(layout)
        self.setWindowTitle("Debug Arayüzü")
        self.setGeometry(100, 100, 400, 300)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    debug_window = DebugUI()
    debug_window.show()
    sys.exit(app.exec_())
'''
    with open(os.path.join(project_root, "gui", "debug_ui.py"), "w", encoding="utf-8") as f:
        f.write(debug_ui_content)

    # 📌 Logger Modülü
    logger_content = r'''# -*- coding: utf-8 -*-
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def log_info(message):
    logging.info(message)

def log_error(message, exc_info=False):
    logging.error(message, exc_info=exc_info)

def log_debug(message):
    logging.debug(message)

def log_performance(message):
    logging.info(message)
'''
    with open(os.path.join(project_root, "logs", "logger.py"), "w", encoding="utf-8") as f:
        f.write(logger_content)

    # 📌 CUDA Kontrolü
    cuda_helper_content = r'''# -*- coding: utf-8 -*-
try:
    import torch
    def is_cuda_available():
        return torch.cuda.is_available()
except ImportError:
    def is_cuda_available():
        return False

if __name__ == "__main__":
    print("CUDA Kullanılabilir mi?:", is_cuda_available())
'''
    with open(os.path.join(project_root, "cpp_modules", "cuda_helper.py"), "w", encoding="utf-8") as f:
        f.write(cuda_helper_content)

    # 📌 Plugin Sistemi
    plugin_interface_content = r'''# -*- coding: utf-8 -*-
class PluginInterface:
    def __init__(self):
        self.plugins = {}

    def 
