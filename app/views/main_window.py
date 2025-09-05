from PySide6.QtWidgets import QMainWindow, QStackedWidget
from .pages.main_menu_page import MainMenuWidget
from .pages.article_management_page import ArticleManagementWidget
from .pages.search_results_page import SearchResultsWidget
from .pages.manual_input_page import ManualInputWidget

class MainWindow(QMainWindow):
    """
    Defines main application window.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News Automation Tool")
        self.setMinimumSize(900, 600)
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components.
        """
        # Create a stacked widget to manage different views
        self.Stack = QStackedWidget(self)

        # Create an instance of each view widget
        self.main_menu_page = MainMenuWidget()
        self.article_management_page = ArticleManagementWidget()
        self.search_results_page = SearchResultsWidget()
        self.manual_input_page = ManualInputWidget()

        # Add the widgets to the stacked widget
        self.Stack.addWidget(self.main_menu_page)
        self.Stack.addWidget(self.article_management_page)
        self.Stack.addWidget(self.search_results_page)
        self.Stack.addWidget(self.manual_input_page)

        # Set initial page to main menu
        self.Stack.setCurrentWidget(self.main_menu_page)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.Stack)

    def switch_page(self, page: str):
        """
        Switches to a specified page in the stacked widget.
        @param page (str): The name of the page to switch to.
        """
        if page == "main_menu":
            self.Stack.setCurrentWidget(self.main_menu_page)
        elif page == "article_management":
            self.Stack.setCurrentWidget(self.article_management_page)
        elif page == "search_results":
            self.Stack.setCurrentWidget(self.search_results_page)
        elif page == "manual_input":
            self.Stack.setCurrentWidget(self.manual_input_page)
        else:
            raise ValueError(f"Unknown page: {page}")