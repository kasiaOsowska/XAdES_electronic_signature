from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog
from BaseWindow import BaseWindow
from Scripts.SigningDocument import sing_document

class SigningWindow(BaseWindow):
    file_path = None
    def __init__(self):
        super().__init__()
        super().initializeUI()
        layout = QVBoxLayout()
        self.setWindowTitle("Podpisywanie dokumentu")

        self.fileButton = QPushButton("Wybierz plik do podpisu")
        self.fileButton.clicked.connect(self.open_file_dialog)

        layout.addWidget(self.fileButton)
        self.setLayout(layout)


    def closeEvent(self, event):
        super().closeEvent(event)

    def open_file_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik do podpisu")
        sing_document(self.file_path, self)

