from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QTextEdit
from BaseWindow import BaseWindow
from Scripts.EncryptFile import encrypt
from Scripts.EncryptDecryptFunctions import Load_public_key
from PySide6.QtCore import QObject, Signal


class Communicate(QObject):
    append_text = Signal(str)


class EncryptWindow(BaseWindow):
    file_path = None

    def __init__(self):
        super().__init__()
        super().initializeUI()

        self.comm = Communicate()
        self.comm.append_text.connect(self.appendText)
        layout = QVBoxLayout()
        self.setWindowTitle("Szyfrowanie dokumentu")

        self.fileButton = QPushButton("Wybierz plik do zaszyfrowania")
        self.fileButton.clicked.connect(self.open_file_dialog)

        self.keyButton = QPushButton("Wskaż klucz publiczny")
        self.keyButton.clicked.connect(self.key_file_dialog)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        layout.addWidget(self.keyButton)
        layout.addWidget(self.fileButton)
        layout.addWidget(self.console)

        self.setLayout(layout)
        self.appendText("Wskaż klucz publiczny, a następnie plik do zaszyfrowania o wielkości 5kB maksymalnie.")

    def closeEvent(self, event):
        super().closeEvent(event)

    def open_file_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik do zaszyfrowania")
        self.appendText("Wybrałeś dokument: " + str(self.file_path))
        encrypt(self.file_path, self)

    def key_file_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Wskaż klucz publiczny")
        self.appendText("Wybrałeś klucz: " + str(self.file_path))
        Load_public_key(self.file_path, self)

    def appendText(self, text):
        self.console.append(text)
