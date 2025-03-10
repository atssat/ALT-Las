import os
import sys

# 🛠 Python'u UTF-8 modunda çalıştırmaya zorla
sys.stdout.reconfigure(encoding='utf-8')

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
    main_app_content = """# -*- coding: utf-8 -*-
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
"""
    with open(os.path.join(project_root, "alT_Las.py"), "w", encoding="utf-8") as f:
        f.write(main_app_content)

    # 📌 Yapay Zeka Modülü (OpenAI Örneği)
    openai_model_content = """# -*- coding: utf-8 -*-
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
"""
    with open(os.path.join(project_root, "ai_models", "openai_model.py"), "w", encoding="utf-8") as f:
        f.write(openai_model_content)

    # 📌 Logger Modülü
    logger_content = """# -*- coding: utf-8 -*-
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def log_info(message):
    logging.info(message)

def log_error(message, exc_info=False):
    logging.error(message, exc_info=exc_info)

def log_debug(message):
    logging.debug(message)
"""
    with open(os.path.join(project_root, "logs", "logger.py"), "w", encoding="utf-8") as f:
        f.write(logger_content)

    print("Tüm proje dosyaları başarıyla oluşturuldu.")

if __name__ == "__main__":
    create_project()
