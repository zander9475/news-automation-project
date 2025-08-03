from .article_controller import ArticleController
from ..models.article_manager import ArticleManager
from ..views.widgets.search_dialog import SearchDialog
from ..services.google_searcher import search_articles
from PySide6.QtWidgets import QMessageBox
from typing import Optional
import os
from dotenv import load_dotenv
import json

class MainController:
    """
    Controls top-level application logic (e.g. switching pages)
    """
    def __init__(self, view):
        # Store main window as instance attribute
        self.view = view

        # Create article manager
        self.article_manager = ArticleManager()

        # Create article controller
        self.article_controller = ArticleController(self.article_manager, self.view)

        # Ensure necessary directories exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        # Connect signals
        self._connect_signals()

        # Load cached search results if available
        self._load_cached_results()

    def _connect_signals(self):
        """
        Connects signals from the view to controller methods.
        """
        # Main menu page signals
        self.view.main_menu_widget.search_requested.connect(self.show_search_dialog)
        self.view.main_menu_widget.search_results_page_requested.connect(self.show_search_results)
        self.view.main_menu_widget.articles_page_requested.connect(self.show_article_management_page)

        # Search results page signals
        self.view.search_results_widget.rerun_search_requested.connect(self.show_search_dialog)
        self.view.search_results_widget.main_menu_requested.connect(self.show_main_menu)

        # Article management page signals
        self.view.article_management_widget.main_menu_requested.connect(self.show_main_menu)
        self.view.article_management_widget.manual_input_requested.connect(self.show_manual_input_page)

        # Manual input page signals
        self.view.manual_input_widget.submission_cancelled.connect(self.show_article_management_page)

    def show_main_menu(self):
        """Displays the main menu page"""
        self.view.Stack.setCurrentWidget(self.view.main_menu_widget) 

    def show_search_dialog(self):
        """Displays the search dialog for Google search."""
        dialog = SearchDialog(self.view)
    
        # Show the dialog and waits for the user to click OK or Cancel
        if dialog.exec(): 
            days_back = dialog.get_selected_days() # Get the value from the dialog
            # Pass the selected days back to the search handler
            self._handle_search(days_back)

    def show_search_results(self):
        """Displays the latest search results."""
        self.view.Stack.setCurrentWidget(self.view.search_results_widget)

    def show_article_management_page(self):
        """Displays the article management page."""
        self.view.Stack.setCurrentWidget(self.view.article_management_widget)

    def show_manual_input_page(self):
        """Displays the manual input page"""
        self.view.Stack.setCurrentWidget(self.view.manual_input_widget)

    def _handle_search(self, days_back):
        """
        Handles the search operation by calling the search service and updating the view.
        """
        # Load API key and CSE ID from environment variables
        load_dotenv()
        api_key = os.getenv("API_KEY")
        cse_id = os.getenv("CSE_ID")

        # Load keywords from JSON file
        with open("keywords.json", "r") as f:
            keywords = json.load(f)["keywords"]

        if not keywords:
            print("No keywords provided for search.")
            return

        # Call the search service
        articles = search_articles(api_key, cse_id, keywords, days_back)

        # Save results to cache file
        with open("data/last_search_cache.json", "w") as f:
            json.dump(articles, f, indent=4)

        # Update the search results widget with the new articles
        self.view.search_results_widget.display_results(articles)
        
        # Switch to the search results page
        self.show_search_results()

    def _load_cached_results(self):
        try:
            with open("data/last_search_cache.json", "r") as f:
                articles = json.load(f)
                if articles:
                    self.view.search_results_widget.display_results(articles)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is empty, do nothing
            pass