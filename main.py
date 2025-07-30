import sys
from PySide6.QtWidgets import QApplication

from app.views.main_window import MainWindow
from app.controllers.main_controller import MainController

def main():
    """
    Initializes and runs the application.
    """
    app = QApplication(sys.argv)

    window = MainWindow()
    controller = MainController(window)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

