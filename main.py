import sys
from datetime import date
import os
from PySide6.QtWidgets import QApplication

from app.views.main_window import MainWindow
from app.controllers.main_controller import MainController
from app.config import DATA_FILE, BASE_DIR

def clear_articles():
    """
    Clears articles upon startup if the program hasn't been run today.
    """
    today = date.today().isoformat()
    date_file = os.path.join(BASE_DIR, "data", "last_run_date.txt")

    # Read last run date
    last_date = None
    if os.path.exists(date_file):
        with open(date_file, "r") as f:
            last_date = f.read().strip()

    # If the date is different, clear the articles
    if last_date != today:
        print("New day detected — clearing articles...")

        # Delete CSV file if it exists
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

        # Save today’s date
        os.makedirs(os.path.dirname(date_file), exist_ok=True)
        with open(date_file, "w") as f:
            f.write(today)

def main():
    """
    Initializes and runs the application.
    """
    app = QApplication(sys.argv)

    clear_articles()

    window = MainWindow()
    controller = MainController(window)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()