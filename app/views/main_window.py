from PySide6.QtWidgets import QMainWindow, QStackedWidget
from .widgets.main_menu_widget import MainMenuWidget
from .widgets.collection_widget import CollectionWidget
from .widgets.search_widget import SearchWidget
from .widgets.preview_articles_widget import PreviewArticlesWidget
from .widgets.manual_input_widget import ManualInputWidget

class MainWindow(QMainWindow):
    """
    Defines main application window.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News Automation Tool")
        self.setGeometry(300, 100, 800, 600)

    def initUI(self):
        """
        Initializes the user interface components.
        """
        # Create a stacked widget to manage different views
        self.Stack = QStackedWidget(self)

        # Create an instance of each view widget
        self.main_menu_widget = MainMenuWidget()
        self.collection_widget = CollectionWidget()
        self.search_widget = SearchWidget()
        self.preview_widget = PreviewArticlesWidget()
        self.manual_input_widget = ManualInputWidget()

        # Add the widgets to the stacked widget
        self.Stack.addWidget(self.main_menu_widget)
        self.Stack.addWidget(self.collection_widget)
        self.Stack.addWidget(self.search_widget)
        self.Stack.addWidget(self.preview_widget)
        self.Stack.addWidget(self.manual_input_widget)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.Stack)