import pandas as pd
from .article import Article
from ..utils import normalize_url

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
        self.seen_session_urls = set() # Keep a set of normalized URLs for fast lookup
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
                    keyword=row.get('keyword', ''),
                    authors=row.get('authors', []),
                    lead=row.get("lead")
                    )
                self.articles.append(article)
                # Populate the set of seen URLs
                if article.url:
                    self.seen_session_urls.add(normalize_url(article.url))            
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
        url = normalize_url(new_article.url)
        
        # Check for duplicate
        if url in self.seen_session_urls:
            print(f'Duplicate article found: {new_article.title}')
            return
        
        # If not duplicate, add article to list and url to set
        self.articles.append(new_article)
        self.seen_session_urls.add(url)

    def remove_article(self, index):
        """
        Removes an article from the Article list.
        @param index (int): The list position of the article to be removed.
        """
        del self.articles[index]

    def reorder_articles(self, new_title_order):
        """
        Takes a list of titles in a new order and rearranges the Articles list to that order
        """
        # Create dictionary for article lookup
        article_mapper = {article.title: article for article in self.articles}

        # Create list for reordered articles
        reordered_articles = [article_mapper[title] for title in new_title_order]

        # Replace unordered list with ordered list
        self.articles = reordered_articles

    def save(self):
        """
        Saves the Article list as a CSV file, overwriting the old file
        """
        if not self.articles:
            print("No articles to save.")
            return
        
        # Convert each Article object in the list to a dictionary
        articles_as_dicts = [article.to_dict() for article in self.articles]

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(articles_as_dicts)

        # Save the DataFrame to the CSV file
        df.to_csv(self.filepath, index=False)
