from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

class MainMenuWidget(QWidget):
    # Define signals to communicate with MainController

    # Constructor
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout(self)