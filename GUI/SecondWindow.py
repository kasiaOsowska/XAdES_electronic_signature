from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from BaseWindow import BaseWindow
from Scripts.ReadingPrivateKey import decrypt_key_async, decrypt_key

class Communicate(QObject):
    append_text = Signal(str)


class SecondWindow(BaseWindow):
    PIN_confirmed = False

    def __init__(self):
        super().__init__()
        super().initializeUI()

        layout = QVBoxLayout()
        self.comm = Communicate()
        self.comm.append_text.connect(self.appendText)

        self.setWindowTitle("Pobieranie klucza z pendrive")

        self.line_edit = QLineEdit()
        confirm_button = QPushButton("Potwierdź PIN")
        confirm_button.clicked.connect(self.change_PIN_confirmed)
        self.console = QTextEdit()
        self.console.setReadOnly(True)

        layout.addWidget(self.console)
        layout.addWidget(self.line_edit)
        layout.addWidget(confirm_button)

        self.setLayout(layout)
        decrypt_key_async(self)

    def change_PIN_confirmed(self):
        decrypt_key(self)

    def appendText(self, text):
        self.console.append(text)

    def get_PIN(self):
        return self.line_edit.text()

    def closeEvent(self, event):
        self.console.clear()
        self.line_edit.clear()
        super().closeEvent(event)
