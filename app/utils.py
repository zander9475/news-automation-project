from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

def text_to_html_paragraphs(text: str) -> str:
    """
    Converts a plain text string into an HTML string with <br><br> tags.

    - Splits text into paragraphs based on one or more empty lines.
    - Preserves single line breaks within a paragraph using <br>.
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    # Normalize different newline characters to \n
    text = text.replace('\r\n', '\n')

    # Split the text into paragraphs based on one or more blank lines
    paragraphs = re.split(r'\n\s*\n', text)

    html_paragraphs = []
    for p in paragraphs:
        # For each paragraph, replace internal newlines with <br>
        content = p.strip().replace('\n', '<br>')
        if content:
            html_paragraphs.append(content)

    # Join paragraphs with <br><br> tags for consistent paragraph spacing
    return "<br><br>".join(html_paragraphs)


def clean_and_format_html(dirty_html: str) -> str:
    """
    Cleans dirty HTML from a QTextEdit widget to a standardized format.

    - Keeps only <b>, <strong>, <i>, <em>, and <a> tags.
    - On <a> tags, it keeps ONLY the 'href' attribute.
    - Strips all other tags, attributes (like style, class), and document structure.
    - Converts paragraph structures into <br><br> for consistent paragraph spacing.
    """
    if not isinstance(dirty_html, str) or not dirty_html.strip():
        return ""

    soup = BeautifulSoup(dirty_html, 'html.parser')

    # Completely remove unwanted tags whose content is also unwanted
    tags_to_discard = [
        'script', 'style', 'head', 'meta', 'link', 'svg', 'canvas', 'math', 'table',
        'form', 'input', 'textarea', 'select', 'option', 'button', 'iframe'
    ]
    for tag in soup.find_all(tags_to_discard):
        tag.decompose()

    # Define the tags and attributes that are allowed
    allowed_tags = {'b', 'strong', 'i', 'em', 'a', 'p', 'br'}
    allowed_attributes = {'a': ['href']}

    # Find all HTML tags in the document
    for tag in soup.find_all(True):
        # If the tag is not allowed, remove the tag but keep its content
        if tag.name not in allowed_tags:
            tag.unwrap()
        else:
            # If tag is allowed, keep only allowed attributes
            attrs = dict(tag.attrs)
            for attr_name, _ in attrs.items():
                if tag.name in allowed_attributes and attr_name in allowed_attributes[tag.name]:
                    continue  # Keep this attribute
                # Remove unallowed attributes
                del tag[attr_name]

    # Get the HTML content from the body, as soup may have added <html>/<body> tags
    if soup.body:
        body_content = ''.join(str(c) for c in soup.body.contents)
    else:
        body_content = str(soup)

    # Convert <p> tags to <br><br> for consistent paragraph spacing.
    cleaned_html = re.sub(r'<p.*?>', '', body_content, flags=re.IGNORECASE)
    cleaned_html = re.sub(r'</p>', '<br><br>', cleaned_html, flags=re.IGNORECASE)

    # Remove any leading/trailing <br> tags that might result from cleaning
    cleaned_html = re.sub(r'^(<br\s*/?>\s*)+|(<br\s*/?>\s*)+$', '', cleaned_html)

    return cleaned_html.strip()


def normalize_url(url):
    """Strips a URL down to just domain and path for duplicate checking.
    Example: nytimes.com/2025/07/31/us/politics/white-house-ballroom-trump.html
    """
    if not url or not isinstance(url, str):
        return ""
    # Use urlparse to handle complex URLs safely
    parsed = urlparse(url)
    # Rebuild the URL with just the core domain and path
    # Removes http/https, www, query parameters, etc.
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path.rstrip('/') # remove trailing slash
    return f"{domain}{path}"


def is_article(url, title):
    """
    Determines if a result is likely to be a news article using layered checks.
    Returns (True, "") if it's an article.
    Returns (False, "reason") if it is not.
    """
    parsed = urlparse(url)
    path = parsed.path.lower()
    title = title.lower()

    # --- RULE 1: High-Priority Exclusions ---
    high_priority_path_exclusions = [
        "/print-edition", "/digital-print-edition", "/subscribe",
        "/archive", "/home", "/index", "/category", "/podcast", 
        "/video", "/sport", "/athletic", "/sitemap"
    ]
    for p in high_priority_path_exclusions:
        if p in path:
            return False, f"High-priority excluded path: '{p}'"
        
    high_priority_title_exclusions = [
        "live:", "live blog", "live updates"
    ]
    for term in high_priority_title_exclusions:
        if term in title:
            return False, f"High-priority excluded title: '{term}'"

    # --- RULE 2: Check for strong positive signals ---
    # If a URL has a date or a clear article pattern, approve it immediately.
    article_patterns = [
        "/article/", "/story/", "/post/", "/report/", "/202", 
        "/jan/", "/feb/", "/mar/", "/apr/", "/may/", "/jun/",
        "/jul/", "/aug/", "/sep/", "/oct/", "/nov/", "/dec/"
    ]
    if any(pattern in path for pattern in article_patterns):
        return True, "" # It's an article, no more checks needed.

    # --- RULE 3: Check for general negative signals ---
    # Path-based exclusions (less critical than high-priority ones)
    excluded_paths = [
        "/user", "/author", "/tags", "/topic", "/section",
        "/profile", "/account", "/login", "/signup", "/register",
        "/about", "/contact", "/by/", "/newsletter", "/people",
        "scmp.com/news/china/diplomacy", "/quotes", "/company",
        "/earnings", "scmp.com/opinion"
    ]
    for p in excluded_paths:
        if p in path:
            return False, f"Excluded path: '{p}'"

    # Title-based exclusions
    excluded_title_terms = [
        "sign up", "topic:", "author:",
        "homepage", "section:", "your daily", "briefing", 
        "bulletin", "alert", "update", "digest"
    ]
    for term in excluded_title_terms:
        if term in title:
            return False, f"Excluded title keyword: '{term}'"

    # --- RULE 4: Final structural checks ---
    if path.count('/') < 2:
        return False, "Path too shallow"
    if len(path) <= 30:
        return False, "Path too short"
    
    # If it passes all checks, assume it's an article.
    return True, ""