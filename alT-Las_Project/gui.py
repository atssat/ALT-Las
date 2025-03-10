# -*- coding: utf-8 -*-
"""
alT-Las Projesi
GUI modülü
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('alT-Las')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.button = QPushButton('Gönder')
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def display_message(self, message, message_type="Info"):
        self.text_edit.append(f"{message_type}: {message}")