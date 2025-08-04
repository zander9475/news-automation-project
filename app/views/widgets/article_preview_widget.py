from PySide6.QtWidgets import (QWidget, QVBoxLayout,  QLabel, QTextBrowser, 
                               QSizePolicy, QHBoxLayout, QPushButton, QMessageBox)
from PySide6.QtCore import Signal, Slot
from app.models.article import Article

class ArticlePreviewWidget(QWidget):
    # Custom signals
    edit_article_requested = Signal(Article)
    delete_article_requested = Signal(Article)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.article = None

    def initUI(self):
        """Initializes UI components"""
        self.main_layout = QVBoxLayout()

        # Header
        self.main_layout.addWidget(QLabel("<h2>Article Details</h2>"))

        # Declare widgets where text will go
        self.title_label = QLabel()
        self.lead_label = QLabel()
        self.author_label = QLabel()
        self.source_label = QLabel()
        self.content_label = QLabel("<b>Content:</b>")
        self.content_text = QTextBrowser()
        self.content_text.setReadOnly(True)
        self.content_text.setOpenExternalLinks(True)

        # Action btns
        self.action_btns = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self._on_edit_clicked)
        self.edit_btn.setEnabled(False)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self._on_delete_clicked)
        self.delete_btn.setEnabled(False)
        self.action_btns.addWidget(self.edit_btn)
        self.action_btns.addWidget(self.delete_btn)

        # Add layout components
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.lead_label)
        self.main_layout.addWidget(self.author_label)
        self.main_layout.addWidget(self.source_label)
        self.main_layout.addWidget(self.content_label)
        self.main_layout.addWidget(self.content_text)
        self.main_layout.addLayout(self.action_btns)
        
        self.main_layout.addStretch()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setLayout(self.main_layout)

    def display_article(self, article: 'Article'):
        """
        Populates the preview pane with article details
        """
        self.article = article

        # Set the text for required fields
        self.title_label.setText(f"<b>Title:</b> {self.article.title}")
        self.source_label.setText(f"<b>Source:</b> {self.article.source}")
        self.content_text.setHtml(self.article.content)

        # Enable optional fields if they exist
        self.lead_label.setVisible(bool(self.article.lead))
        if self.article.lead:
            self.lead_label.setText(f"<b>Lead:</b> {self.article.lead}")

        self.author_label.setVisible(bool(self.article.author))
        if self.article.author:
            self.author_label.setText(f"<b>Author:</b> {self.article.author}")
        self.edit_btn.setEnabled(True)

    @Slot()
    def _on_edit_clicked(self):
        """Passes article to controller through parent widget"""
        if self.article:
            self.edit_article_requested.emit(self.article)

    @Slot()
    def _on_delete_clicked(self):
        # QMessageBox question to confirm delete
        if self.article:
            confirmation = QMessageBox.question(
                self, "Confirm Delete", 
                f"Are you sure you want to delete the article '{self.article.title}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.delete_article_requested.emit(self.article)