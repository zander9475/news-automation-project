from newspaper import Article, ArticleException
import FreeSimpleGUI as sg
from urllib.parse import urlparse
from titlecase import titlecase

def clean_author_string(authors_raw): # Change to return a list of names
    """
    Cleans the raw author list from newspaper3k to remove duplicates and junk text.
    """
    if not authors_raw:
        return ""

    # Combine all found authors into a single string, separate by commas
    full_string = ", ".join(authors_raw)

    # List of common junk phrases to remove
    junk_phrases = ["Updated On", "By"]
    for phrase in junk_phrases:
        full_string = full_string.replace(phrase, "")

    # Split the string into individual names
    names = [name.strip() for name in full_string.split(',') if name.strip()]

    # Use a list to find unique names while preserving order
    unique_names = []
    for name in names:
        if name and name not in unique_names:
            unique_names.append(name)
            
    #Second cleaning step to remove combined names
    if len(unique_names) > 1:
        final_names = []
        for name_to_check in unique_names:
            is_redundant = False
            for other_name in unique_names:
                if name_to_check != other_name and other_name in name_to_check:
                    is_redundant = True
                    break
            if not is_redundant:
                final_names.append(name_to_check)
        unique_names = final_names
    
    return ", ".join(unique_names)


def scrape_article_from_url(url):
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

        # Clean the author string
        cleaned_authors = clean_author_string(article.authors).title()

        # Extract the base domain name from the URL
        source_domain = urlparse(url).netloc.replace("www.", "").split('.')[0].lower()

        # Look up source domain in the map. If not found, use capitalized domain name.
        formatted_source = SOURCE_MAP.get(source_domain, source_domain.title())

        return {
            "title": capitalized_title or "Untitled",
            "author": cleaned_authors,
            "source": formatted_source,
            "content": article.text,
            "url": url
        }
    except Exception as e:
        # Check if the error message contains the '403' error code
        if '403' in str(e):
            raise ArticleException("This website does not allow web scraping by bots.")
        else:
            # For all other errors, re-raise the original exception
            raise ArticleException(f"Failed to process article: {e}")


def prompt_for_manual_article():
    """
    Opens a GUI window to get article details manually.
    Returns a dictionary of article data if submitted, otherwise None.
    """
    layout = [
        [sg.Text("Please enter content manually.")],
        [sg.Text("Title:", size=(8,1)), sg.InputText(key="-TITLE-")],
        [sg.Text("Author:", size=(8,1)), sg.InputText(key="-AUTHOR-")],
        [sg.Text("Source: ", size=(8,1)), sg.InputText(key="-SOURCE-")],
        [sg.Text("Content:")],
        [sg.Multiline(size=(70, 15), key="-CONTENT-")],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window("Manual Entry Required", layout)
    event, values = window.read() # type: ignore
    window.close()

    if event == "Submit":
        # Capitalize title and source
        capitalized_title = titlecase(values["-TITLE-"])
        capitalized_source = values["-SOURCE-"].title()

        # Create the base dictionary with required fields
        article_data = {
            "title": capitalized_title,
            "source": capitalized_source,
            "content": values["-CONTENT-"],
        }
        # Check if the author field has text before adding it
        author_text = values["-AUTHOR-"]
        if author_text:
            article_data["author"] = author_text.title()
 
        return article_data  

    return None # Return None if user cancels