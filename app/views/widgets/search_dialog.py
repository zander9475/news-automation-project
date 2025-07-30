from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QDialogButtonBox, QPushButton

class SearchDialog(QDialog):
    """
    Dialog for searching articles with a date range.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Articles")
        
        # Define layout and components
        layout = QVBoxLayout(self)
        
        self.label = QLabel("Select the number of days back to search:")
        layout.addWidget(self.label)
        
        # Add a spinbox for selecting number of days back
        self.days_back_spinbox = QSpinBox(self)
        self.days_back_spinbox.setRange(1, 7)  # Allow up to 7 days
        self.days_back_spinbox.setValue(1)  # Default to 1 day
        layout.addWidget(self.days_back_spinbox)
        
        # Add buttons to run search or cancel
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel, self)
        self.run_search_button = QPushButton("Run Search", self)
        self.button_box.addButton(self.run_search_button, QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_selected_days(self):
        """Returns the number of days selected in the spinbox."""
        return self.days_back_spinbox.value()