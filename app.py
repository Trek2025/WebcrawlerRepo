import os
import time
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from utils.uploader import upload_directory_to_drive

MAX_DEPTH = 2

def save_page(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def is_valid_link(link, base_domain):
    parsed_link = urlparse(link)
    return parsed_link.netloc == "" or parsed_link.netloc == base_domain

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
        if response.status_code not in [200, 202]:  # Accept 200 and 202
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
            time.sleep(1)  # Polite crawling
            crawl(absolute_link, folder_path, visited, depth + 1)

def main():
    website_url = input("Enter the website URL to crawl (e.g., https://example.com): ").strip()

    parsed_url = urlparse(website_url)
    domain_name = parsed_url.netloc.replace(".", "_")
    local_directory = f"{domain_name}_crawl"

    print(f"Crawling {website_url} up to {MAX_DEPTH} levels...")
    os.makedirs(local_directory, exist_ok=True)
    crawl(website_url, local_directory)

    print("Uploading to Google Drive...")
    upload_directory_to_drive(local_directory, domain_name)
    print("Done!")

if __name__ == "__main__":
    main()
