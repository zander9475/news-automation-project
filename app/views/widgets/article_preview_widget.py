from PySide6.QtWidgets import QWidget, QVBoxLayout

class ArticlePreviewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initializes UI components"""
        self.main_layout = QVBoxLayout()