from urllib.parse import urlparse

def normalize_url(url):
    """Strips a URL down to a clean, consistent format for matching."""
    if not url:
        return ""
    # Use urlparse to handle complex URLs safely
    parsed = urlparse(url)
    # Rebuild the URL with just the core domain and path
    # Removes http/https, www, query parameters, etc.
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path.rstrip('/') # remove trailing slash
    return f"{domain}{path}"