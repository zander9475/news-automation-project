from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextBrowser,
                               QSizePolicy, QHBoxLayout, QPushButton, QMessageBox)
from PySide6.QtCore import Signal, Slot, Qt
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
        self.header = QLabel()
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.header)

        # Declare widgets where text will go
        self.title_label = QLabel()
        self.lead_label = QLabel()
        self.author_label = QLabel()
        self.source_label = QLabel()
        self.content_label = QLabel()
        self.content_text = QTextBrowser()
        self.content_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        
        # Set stretch so content_text grows vertically
        self.main_layout.setStretch(self.main_layout.indexOf(self.content_text), 1)

        self.setLayout(self.main_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.clear_display()

    def display_article(self, article: 'Article'):
        """
        Populates the preview pane with article details
        """
        self.article = article

        # Set the header text
        self.header.setText("Selected article details:")

        # Set the text for required fields
        self.title_label.setText(f"<b>Title:</b> {self.article.title}")
        self.source_label.setText(f"<b>Source:</b> {self.article.source}")
        # Show plain text content
        self.content_text.setPlainText(self.article.content)

        # Set visibility for widgets
        self.title_label.setVisible(True)
        self.source_label.setVisible(True)
        self.content_label.setVisible(True)
        self.content_text.setVisible(True)
        self.action_btns.setContentsMargins(0, 5, 0, 0) # Adjust margin for aesthetics
        self.action_btns.setSpacing(5) # Add spacing between buttons
        self.edit_btn.setVisible(True)
        self.delete_btn.setVisible(True)

        # Enable optional fields if they exist
        self.lead_label.setVisible(bool(self.article.lead))
        if self.article.lead:
            self.lead_label.setText(f"<b>Lead:</b> {self.article.lead}")

        self.author_label.setVisible(bool(self.article.author))
        if self.article.author and len(self.article.author) > 0:
            # Split the author list into a string
            authors = ', '.join(self.article.author)
            self.author_label.setText(f"<b>Author(s):</b> {authors}")

        # Enable action buttons
        self.edit_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

    def clear_display(self):
        """Clears all fields and disables buttons in the preview pane."""
        self.article = None

        # Set the header to the placeholder text
        self.header.setText("Select an article from the list to view its details.")

        # Clear and hide content widgets
        self.title_label.setText("")
        self.title_label.setVisible(False)
        self.lead_label.setText("")
        self.lead_label.setVisible(False)
        self.author_label.setText("")
        self.author_label.setVisible(False)
        self.source_label.setText("")
        self.source_label.setVisible(False)
        self.content_label.setText("")
        self.content_label.setVisible(False)
        self.content_text.setPlainText("")
        self.edit_btn.setVisible(False)
        self.delete_btn.setVisible(False)
        
        # Disable action buttons
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

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