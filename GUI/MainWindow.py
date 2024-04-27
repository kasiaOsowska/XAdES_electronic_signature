from PySide6.QtWidgets import QPushButton, QVBoxLayout, QTextEdit
from PySide6.QtCore import QObject, Signal

import config
from SecondWindow import SecondWindow
from SigningWindow import SigningWindow
from BaseWindow import BaseWindow

class Communicate(QObject):
    append_text = Signal(str)

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.signing_button = None
        self.open_second_window_button = None
        self.print_button = None
        super().initializeUI()
        self.second_window = None
        self.signing_window = None

    def initializeUI(self):
        layout = QVBoxLayout()
        self.comm = Communicate()
        self.comm.append_text.connect(self.appendText)

        self.pendrive_button = QPushButton("Mam klucz na pendrivie")
        self.pendrive_button.clicked.connect(self.open_second_window)

        self.signing_button = QPushButton("Chce podpisać dokument")
        self.signing_button.clicked.connect(self.open_signing_window)

        self.open_second_window_button = QPushButton("Otwórz Drugie Okno")
        self.open_second_window_button.clicked.connect(self.open_signing_window)
        self.console = QTextEdit()
        self.console.setReadOnly(True)

        layout.addWidget(self.pendrive_button)
        layout.addWidget(self.signing_button)
        layout.addWidget(self.console)
       # layout.addWidget(self.open_second_window_button)

        self.setLayout(layout)

    def appendText(self, text):
        self.console.append(text)
    def open_second_window(self):
        if not self.second_window:
            self.second_window = SecondWindow()
        self.second_window.show()

    def open_signing_window(self):
        if config.PRIVATE_KEY is not None:
            if not self.signing_window:
                self.signing_window = SigningWindow()
            self.signing_window.show()
        else:
            self.console.append("Najpierw załaduj klucz prywatny")
