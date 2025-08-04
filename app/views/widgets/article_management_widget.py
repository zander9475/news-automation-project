from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QSplitter, 
                                QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, Slot
from .article_preview_widget import ArticlePreviewWidget
from app.models.article import Article

class ArticleManagementWidget(QWidget):
    # Custom signals
    url_scrape_requested = Signal(str) # Connects to ArticleController
    manual_input_requested = Signal() # Connects to ArticleController
    main_menu_requested = Signal()
    article_preview_requested = Signal(int)
    edit_article_requested = Signal(Article)

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
        self.listbox_header = QLabel("Reorder articles by selecting an article and dragging it to your desired location." \
                                        "\nClick on any article title to preview its contents.")
        self.listbox_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        # Enable previewing by selecting article title
        self.listbox.currentItemChanged.connect(self._on_item_changed)

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

        # Connect to the child's signal
        self.preview_pane.edit_article_requested.connect(self._on_child_edit_request)

    def _on_url_btn_clicked(self):
        """
        Passes the URL to the controller for scraping.
        """
        url = self.url_input.text().strip()
        if url:
            self.url_scrape_requested.emit(url)
            self.url_input.clear()

    @Slot()
    def _on_item_changed(self):
        """
        Handles selection of an article title in the listbox.
        """
        selected_item = self.listbox.currentItem()

        if selected_item:
            # Get its index
            index = self.listbox.row(selected_item)
            # Pass that index to the controller
            self.article_preview_requested.emit(index)

    def populate_list(self, articles):
        """
        Displays the list of article titles in the ListWidget.
        
        @param articles: list of Article objects.
        """
        # Clear listbox
        self.listbox.clear()

        for article in articles:
            # Create a list item
            title_item = QListWidgetItem(article.title)
            
            # Set the Article object as hidden data on the title
            title_item.setData(Qt.ItemDataRole.UserRole, article)

            # Add the item to the list widget
            self.listbox.addItem(title_item)

    def set_preview_visible(self, visible: bool):
        """Public method to control preview visibility"""
        self.preview_pane.setVisible(visible)

    def update_preview(self, article):
        """Public method to update preview content"""
        self.preview_pane.display_article(article)

    def _on_child_edit_request(self, article):
        self.edit_article_requested.emit(article)