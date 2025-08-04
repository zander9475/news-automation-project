from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                               QTextEdit, QHBoxLayout, QPushButton, QMessageBox)
from app.models.article import Article

class ManualInputWidget(QWidget):
    # Custom signals
    article_submitted = Signal(Article)
    submission_cancelled = Signal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initializes UI components"""
        self.main_layout = QVBoxLayout()

        # Component 1: Header
        self.header = QLabel("Enter article details: ")
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
            self.article_submitted.emit(article)
            
            # Clear the form after successful submission
            self._clear_form()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create article: {str(e)}")

    def _clear_form(self):
        """
        Clears all input fields in the form
        """
        self.title_input.clear()
        self.lead_input.clear()
        self.author_input.clear()
        self.source_input.clear()
        self.content_input.clear()

    def set_article_data(self, article: Article):
        """
        Populates the form with data from an Article object for editing.
        
        @param article: Article object to populate the form with.
        """
        self.title_input.setText(article.title)
        self.lead_input.setText(article.lead if article.lead else "")
        self.author_input.setText(", ".join(article.author) if article.author else "")
        self.source_input.setText(article.source)
        self.content_input.setHtml(article.content)