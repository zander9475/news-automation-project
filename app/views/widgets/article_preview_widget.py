from PySide6.QtWidgets import QWidget, QVBoxLayout,  QLabel, QTextBrowser, QSizePolicy
from app.models.article import Article

class ArticlePreviewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_article = None

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
        self.content_text = QTextBrowser()
        self.content_text.setReadOnly(True)
        self.content_text.setOpenExternalLinks(True)

        # Add the widgets
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.lead_label)
        self.main_layout.addWidget(self.author_label)
        self.main_layout.addWidget(self.source_label)
        self.main_layout.addWidget(self.content_text)

        self.main_layout.addStretch()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setLayout(self.main_layout)

    def display_article(self, article: 'Article'):
        """
        Populates the preview pane with article details
        """
        # Set the text for required fields
        self.title_label.setText(f"<b>Title:</b> {article.title}")
        self.source_label.setText(f"<b>Source:</b> {article.source}")
        self.content_text.setHtml(article.content)

        # Enable optional fields if they exist
        self.lead_label.setVisible(bool(article.lead))
        if article.lead:
            self.lead_label.setText(f"<b>Lead:</b> {article.lead}")

        self.author_label.setVisible(bool(article.author))
        if article.author:
            self.author_label.setText(f"<b>Author:</b> {article.author}")