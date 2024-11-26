import sys
import requests
from bs4 import BeautifulSoup

def fetch_and_extract_gifs(base_path, search_query):
    """
    Fetch HTML content from a URL and extract the first 10 .gif image URLs.
    
    Args:
        base_path (str): The base URL path to search on
        search_query (str): The search query to append to the URL
    
    Returns:
        list: A list of the first 10 .gif image URLs found in the HTML
    """
    # Construct the full URL with the base path and search query
    url = f"{base_path}{search_query}"
    
    try:
        response = requests.get(url)
        
        # Raise an exception for bad HTTP responses
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all img tags and filter for .gif URLs
        gif_images = [
            img['src'] for img in soup.find_all('img', src=True) 
            if img['src'].lower().endswith('.gif')
        ]
        
        # Return the first 10 gif URLs (or fewer if less than 10 exist)
        return gif_images[:10]
    
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        return []

def main():
    # Check if correct number of arguments was provided
    if len(sys.argv) < 3:
        print("Usage: python script.py <base_path> <search_query>", file=sys.stderr)
        print("Example: python script.py https://example.com/search/ cats", file=sys.stderr)
        sys.exit(1)
    
    # Get the base path and search query from command line arguments
    base_path = sys.argv[1]
    search_query = sys.argv[2]
    if not base_path.endswith('/'):
        base_path += '/'
    
    gif_urls = fetch_and_extract_gifs(base_path, search_query)
    for gif_url in gif_urls:
        print(gif_url)

if __name__ == "__main__":
    main()