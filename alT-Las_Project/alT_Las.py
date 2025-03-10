# -*- coding: utf-8 -*-
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
