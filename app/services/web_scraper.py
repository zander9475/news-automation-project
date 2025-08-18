from newspaper import Article, ArticleException
from titlecase import titlecase
import tldextract
import requests

def clean_author_string(authors_raw):
    """
    Cleans the raw author list from newspaper3k to remove duplicates and junk text.
    """
    if not authors_raw:
        return []

    cleaned_names = []
    junk_phrases = ["Updated On", "By"]

    # Loop through each string in the author list provided by newspaper3k
    for raw_string in authors_raw:
        # Remove any junk phrases from the string
        for phrase in junk_phrases:
            raw_string = raw_string.replace(phrase, "")

        # Split each string by commas in case it accidentally contains multiple names
        names = raw_string.split(',')

        # Add the cleaned names to cleaned names list
        for name in names:
            clean_name = name.strip()
            if clean_name:
                cleaned_names.append(clean_name)
            
    # Remove duplicate names
    unique_names = []
    for name in cleaned_names:
        if name not in unique_names:
            unique_names.append(name)
            
    # Remove combined names (e.g. "John Doe Jane Smith")
    if len(unique_names) > 1:
        combined_names = []
        # Loop through list
        for name in unique_names:
            # For each name, loop through rest of list
            for other_name in unique_names:
                # Combined name if name (outer loop) contains another name
                if other_name in name and other_name != name:
                    combined_names.append(name)
        # Include only names not found in combined names
        final_names = [name for name in unique_names if name not in combined_names]
        return final_names
    
    return unique_names

def scrape_url(url):
        """
        Tries live fetch first; if blocked or error, falls back to Google Cache.
        Returns article data dict on success, raises ArticleException on failure.
        """
        # Map domain names to source titles
        SOURCE_MAP = {
            "apnews": "Associated Press",
            "nytimes": "New York Times",
            "wsj": "Wall Street Journal",
            "politico": "POLITICO",
            "ft": "Financial Times",
            "cnbc": "CNBC",
            "scmp": "South China Morning Post",
            "foxnews": "Fox News",
            "washingtonpost": "Washington Post",
            "cnn": "CNN",
            "bloomberglaw": "Bloomberg"
        }

        # Set user agent (to avoid website blocks)
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )

        # Common request headers for both tools
        headers = {
            "User-Agent": user_agent,
            "Accept-Language": "en-US,en;q=0.9",
        }

        def fetch(url_to_fetch):
            """
            Fetches the URL and returns the HTML content.
            """
            try:
                response = requests.get(url_to_fetch, headers=headers)
                response.raise_for_status()
                html = response.text
                if not html.strip():
                    raise ArticleException("Empty HTML returned")
                return html
            except requests.RequestException as e:
                raise ArticleException(f"Could not fetch page: {e}")
        
        # Try live URL first
        try:
            html = fetch(url)
        except ArticleException as e_live:
            # On certain errors ('401', etc), try Google Cache fallback
            if isinstance(e_live.args[0], str) and any(code in e_live.args[0] for code in ['401', '403', '404']):
                cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
                try:
                    html = fetch(cache_url)
                except ArticleException as e_cache:
                    # Both failed
                    raise ArticleException(
                        f"Failed live URL ({e_live}) and Google Cache ({e_cache})"
                    )
            else:
                # Some other error: re-raise
                raise

        # Extract content with Newspaper3k
        article = Article(url)
        article.set_html(html)
        article.parse()
        
        if not article.text:
            raise ArticleException("Scrape resulted in no content")
        
        # Capitalize article title
        capitalized_title = titlecase(article.title) if article.title else None

        # Clean author list
        cleaned_authors = clean_author_string(article.authors)

        # Extract the base domain name from the URL
        source_domain = tldextract.extract(url).domain

        # Look up source domain in the map. If not found, use capitalized domain name.
        formatted_source = SOURCE_MAP.get(source_domain, source_domain.title())

        return {
            "title": capitalized_title,
            "author": cleaned_authors,
            "source": formatted_source,
            "content": article.text,
            "url": url
        }