from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import Signal

class ReorderableListWidget(QListWidget):
    """
    List widget that emits a custom signal when a drag-and-drop action is completed.
    """
    orderChanged = Signal()

    def dropEvent(self, event):
        super().dropEvent(event)  # Perform the default drop action
        self.orderChanged.emit()  # Emit custom signal
