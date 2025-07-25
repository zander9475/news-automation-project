# search.py

import requests
import pandas as pd
import os
from urllib.parse import urlparse
from pandas.errors import EmptyDataError

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
        "/video", "/sport", "/athletic"
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
        "/about", "/contact", "/by", "/newsletter", "/people",
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


def normalize_url(url):
    """Strips a URL down to a clean, consistent format for matching."""
    if not url:
        return ""
    # Use urlparse to handle complex URLs safely
    parsed = urlparse(url)
    # Rebuild the URL with just the core domain and path
    # Removes http/https, www, query parameters, and fragments
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path.rstrip('/') # remove trailing slash
    return f"{domain}{path}"


def search_articles(api_key, cse_id, keywords, days_back):
    """
    Finds most relevant articles from the last X days, ensuring no duplicates.
    """
    articles = []
    seen_urls = set()
    for keyword in keywords:
        print(f"Searching for new articles for keyword: '{keyword}'...")
        try:
            # Set parameters for the Google Custom Search API
            params = {
                "key": api_key,
                "cx": cse_id,
                "q": keyword,
                "dateRestrict": f"d{days_back}"
            }
            # Query the API
            response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
            response.raise_for_status()

            # Convert raw JSON response to a structured format
            for item in response.json().get("items", []):
                url = item["link"]
                title = item.get("title", "")
                normalized_url = normalize_url(url)
                is_valid_article, reason = is_article(url, title)

                # Skip non-articles and print the reason why
                if not is_valid_article:
                    print(f"Skipping non-article ({reason}): {title} | {url}")
                    continue

                # Add article if not a duplicate
                if normalized_url not in seen_urls:
                    articles.append({
                        "Title": item["title"],
                        "URL": item["link"],
                        "Source": item.get("displayLink", ""),
                        "Keyword": keyword,
                    })
                    seen_urls.add(normalized_url)

        except requests.exceptions.RequestException as e:
            # This single block now catches all network/HTTP errors gracefully
            print(f"API request failed for keyword: '{keyword}'")
            
            # Optionally, provide more detail for specific errors
            if isinstance(e, requests.exceptions.HTTPError):
                if e.response.status_code == 429:
                    print("  > Reason: You have likely exceeded your daily API quota.")
                else:
                    print(f"  > Reason: HTTP Error {e.response.status_code} ({e.response.reason})")
            else:
                print(f"  > Reason: A network error occurred: {e}")
                
            continue

    if not articles:
        print("No new articles found across all keywords.")
        # Create empty excel to not break workflow, but don't use pandas for it
        if not os.path.exists("data/raw_results.xlsx"):
            pd.DataFrame().to_excel("data/raw_results.xlsx", index=False)
        return


    # Create dataframe of articles and save to excel sheet
    df = pd.DataFrame(articles)
    output_path = "data/raw_results.xlsx"
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Search Results', index=False)
        # (Formatting code remains the same)
        worksheet = writer.sheets['Search Results']
        for i, col in enumerate(df.columns):
            if col == 'URL':
                worksheet.set_column(i, i, 50)
                continue
            column_len = df[col].astype(str).map(len).max()
            header_len = len(col)
            width = max(column_len, header_len) if pd.notna(column_len) else header_len
            worksheet.set_column(i, i, width + 2)