from ..models.article_manager import ArticleManager
from ..views.widgets.search_dialog import SearchDialog

class MainController:
    """
    Controls top-level application logic, such as switching pages
    """
    def __init__(self, view):
        # Store main window as instance attribute
        self.view = view

        # Create article manager
        self.article_manager = ArticleManager()

    def _connect_signals(self):
        """
        Connects signals from the view to controller methods.
        """
        self.view.main_menu_widget.search_requested.connect(self.show_search_dialog)
        self.view.main_menu_widget.search_results_page_requested.connect(self.show_search_results)
        self.view.main_menu_widget.collection_page_requested.connect(self.show_collection_page)
        self.view.main_menu_widget.preview_articles_page_requested.connect(self.show_preview_articles)

    def show_search_dialog(self):
        """Displays the search dialog for Google search."""
        dialog = SearchDialog(self.view) # Create an instance of your dialog
    
        # .exec() shows the dialog and waits for the user to click OK or Cancel
        if dialog.exec(): 
            days_back = dialog.get_selected_days() # Get the value from the dialog
            # ... run the search with the days_back value ...

    def show_search_results(self):
        """Displays the latest search results."""
        self.view.Stack.setCurrentWidget(self.view.search_results_widget)

    def show_collection_page(self):
        """Displays the article collection page."""
        self.view.Stack.setCurrentWidget(self.view.collection_widget)

    def show_preview_articles(self):
        """Displays the preview articles page."""
        self.view.Stack.setCurrentWidget(self.view.preview_widget)

