from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QSplitter, 
                                QHBoxLayout, QLineEdit, QListWidget, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from .article_preview_widget import ArticlePreviewWidget

class ArticleManagementWidget(QWidget):
    # Custom signals
    url_scrape_requested = Signal(str) # Needs method in main_controller
    manual_input_requested = Signal()
    main_menu_requested = Signal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initializes UI components"""
        self.main_layout = QVBoxLayout()

        # First component: QLabel for header
        self.header = QLabel("Welcome to the article collection screen. Add article by URL, or add manually.")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.header)

        # Second component: QHBox layout for submitting article by URL
        self.url_input_layout = QHBoxLayout()
        self.url_header = QLabel("Enter by URL: ")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste URL here")
        self.submit_url_btn = QPushButton("Submit URL")
        self.submit_url_btn.clicked.connect(self._on_url_btn_clicked)
        self.url_input_layout.addWidget(self.url_header)
        self.url_input_layout.addWidget(self.url_input)
        self.url_input_layout.addWidget(self.submit_url_btn)
        self.main_layout.addLayout(self.url_input_layout)

        # Third component: QHBox layout containing QLabel and QPushButton for adding article manually
        self.manual_input_layout = QHBoxLayout()
        self.manual_header = QLabel("Enter article details manually: ")
        self.submit_manual_btn = QPushButton("Add Manually")
        self.submit_manual_btn.clicked.connect(self.manual_input_requested.emit)
        self.manual_input_layout.addWidget(self.manual_header)
        self.manual_input_layout.addWidget(self.submit_manual_btn)
        self.main_layout.addLayout(self.manual_input_layout)

        # Fourth component: QLabel for reordering articles
        self.listbox_header = QLabel("Reorder articles by selecting an article and dragging it to your desired location.")
        self.main_layout.addWidget(self.listbox_header)

        # Fifth component: QSplitter for master-detail view
        self.splitter = QSplitter()

        # Master view: listbox
        self.listbox = QListWidget()

        # Enable drag-and-drop
        self.listbox.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.listbox.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.listbox.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.splitter.addWidget(self.listbox)

        # Enable previewing by clicking on article title
        self.listbox.itemClicked.connect(self._on_title_clicked)

        # Detail view: preview pane
        self.preview_pane = ArticlePreviewWidget()
        self.splitter.addWidget(self.preview_pane)

        self.main_layout.addWidget(self.splitter)

        # Final component: QHBox for save/cancel buttons
        self.action_btns = QHBoxLayout()
        self.save_order_btn = QPushButton("Save Order")
        self.main_menu_btn = QPushButton("Back to Main Menu")
        self.main_menu_btn.clicked.connect(self.main_menu_requested.emit)
        self.action_btns.addWidget(self.save_order_btn)
        self.action_btns.addWidget(self.main_menu_btn)
        self.main_layout.addLayout(self.action_btns)

        # Set layout
        self.setLayout(self.main_layout)

    def _on_url_btn_clicked(self):
        """
        Passes the URL to the controller for scraping.
        """
        url = self.url_input.text().strip()
        if url:
            self.url_scrape_requested.emit(url)
            self.url_input.clear()

    def _on_title_clicked(self, item):
        """
        Pops up a dialog showing a preview of selected article.
        Allows user to edit article details.
        """
        pass

    def display_articles(self, articles):
        """
        Displays the list of article titles in the ListWidget.
        
        @param articles: list of Article objects.
        """
        """ self.table.setRowCount(len(results))
        for row, article in enumerate(results):
            # Create a table item for the title
            title_item = QTableWidgetItem(article['title'])
            # Set the URL as hidden data on the title item
            title_item.setData(Qt.ItemDataRole.UserRole, article['url'])

            # Set the items in the table
            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, QTableWidgetItem(article['source']))
            self.table.setItem(row, 2, QTableWidgetItem(article['keyword'])) """
