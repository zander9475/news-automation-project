from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                               QTextEdit, QHBoxLayout, QPushButton, QMessageBox)
from app.models.article import Article
from typing import Optional

class ManualInputWidget(QWidget):
    # Custom signals
    submission_completed = Signal(Article)
    submission_cancelled = Signal()

    def __init__(self):
        super().__init__()
        self.is_editing_mode = False
        self.article_being_edited: Optional[Article]
        self.initUI()

    def initUI(self):
        """Initializes UI components"""
        self.main_layout = QVBoxLayout()

        # Component 1: Header
        self.header = QLabel("<h2>Enter Article Details</h2>")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.header)

        # Component 2: Title
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel("Title: ")
        self.title_input = QLineEdit()
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.title_input)
        self.main_layout.addLayout(self.title_layout)

        # Component 3: Lead (portion in italics between title and author)
        self.lead_layout = QHBoxLayout()
        self.lead_label = QLabel("Lead: ")
        self.lead_input = QLineEdit()
        self.lead_layout.addWidget(self.lead_label)
        self.lead_layout.addWidget(self.lead_input)
        self.main_layout.addLayout(self.lead_layout)

        # Component 4: Author(s)
        self.author_layout = QHBoxLayout()
        self.author_label = QLabel("Author(s): ")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("If multiple authors, separate by comma.")
        self.author_layout.addWidget(self.author_label)
        self.author_layout.addWidget(self.author_input)
        self.main_layout.addLayout(self.author_layout)

        # Component 5: Source
        self.source_layout = QHBoxLayout()
        self.source_label = QLabel("Source: ")
        self.source_input = QLineEdit()
        self.source_layout.addWidget(self.source_label)
        self.source_layout.addWidget(self.source_input)
        self.main_layout.addLayout(self.source_layout)

        # Component 6: Content
        self.content_layout = QVBoxLayout()
        self.content_label = QLabel("Content: ")
        self.content_input = QTextEdit()
        self.content_layout.addWidget(self.content_label)
        self.content_layout.addWidget(self.content_input)
        self.main_layout.addLayout(self.content_layout)

        # Component 7: Action buttons
        self.action_btns = QHBoxLayout()
        self.submit_btn = QPushButton("Add Article")
        self.submit_btn.clicked.connect(self._on_article_submission)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.submission_cancelled)
        self.action_btns.addWidget(self.submit_btn)
        self.action_btns.addWidget(self.cancel_btn)
        self.main_layout.addLayout(self.action_btns)

        # Set layout
        self.setLayout(self.main_layout)

    def _on_article_submission(self):
        """
        Gathers data from UI fields and assembles or edits Article object
        """
        # Gather data from input fields
        title = self.title_input.text().strip()
        lead = self.lead_input.text().strip() if self.lead_input.text().strip() else None
        author_text = self.author_input.text().strip()
        source = self.source_input.text().strip()
        content = self.content_input.toHtml().strip() 

        # Validate required fields
        if not title:
            QMessageBox.warning(self, "Validation Error", "Title is required.")
            return
        
        if not source:
            QMessageBox.warning(self, "Validation Error", "Source is required.")
            return
        
        if not content:
            QMessageBox.warning(self, "Validation Error", "Content is required.")
            return
        
        # Process authors - split by comma and clean up whitespace
        authors = []
        if author_text:
            # Splits authors string by comma, adds individual authors into list
            authors = [author.strip() for author in author_text.split(',') if author.strip()]

        # Check if adding or editing article
        if self.is_editing_mode:
            # Update the properties of the existing article object
            edited_article = self.article_being_edited
            edited_article.title = title
            edited_article.lead = lead
            edited_article.author = authors if authors else [""]
            edited_article.source = source
            edited_article.content = content

            # Emit signal
            self.submission_completed.emit(edited_article)
        else:
            # Create Article object
            try:
                article = Article(
                    title=title,
                    content=content,
                    source=source,
                    keyword="Manual",
                    author=authors,
                    url=None,
                    lead=lead
                )
                
                # Emit article submission signal
                self.submission_completed.emit(article)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create article: {str(e)}")

        # Reset form state
        self._clear_form()

    def _clear_form(self):
        """
        Clears all input fields in the form and resets widget state
        """
        # Clear inputs
        self.title_input.clear()
        self.lead_input.clear()
        self.author_input.clear()
        self.source_input.clear()
        self.content_input.clear()

        # Reset flags
        self.is_editing_mode = False
        self.article_being_edited = None

        # Reset UI elements
        self.submit_btn.setText("Add Article")
        self.header.setText("<h2>Enter Article Details</h2>")

    def set_article_data(self, article: Article):
        """
        Populates the form with data from an Article object for editing.
        @param article: Article object to populate the form with.
        """
        # Set flags
        self.is_editing_mode = True
        self.article_being_edited = article

        # Update UI elements for editing
        self.submit_btn.setText("Save Changes")
        self.header.setText("<h2>Edit Article Details</h2>")

        # Pre-fill input fields
        self.title_input.setText(article.title)
        self.lead_input.setText(article.lead if article.lead else "")
        self.author_input.setText(", ".join(article.author) if article.author else "")
        
        self.source_input.setText(article.source)
        self.content_input.setPlainText(article.content)