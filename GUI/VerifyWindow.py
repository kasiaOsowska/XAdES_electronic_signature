from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QTextEdit
from BaseWindow import BaseWindow
from Scripts.Verification import verify
from Scripts.EncryptDecryptFunctions import Load_public_key
from PySide6.QtCore import QObject, Signal
import config
class Communicate(QObject):
    append_text = Signal(str)

class VerifyWindow(BaseWindow):
    key_path = None
    xml_file_path = None
    file_path = None
    def __init__(self):
        super().__init__()
        super().initializeUI()

        self.comm = Communicate()
        self.comm.append_text.connect(self.appendText)
        layout = QVBoxLayout()
        self.setWindowTitle("Weryfikowanie podpisu")

        self.fileButton = QPushButton("Wskaż klucz publiczny")
        self.fileButton.clicked.connect(self.open_file_dialog)

        self.xmlfileButton = QPushButton("Wskaż podpis .xml")
        self.xmlfileButton.clicked.connect(self.open_xmlfile_dialog)

        self.fileButton2 = QPushButton("Wskaż plik, który chcesz zweryfikować")
        self.fileButton2.clicked.connect(self.open_file_dialog2)

        self.verify_button = QPushButton("Werufikuj podpis")
        self.verify_button.clicked.connect(self.verify_button_fun)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        layout.addWidget(self.fileButton)
        layout.addWidget(self.xmlfileButton)
        layout.addWidget(self.fileButton2)
        layout.addWidget(self.verify_button)
        layout.addWidget(self.console)

        self.setLayout(layout)


    def closeEvent(self, event):
        super().closeEvent(event)

    def open_file_dialog(self):
        self.key_path, _ = QFileDialog.getOpenFileName(self, "Wybierz klucz publiczny")
        self.appendText("Wybrałeś plik: " + str(self.key_path))
        Load_public_key(self.key_path, self)

    def open_file_dialog2(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik do sprawdzenia")
        self.appendText("Wybrałeś plik: " + str(self.file_path))

    def open_xmlfile_dialog(self):
        self.xml_file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik .xml z podpisem")
        self.appendText("Wybrałeś plik: " + str(self.xml_file_path))

    def verify_button_fun(self):
        if config.PUBLIC_KEY is not None:
            if self.xml_file_path is not None:
                if self.file_path is not None:
                    verify(self.xml_file_path, self.file_path, self)
                else:
                    self.appendText("Podaj plik do weryfikacji")
            else:
                self.appendText("Podaj plik .xml z podpisem")
        else:
            self.appendText("Podaj klucz publiczny")

    def appendText(self, text):
        self.console.append(text)

