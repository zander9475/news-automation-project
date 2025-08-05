from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class MainMenuWidget(QWidget):
    """
    Defines main menu pages
    """
    # Define signals to communicate with MainController
    search_requested = Signal()
    search_results_page_requested = Signal()
    articles_page_requested = Signal()
    # Potential addition: settings page

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initializes UI components (layouts, labels, buttons, etc.)"""
        self.main_layout = QVBoxLayout()

        # Define layout components
        # Connect button clicks to custom signals
        self.page_header = QLabel("<h1>Welcome to the News Clipper tool.<\h1>")
        self.page_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_subheader = QLabel("<h2>Select \"Search Google\" to begin, or choose another option.</h2>")
        self.page_subheader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.search_button = QPushButton("Search Google", self)
        self.search_button.clicked.connect(self.search_requested.emit)

        self.search_results_button = QPushButton("View Latest Search Results")
        self.search_results_button.clicked.connect(self.search_results_page_requested.emit)

        self.articles_button = QPushButton("Manage Articles")
        self.articles_button.clicked.connect(self.articles_page_requested.emit)

        # Add components to main layout
        self.main_layout.addWidget(self.page_header)
        self.main_layout.addWidget(self.page_subheader)
        self.main_layout.addWidget(self.search_button)
        self.main_layout.addWidget(self.search_results_button)
        self.main_layout.addWidget(self.articles_button)

        # Set layout for this widget
        self.setLayout(self.main_layout)

        # Set style sheet
        self.setStyleSheet("""
            QPushButton{
                font-size: 18px;
                font-family: Arial;
                padding: 20px;
                margin: 5px;
                border: 3px solid;
                border-radius: 10px;
            }
        """)