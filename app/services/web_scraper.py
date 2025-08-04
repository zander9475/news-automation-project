from newspaper import Article, ArticleException
import trafilatura
from urllib.parse import urlparse
from titlecase import titlecase
from bs4 import BeautifulSoup

def clean_author_string(authors_raw):
    """
    Cleans the raw author list from newspaper3k to remove duplicates and junk text.
    """
    if not authors_raw:
        return ""

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
    Tries to scrape a single URL.
    Returns a dictionary of article data on success.
    Raises an ArticleException on failure.
    """
    try:
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
            "washingtonpost": "Washington Post"
        }

        article = Article(url)
        article.download()
        article.parse()
        
        if not article.text:
            raise ArticleException("Scrape resulted in no content")
        
        # Capitalize article title
        capitalized_title = titlecase(article.title) if article.title else "Untitled"

        # Clean author list
        cleaned_authors = clean_author_string(article.authors)

        # Extract the base domain name from the URL
        source_domain = urlparse(url).netloc.replace("www.", "").split('.')[0].lower()

        # Look up source domain in the map. If not found, use capitalized domain name.
        formatted_source = SOURCE_MAP.get(source_domain, source_domain.title())

        # Get article content as html using trafilatura
        full_html= trafilatura.fetch_url(url)

        if full_html:
            unclean_html = trafilatura.extract(
                full_html,
                include_links=True,
                output_format='html',
                favor_recall=False,
                include_tables=False,
                include_images=False
            )
        
        if not unclean_html:
            return None

        # Parse with BeautifulSoup for cleaning
        soup = BeautifulSoup(unclean_html, 'html.parser')
        
        # Remove unwanted elements but be more selective
        # Don't remove all divs/spans as they might contain legitimate content
        unwanted_selectors = [
            'table', 'tr', 'td', 'th', 'thead', 'tbody', 'tfoot',
            'nav', 'aside', 'header', 'footer', 'figure', 'figcaption',
            '.ad', '.advertisement', '.social-share', '.related-articles',
            '.newsletter-signup', '.author-bio', '.tags', '.metadata'
        ]
        
        for selector in unwanted_selectors:
            for element in soup.select(selector):
                element.decompose()

        # Check if this looks like real article content
        if not is_likely_article_content(soup):
            raise ArticleException("This does not look like a regular news article." \
                                    "\nPlease add content manually if you would like to include it anyway.")

        # Convert the cleaned soup back to HTML string
        content_html = str(soup)

        return {
            "title": capitalized_title or "Untitled",
            "author": cleaned_authors,
            "source": formatted_source,
            "content": content_html,
            "url": url
        }
    except Exception as e:
        # Check if the error message contains the '403' error code
        if '403' in str(e):
            raise ArticleException("This website does not allow web scraping by bots.")
        elif '401' in str(e):
            raise ArticleException("This article is paywalled or requires a login\n(Usually a Google sign-in).")
        else:
            # For all other errors, re-raise the original exception
            raise ArticleException(e)
        
def is_likely_article_content(soup):
    """
    Determine if the extracted content looks like a real article
    """
    # Get all text content
    text = soup.get_text()
    
    # Count different types of content
    paragraphs = soup.find_all('p')
    lists = soup.find_all(['ul', 'ol'])
    list_items = soup.find_all('li')
    
    # Red flags for interactive graphics/data viz
    red_flags = 0
    
    # Too many list items relative to paragraphs
    if len(list_items) > len(paragraphs) * 3:
        red_flags += 1
    
    # Very short paragraphs (likely labels/captions)
    short_paragraphs = sum(1 for p in paragraphs if len(p.get_text().strip()) < 50)
    if short_paragraphs > len(paragraphs) * 0.7:
        red_flags += 1
    
    # Lots of numbers/percentages (suggests data viz)
    import re
    numbers = re.findall(r'\d+%|\d+\.\d+%|\$\d+', text)
    if len(numbers) > 20:
        red_flags += 1
    
    # Too many single-word list items (country lists, etc.)
    single_word_items = sum(1 for li in list_items if len(li.get_text().strip().split()) <= 2)
    if single_word_items > len(list_items) * 0.5:
        red_flags += 1
    
    return red_flags <= 1  # Allow some red flags, but not too many