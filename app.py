import os
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from utils.uploader import upload_directory_to_drive

# Set your Google Drive parent folder ID here
DRIVE_PARENT_FOLDER_ID = '1rIhsYfYUh4I3cdtM9-8-OjJzsG7r3ys-'

MAX_DEPTH = 2  # Maximum crawl depth

def is_valid_link(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain and parsed.scheme in ["http", "https"]

def save_page(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def crawl(url, folder_path, visited=None, depth=0):
    if visited is None:
        visited = set()

    if depth > MAX_DEPTH:
        return

    if url in visited:
        return

    print(f"Crawling {url} at depth {depth}...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url} - Status code: {response.status_code}")
            return
    except Exception as e:
        print(f"Exception while fetching {url}: {e}")
        return

    visited.add(url)

    # Save the current page
    parsed_url = urlparse(url)
    path = parsed_url.path.strip("/")
    if not path:
        path = "index"
    filename = os.path.join(folder_path, path.replace("/", "_") + ".html")
    save_page(response.text, filename)

    # Parse links and crawl them
    soup = BeautifulSoup(response.text, "html.parser")
    base_domain = parsed_url.netloc
    for link_tag in soup.find_all("a", href=True):
        link = link_tag['href']
        absolute_link = urljoin(url, link)
        if is_valid_link(absolute_link, base_domain):
            time.sleep(1)  # Be polite
            crawl(absolute_link, folder_path, visited, depth + 1)

def main():
    website_url = input("Enter the website URL to crawl (e.g., https://example.com): ").strip()

    if not website_url.startswith("http"):
        print("Invalid URL format. URL must start with http:// or https://")
        return

    parsed_url = urlparse(website_url)
    domain_name = parsed_url.netloc.replace('.', '_')  # example_com

    local_directory = f"{domain_name}_crawl"
    os.makedirs(local_directory, exist_ok=True)

    print(f"Crawling {website_url} up to {MAX_DEPTH} levels...")
    crawl(website_url, local_directory)

    print("Crawling completed!")
    print("Uploading to Google Drive...")

    upload_directory_to_drive(local_directory, domain_name, DRIVE_PARENT_FOLDER_ID)

    print("Upload completed successfully!")

if __name__ == "__main__":
    main()
