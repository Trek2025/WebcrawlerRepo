# app.py
import os
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from uploader import upload_crawled_files

# --- CONFIGURATION ---
BASE_LOCAL_DIR = 'crawled_data'  # Local base directory
DRIVE_PARENT_FOLDER_ID = '1rIhsYfYUh4I3cdtM9-8-OjJzsG7r3ys-'  # Your Google Drive folder ID
# ----------------------

# Create local folders
def setup_local_folders(domain):
    safe_domain = re.sub(r'[^\w]', '_', domain)
    base_path = os.path.join(BASE_LOCAL_DIR, f"{safe_domain}_crawl", "webcrawl")
    os.makedirs(base_path, exist_ok=True)
    return base_path

# Very basic crawler (1-level deep)
def crawl_website(start_url, save_dir):
    try:
        response = requests.get(start_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {start_url}: {e}")
        return

    parsed_url = urlparse(start_url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Save main page
    main_file_path = os.path.join(save_dir, 'index.html')
    with open(main_file_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f"Saved: {main_file_path}")

    # Find and save internal links
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/'):
            full_url = domain + href
            links.add(full_url)
        elif href.startswith(domain):
            links.add(href)

    for link in links:
        try:
            res = requests.get(link, timeout=10)
            res.raise_for_status()
            subpage = BeautifulSoup(res.text, 'html.parser')

            filename = re.sub(r'[^\w]', '_', urlparse(link).path.strip('/')) or 'home'
            filepath = os.path.join(save_dir, f"{filename}.html")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(subpage.prettify())
            print(f"Saved: {filepath}")
        except Exception as e:
            print(f"Failed to fetch {link}: {e}")

# --- MAIN ---
def main():
    website_url = input("Enter the website URL to crawl (e.g., https://example.com): ").strip()
    parsed_url = urlparse(website_url)
    domain = parsed_url.netloc

    # Setup local folders
    save_dir = setup_local_folders(domain)

    # Crawl and save
    crawl_website(website_url, save_dir)

    # Upload to Google Drive
    upload_crawled_files(domain, os.path.join(BASE_LOCAL_DIR, f"{re.sub(r'[^\w]', '_', domain)}_crawl"), DRIVE_PARENT_FOLDER_ID)

if __name__ == "__main__":
    main()
