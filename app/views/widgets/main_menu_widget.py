from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class MainMenuWidget(QWidget):
    """
    Defines main menu pages
    """
    # Define signals to communicate with MainController
    search_requested = Signal()
    search_results_page_requested = Signal()
    collection_page_requested = Signal()
    preview_articles_page_requested = Signal()
    # Potential addition: settings page

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initializes UI components (layouts, labels, buttons, etc.)"""
        self.main_layout = QVBoxLayout()

        # Define layout components
        # Connect button clicks to custom signals
        self.page_header = QLabel("Welcome to the News Clipper tool. " \
                            "Select \"Search Google\" to begin, or choose another option", self)
        self.page_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.search_button = QPushButton("Search Google", self)
        self.search_button.clicked.connect(self.search_requested.emit)

        self.search_results_button = QPushButton("View Latest Search Results", self)
        self.search_results_button.clicked.connect(self.search_results_page_requested.emit)

        self.article_collection_button = QPushButton("Collect Articles", self)
        self.article_collection_button.clicked.connect(self.collection_page_requested.emit)

        self.preview_articles_button = QPushButton("Preview Articles", self)
        self.preview_articles_button.clicked.connect(self.preview_articles_page_requested.emit)

        # Add components to main layout
        self.main_layout.addWidget(self.page_header)
        self.main_layout.addWidget(self.search_button)
        self.main_layout.addWidget(self.search_results_button)
        self.main_layout.addWidget(self.article_collection_button)
        self.main_layout.addWidget(self.preview_articles_button)

        # Set layout for this widget
        self.setLayout(self.main_layout)