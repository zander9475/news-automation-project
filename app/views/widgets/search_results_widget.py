import webbrowser
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class SearchResultsWidget(QWidget):
    """
    Displays Google search results.
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes UI components. Will show search results by displaying title (as clickable url), source, and keyword
        """
        layout = QVBoxLayout(self)
    
        # Create search results table
        self.table = QTableWidget()
        
        # Configure the columns
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Title", "Source", "Keyword"])

        # Set the table to stretch the columns to fit the content
        self.table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table)

        # Connect the item clicked signal to a method that opens the URL
        self.table.itemClicked.connect(self._on_title_clicked)

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

            # Set the items in the table
            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, QTableWidgetItem(article['source']))
            self.table.setItem(row, 2, QTableWidgetItem(article['keyword']))

    def _on_title_clicked(self, item):
        """
        Opens the URL associated with the clicked title item.
        """
        url = item.data(Qt.ItemDataRole.UserRole)
        if url:
            webbrowser.open(url)