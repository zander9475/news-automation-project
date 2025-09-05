from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QSplitter, QSizePolicy,
                                QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, Slot
from ..widgets.article_preview_widget import ArticlePreviewWidget
from app.models.article import Article
from ..widgets.reorderable_list_widget import ReorderableListWidget

class ArticleManagementWidget(QWidget):
    # Custom signals, connect to ArticleController
    url_scrape_requested = Signal(str)
    manual_input_requested = Signal()
    main_menu_requested = Signal() # Connect to MainController
    article_preview_requested = Signal(Article)
    edit_article_requested = Signal(Article)
    delete_article_requested = Signal(Article)
    save_articles_requested = Signal()
    reorder_articles_requested = Signal(list)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initializes UI components"""
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # First component: QLabel for header
        self.header = QLabel("Welcome to the article collection screen. Add article by URL, or add manually.")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setWordWrap(True)
        self.header.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
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

        # Third component: QHBox layout for manual input
        self.manual_input_layout = QHBoxLayout()
        self.manual_header = QLabel("Enter article details manually: ")
        self.submit_manual_btn = QPushButton("Add Manually")
        self.submit_manual_btn.clicked.connect(self.manual_input_requested.emit)
        self.manual_input_layout.addWidget(self.manual_header)
        self.manual_input_layout.addWidget(self.submit_manual_btn)
        self.manual_input_layout.addStretch(1)
        self.main_layout.addLayout(self.manual_input_layout)

        # Fourth component: QLabel for reordering articles
        self.listbox_header = QLabel("Reorder articles by selecting an article and dragging it to your desired location." \
                                        "\nClick on any article title to preview its contents.")
        self.listbox_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.listbox_header.setWordWrap(True)
        self.listbox_header.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.main_layout.addWidget(self.listbox_header)

        # Fifth component: QSplitter for master-detail view
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setSizes([300, 500]) # Initial width ratio

        # Master view: listbox
        self.listbox = ReorderableListWidget()

        # Enable drag-and-drop and previewing
        self.listbox.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.listbox.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.listbox.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.listbox.itemClicked.connect(self._on_item_changed)
        self.listbox.orderChanged.connect(self._on_order_changed)
        self.splitter.addWidget(self.listbox)

        # Detail view: preview pane
        self.preview_pane = ArticlePreviewWidget()
        self.splitter.addWidget(self.preview_pane)

        # Set stretch factors for the splitter
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

        self.main_layout.addWidget(self.splitter, stretch=1)

        # Final component: Action buttons
        self.action_btns = QHBoxLayout()
        self.build_email_btn = QPushButton("Build Email")
        self.build_email_btn.clicked.connect(self.save_articles_requested.emit)
        self.main_menu_btn = QPushButton("Back to Main Menu")
        self.main_menu_btn.clicked.connect(self.main_menu_requested.emit)
        self.action_btns.addWidget(self.build_email_btn)
        self.action_btns.addWidget(self.main_menu_btn)
        self.action_btns.addStretch(1)
        self.main_layout.addLayout(self.action_btns)

        # Set layout
        self.setLayout(self.main_layout)

        # Connect to preview pane signals
        self.preview_pane.edit_article_requested.connect(self.edit_article_requested.emit)
        self.preview_pane.delete_article_requested.connect(self.delete_article_requested.emit)

    @Slot()
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
            # Get the Article object
            article = selected_item.data(Qt.ItemDataRole.UserRole)

            # Pass that article to the controller
            self.article_preview_requested.emit(article)

    @Slot()
    def _on_order_changed(self):
        """
        Handles reordering of article listbox
        """
        titles = [self.listbox.item(i).text() for i in range(self.listbox.count())]
        self.reorder_articles_requested.emit(titles)

    def populate_list(self, articles):
        """
        Displays the list of article titles in the ListWidget.
        
        @param articles: list of Article objects.
        """
        # Clear preview pane
        self.preview_pane.clear_display()

        # Clear listbox
        self.listbox.clear()

        for article in articles:
            # Create a list item
            title_item = QListWidgetItem(article.title)
            
            # Set the Article object as hidden data on the title
            title_item.setData(Qt.ItemDataRole.UserRole, article)

            # Add the item to the list widget
            self.listbox.addItem(title_item)

    def update_preview(self, article):
        """Public method to update preview content"""
        self.preview_pane.display_article(article)

    def reset_view(self):
        """Resets the state of the article management widget."""
        # Clear the preview pane
        self.preview_pane.clear_display()

        # Clear listbox selection
        self.listbox.clearSelection()