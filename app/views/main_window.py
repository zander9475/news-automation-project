from PySide6.QtWidgets import QMainWindow, QStackedWidget
from .widgets.main_menu_widget import MainMenuWidget
from .widgets.article_management_widget import ArticleManagementWidget
from .widgets.search_results_widget import SearchResultsWidget
from .widgets.manual_input_widget import ManualInputWidget

class MainWindow(QMainWindow):
    """
    Defines main application window.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News Automation Tool")
        self.setGeometry(300, 100, 800, 600)
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components.
        """
        # Create a stacked widget to manage different views
        self.Stack = QStackedWidget(self)

        # Create an instance of each view widget
        self.main_menu_widget = MainMenuWidget()
        self.article_management_widget = ArticleManagementWidget()
        self.search_results_widget = SearchResultsWidget()
        self.manual_input_widget = ManualInputWidget()

        # Add the widgets to the stacked widget
        self.Stack.addWidget(self.main_menu_widget)
        self.Stack.addWidget(self.article_management_widget)
        self.Stack.addWidget(self.search_results_widget)
        self.Stack.addWidget(self.manual_input_widget)

        # Set initial page to main menu
        self.Stack.setCurrentWidget(self.main_menu_widget)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.Stack)