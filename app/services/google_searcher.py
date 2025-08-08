import requests
from ..utils import normalize_url, is_article

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
                "num": 5,
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
                        "title": item["title"],
                        "url": item["link"],
                        "source": item.get("displayLink", ""),
                        "keyword": keyword,
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

    # Return article list to controller        
    return articles