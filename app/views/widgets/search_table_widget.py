from PySide6.QtWidgets import QTableWidget, QHeaderView

class SearchTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(SearchTableWidget, self).__init__(parent)
        
        # Set up the table
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Title", "Source", "Keyword", ""])
        
        # Set initial column widths proportionally
        total_width = self.width()
        if total_width == 0:
            total_width = 800  # Default width if not yet set
        self.setColumnWidth(0, int(0.45 * total_width))  # Title: 60%
        self.setColumnWidth(1, int(0.20 * total_width))  # Source: 15%
        self.setColumnWidth(2, int(0.20 * total_width))  # Keyword: 15%
        self.setColumnWidth(3, int(0.13 * total_width))  # Button: 10%
        
        # Make all columns interactive (user-resizable)
        header = self.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Interactive)
        
        # Store the old width for scaling
        self.old_width = total_width

    def resizeEvent(self, event):
        # Call the parent's resizeEvent
        super(SearchTableWidget, self).resizeEvent(event)
        
        # Get the new width
        new_width = self.width()
        
        # Calculate the scale factor
        if hasattr(self, 'old_width') and self.old_width > 0:
            scale = new_width / self.old_width
        else:
            scale = 1
        
        # Scale each column proportionally
        for i in range(4):
            current_width = self.columnWidth(i)
            new_col_width = int(current_width * scale)
            self.setColumnWidth(i, new_col_width)
        
        # Update the old width
        self.old_width = new_width