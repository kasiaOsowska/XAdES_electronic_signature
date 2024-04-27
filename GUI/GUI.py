import sys
import os
from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow


def load_style_sheet(file):
    with open(file, "r") as f:
        return f.read()


app = QApplication()
current_dir = os.path.dirname(os.path.abspath(__file__))
styleSheet = load_style_sheet(os.path.join(current_dir, "style.qss"))
app.setStyleSheet(styleSheet)

window = MainWindow()
window.show()
sys.exit(app.exec())
