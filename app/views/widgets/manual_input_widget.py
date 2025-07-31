from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                               QTextEdit, QHBoxLayout, QPushButton)

class ManualInputWidget(QWidget):
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
        self.cancel_btn = QPushButton("Cancel")
        self.main_layout.addLayout(self.action_btns)

        # Set layout
        self.setLayout(self.main_layout)