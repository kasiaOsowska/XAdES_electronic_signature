from PySide6.QtWidgets import QPushButton, QVBoxLayout, QTextEdit
from PySide6.QtCore import QObject, Signal

import config
from SecondWindow import SecondWindow
from SigningWindow import SigningWindow
from VerifyWindow import VerifyWindow
from BaseWindow import BaseWindow
from DecryptWindow import DecryptWindow
from EncryptWindow import EncryptWindow

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
        self.verify_window = None
        self.encrypt_window = None
        self.decrypt_window = None

    def initializeUI(self):
        layout = QVBoxLayout()
        self.comm = Communicate()
        self.comm.append_text.connect(self.appendText)

        self.pendrive_button = QPushButton("Mam klucz na pendrivie")
        self.pendrive_button.clicked.connect(self.open_second_window)

        self.signing_button = QPushButton("Chcę podpisać dokument")
        self.signing_button.clicked.connect(self.open_signing_window)

        self.verify_window_button = QPushButton("Chcę zweryfikować podpis")
        self.verify_window_button.clicked.connect(self.open_verify_window)

        self.encrypt_window_button = QPushButton("Chcę zaszyfrować plik")
        self.encrypt_window_button.clicked.connect(self.open_encrypt_window)

        self.decrypt_window_button = QPushButton("Chcę odszyfrować plik")
        self.decrypt_window_button.clicked.connect(self.open_decrypt_window)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        layout.addWidget(self.pendrive_button)
        layout.addWidget(self.signing_button)
        layout.addWidget(self.verify_window_button)
        layout.addWidget(self.encrypt_window_button)
        layout.addWidget(self.decrypt_window_button)
        layout.addWidget(self.console)

        self.setLayout(layout)

    def appendText(self, text):
        self.console.append(text)
    def open_second_window(self):
        if not self.second_window:
            self.second_window = SecondWindow()
        self.second_window.show()

    def open_verify_window(self):
        if not self.verify_window:
            self.verify_window = VerifyWindow()
        self.verify_window.show()

    def open_encrypt_window(self):
        if not self.encrypt_window:
            self.encrypt_window = EncryptWindow()
        self.encrypt_window.show()

    def open_decrypt_window(self):
        if config.PRIVATE_KEY is not None:
            if not self.decrypt_window:
                self.decrypt_window = DecryptWindow()
            self.decrypt_window.show()
        else:
            self.console.append("Najpierw załaduj klucz prywatny")

    def open_signing_window(self):
        if config.PRIVATE_KEY is not None:
            if not self.signing_window:
                self.signing_window = SigningWindow()
            self.signing_window.show()
        else:
            self.console.append("Najpierw załaduj klucz prywatny")
