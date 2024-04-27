from PySide6.QtWidgets import QApplication, QWidget


class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        screen = QApplication.primaryScreen().availableGeometry()

        width = screen.width() * 0.5
        height = screen.height() * 0.5
        left = (screen.width() - width) / 2
        top = (screen.height() - height) / 2
        self.setGeometry(left, top, width, height)


