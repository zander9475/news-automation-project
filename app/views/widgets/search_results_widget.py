import webbrowser
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                               QHBoxLayout, QPushButton, QAbstractItemView, QLabel, QSizePolicy)

class SearchResultsWidget(QWidget):
    """
    Displays Google search results.
    """
    # Custom signals
    rerun_search_requested = Signal()
    main_menu_requested = Signal()
    article_addition_requested = Signal(dict)
    articles_page_requested = Signal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes UI components. Will show search results by displaying title (as clickable url), source, and keyword
        """
        self.main_layout = QVBoxLayout()

        # Header
        self.header = QLabel("<h2>View Search Results Here.<\h2>")
        self.page_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setWordWrap(True)
        self.header.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        # Rerun search button at the top
        self.rerun_search_btn = QPushButton("Rerun Search")
        self.rerun_search_btn.clicked.connect(self.rerun_search_requested.emit)
        self.main_layout.addWidget(self.rerun_search_btn)
    
        # Create search results table
        self.table = QTableWidget()
        
        # Configure the columns
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Source", "Keyword", ""])

        # Set the table to stretch the columns to fit the content
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Disable editing
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.main_layout.addWidget(self.table)

        # Action buttons
        self.action_btns = QHBoxLayout()
        self.main_menu_btn = QPushButton("Back to Main Menu")
        self.main_menu_btn.clicked.connect(self.main_menu_requested.emit)
        self.articles_page_btn= QPushButton("Proceed to Manage Articles")
        self.articles_page_btn.clicked.connect(self.articles_page_requested.emit)
        self.action_btns.addWidget(self.main_menu_btn)
        self.action_btns.addWidget(self.articles_page_btn)
        self.main_layout.addLayout(self.action_btns)

        # Connect the item clicked signal to a method that opens the URL
        self.table.itemClicked.connect(self._on_title_clicked)

        # Set layout
        self.setLayout(self.main_layout)

    def display_results(self, results):
        """
        Displays the search results in the table.
        
        @param results: List of dictionaries containing article information.
        """
        self.table.setRowCount(len(results))
        for row, article in enumerate(results):
            # Create a table item for the title
            title_item = QTableWidgetItem(article['title'])
            # Set the URL as hidden data on the title item
            title_item.setData(Qt.ItemDataRole.UserRole, article['url'])

            # Create "Add to Email" button for each article
            add_btn = QPushButton("Add to Email")
            # Use a lambda function to to pass specific article from the loop when clicked
            add_btn.clicked.connect(
                lambda _=False, # Catch boolean value from click
                article=article: (self.article_addition_requested.emit(article))
            )

            # Set the items in the table
            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, QTableWidgetItem(article['source']))
            self.table.setItem(row, 2, QTableWidgetItem(article['keyword']))
            self.table.setCellWidget(row, 3, add_btn)

    def _on_title_clicked(self, item):
        """
        Opens the URL associated with the clicked title item.
        """
        url = item.data(Qt.ItemDataRole.UserRole)
        if url:
            webbrowser.open(url)