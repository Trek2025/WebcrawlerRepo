import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from utils.uploader import upload_directory_to_drive

# Maximum crawling depth
MAX_DEPTH = 2

def clean_domain_name(url):
    domain = urlparse(url).netloc
    return domain.replace(".", "_")

def save_page(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def is_valid_link(link, base_domain):
    if not link.startswith("http"):
        return True  # Allow relative links
    parsed_link = urlparse(link)
    return parsed_link.netloc == base_domain

def crawl(url, folder_path, visited, depth=0):
    if depth > MAX_DEPTH:
        return
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url} - Status code: {response.status_code}")
            return
    except Exception as e:
        print(f"Exception while fetching {url}: {e}")
        return

    parsed_url = urlparse(url)
    if url in visited:
        return
    visited.add(url)

    # Save the page
    path = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = os.path.join(folder_path, f"{path}.html")
    save_page(response.text, filename)

    # Parse links and crawl them
    soup = BeautifulSoup(response.text, "html.parser")
    base_domain = parsed_url.netloc
    for link_tag in soup.find_all("a", href=True):
        link = link_tag['href']
        absolute_link = urljoin(url, link)
        if is_valid_link(absolute_link, base_domain):
            crawl(absolute_link, folder_path, visited, depth + 1)

def main():
    target_url = input("Enter the website URL to crawl (e.g., https://example.com): ").strip()
    domain_name = clean_domain_name(target_url)
    local_directory = f"{domain_name}_crawl"
    
    print(f"Crawling {target_url} up to {MAX_DEPTH} levels...")
    visited = set()
    crawl(target_url, local_directory, visited)

    print(f"Saved crawled pages to {local_directory}")
    
    print("Uploading to Google Drive...")
    upload_directory_to_drive(local_directory, domain_name)
    print("Upload complete!")

if __name__ == "__main__":
    main()
