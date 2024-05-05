from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QTextEdit
from BaseWindow import BaseWindow
from Scripts.EncryptFile import decrypt
from Scripts.EncryptDecryptFunctions import Load_public_key
from PySide6.QtCore import QObject, Signal


class Communicate(QObject):
    append_text = Signal(str)


class DecryptWindow(BaseWindow):
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

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        layout.addWidget(self.fileButton)
        layout.addWidget(self.console)

        self.setLayout(layout)

    def closeEvent(self, event):
        super().closeEvent(event)

    def open_file_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik do odszyfrowania")
        self.appendText("Wybrałeś dokument: " + str(self.file_path))
        decrypt(self.file_path, self)


    def appendText(self, text):
        self.console.append(text)
