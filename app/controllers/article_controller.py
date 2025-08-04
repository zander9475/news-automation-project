from ..models.article import Article
from ..services.web_scraper import scrape_url
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal, Slot, QObject
from typing import Optional

class ArticleController(QObject):
    """
    Controls logic to perform CRUD operations on Articles. Communicates with ArticleManager
    """
    # Custom signals
    manual_article_added = Signal()

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self._connect_signals()

        # Load existing articles to article management page
        self._refresh_articles_view()

    def _connect_signals(self):
        # Search results page signals
        self.view.search_results_widget.article_addition_requested.connect(self.handle_search_result_add)

        # Article management page signals
        self.view.article_management_widget.url_scrape_requested.connect(self._handle_manual_url_add)
        self.view.article_management_widget.article_preview_requested.connect(self._show_article_preview)
        self.view.article_management_widget.edit_article_requested.connect(self._handle_article_edit)

        # Manual input page signals
        self.view.manual_input_widget.article_submitted.connect(self._handle_manual_input_add)

        # Article manager model signals
        self.model.articles_changed.connect(self._refresh_articles_view)

    @Slot()
    def _refresh_articles_view(self):
        articles = self.model.get_all_articles()
        self.view.article_management_widget.populate_list(articles)

    @Slot(dict)
    def handle_search_result_add(self, result_data: dict):
        """
        Adds an article added by the user through the "Add to Email" button on the search results page
        
        @param result_data (dict): A dictionary of the article's data so far (title, url, source, keyword)
        """
        # Fetch the url and keyword
        url = result_data.get("url")
        keyword = result_data.get("keyword")
        if not (url and keyword): return

        # Call the helper, which returns the article and its addition status
        article, was_added = self._scrape_url_and_add(url, keyword)

        if article and was_added:
            # Success dialog
            QMessageBox.information(
                self.view, 
                "Success", 
                f"'{article.title}' was successfully added."
            )
        elif article and not was_added:
            # Duplicate error dialog
            QMessageBox.warning(
                self.view, 
                "Duplicate Article", 
                f"'{article.title}' is already in your collection."
            )

    @Slot(str)
    def _handle_manual_url_add(self, url: str):
        """
        Adds an article entered by the user through the URL field in the article management page

        @param url (str): The url of the article
        """
        article, was_added = self._scrape_url_and_add(url)

        if article and was_added:
            # Success dialog
            QMessageBox.information(
                self.view, 
                "Success", 
                f"'{article.title}' was successfully added."
            )
        elif article and not was_added:
            # Duplicate error dialog
            QMessageBox.warning(
                self.view, 
                "Duplicate Article", 
                f"'{article.title}' is already in your collection."
            )

    def _handle_manual_input_add(self, article: Article):
        """
        Adds an article entered through manual input to the article management page

        @param article (Article): the Article object to add
        """
        was_added = self.model.add_article(article)
        if was_added:
            # Success dialog
            QMessageBox.information(
                self.view, 
                "Success", 
                f"'{article.title}' was successfully added."
            )
        else:
            # Duplicate error dialog
            QMessageBox.warning(
                self.view, 
                "Duplicate Article", 
                f"'{article.title}' is already in your collection."
            )
        self.manual_article_added.emit()

    def _scrape_url_and_add(self, url: str, keyword: Optional[str] = None):
        """
        Private helper: Tries to scrape and add an article.

        @return tuple: (status, article_obj)
        """
        try:
            # Attempt to scrape, pass keyword in if coming from search results page
            article_dict = scrape_url(url)
            if keyword:
                article_dict['keyword'] = keyword

            # Create article object
            article = Article(**article_dict)

            # Attempt to add article to the model. Model returns status of article addition.
            was_added = self.model.add_article(article)

            return article, was_added
        except Exception as e:
            if 'login' in str(e):
                user_prompt = "Please attempt to login to the website.\nIf paywalled, add this article manually."
            else:
                user_prompt = "Please add this article manually."
            QMessageBox.critical(
                self.view,
                "Scrape Failed",
                f"Scrape failed: {e}\n\n{user_prompt}"
            )
            return None, None
        
    def _show_article_preview(self, index):
        """
        Retrieves article from ArticleManager. Updates preview pane with that article.

        @param index (int): The article's index in the articles order.
        """
        # Retrieve article from model
        article = self.model.get_single_article(index)

        # Pass article to preview pane and show it
        if article:
            self.view.article_management_widget.update_preview(article)

    def _handle_article_edit(self, article: Article):
        """
        Opens a pane to edit an existing article and updates the model if changes are saved.
        """
        if not article:
            return
        
        # Open the manual input widget with the article data
        self.view.manual_input_widget.set_article_data(article)
        self.view.Stack.setCurrentWidget(self.view.manual_input_widget)

        # Connect the submission signal to the ArticleManager's edit method
        self.view.manual_input_widget.article_submitted.connect(
            lambda edited_article: self.model.edit_article(
                self.model.get_all_articles().index(article), edited_article
            )
        )


