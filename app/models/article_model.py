import pandas as pd
from .article import Article

class ArticleManager:
    """
    Manages the collection of all Article objects.
    """
    def __init__(self, filepath="data/full_articles.csv"):
        """
        Initializes the ArticleModel.
        
        @param filepath (str): Path to the CSV file containing articles.
        """
        self.filepath = filepath
        self.articles = []
        self._load_articles()

    def _load_articles(self):
        """
        Private method: loads existing articles from the CSV file into a list of Article objects.
        """
        try:
            df = pd.read_csv(self.filepath)

            # Replace NaN values with None for optional fields
            df = df.where(pd.notna(df), None)

            # Create an Article object for each row in the dataframe
            for _, row in df.iterrows():
                article = Article(
                    title=row.get('title', ''),
                    content=row.get('content', ''),
                    source=row.get('source', ''),
                    url=row.get('url', ''),
                    authors=row.get('authors', []),
                    lead=row.get("lead")
                    )
                self.articles.append(article)
        except FileNotFoundError:
            print(f"{self.filepath} not found. Starting with empty article list.")
            self.articles = []

    def get_all_articles(self):
        """Returns a list of all Article objects"""
        return self.articles
    
    def add_article(self, new_article):
        """
        Takes a new Article object and adds it to the list of Articles.
        Performs a duplicate check before adding.
        """
        pass

    def remove_article(self, index):
        """
        Removes an article from the Article list.
        @param index (int): The position in the list of the article to be removed.
        """
        pass

    def reorder_articles(self, new_title_order):
        """
        Takes a list of titles in a new order and rearranges the Articles list to that order
        """
        pass

    def save(self):
        """
        Saves the Article list as a CSV file, overwriting the old file
        """
        pass