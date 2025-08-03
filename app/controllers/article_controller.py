from ..models.article import Article
from ..services.web_scraper import scrape_url
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Slot
from typing import Optional

class ArticleController:
    """
    Controls logic to perform CRUD operations on Articles. Communicates with ArticleManager
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        # Search results page signals
        self.view.search_results_widget.article_addition_requested.connect(self.handle_search_result_add)

        # Article management page signals
        self.view.article_management_widget.url_scrape_requested.connect(self.handle_manual_url_add)

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

        # Update the article management page
        all_articles = self.model.get_all_articles()
        self.view.articles_widget.display_articles(all_articles) 

    @Slot(str)
    def handle_manual_url_add(self, url: str):
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

    def _scrape_url_and_add(self, url: str, keyword: Optional[str] = None):
        """
        Private helper: Tries to scrape and add an article.

        @return tuple: (status, article_obj)
        """
        try:
            # Attempt to scrape, pass keyword in if coming from search results page
            print("Scraping...")
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