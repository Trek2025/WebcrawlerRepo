import os
import re
import time
from urllib.parse import urlparse, urljoin

from playwright.sync_api import sync_playwright
from utils.uploader import upload_directory_to_drive

def sanitize_filename(url):
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', url)

def save_html(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def crawl_page(page, url, domain, visited, save_dir, max_depth, current_depth):
    if current_depth > max_depth or url in visited:
        return

    try:
        response = page.goto(url, wait_until="networkidle", timeout=15000)
        if not response or response.status >= 400:
            print(f"Failed to fetch {url} - Status code: {response.status if response else 'No Response'}")
            return
        print(f"Crawled {url}")

        visited.add(url)
        html_content = page.content()
        filename = sanitize_filename(urlparse(url).path.strip("/")) or "index"
        file_path = os.path.join(save_dir, f"{filename}.html")
        save_html(html_content, file_path)

        if current_depth < max_depth:
            links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
            for link in links:
                if link and domain in link:
                    crawl_page(page, link.split("#")[0], domain, visited, save_dir, max_depth, current_depth + 1)

    except Exception as e:
        print(f"Error crawling {url}: {str(e)}")

def main():
    website_url = input("Enter the website URL to crawl (e.g., https://example.com): ").strip()
    parsed_url = urlparse(website_url)
    domain = parsed_url.netloc
    if not domain:
        print("Invalid URL. Exiting.")
        return

    folder_name = f"{domain.replace('.', '_')}_crawl"
    save_dir = os.path.join(os.getcwd(), folder_name)
    os.makedirs(save_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Crawling {website_url} up to 2 levels...")
        visited = set()
        crawl_page(page, website_url, domain, visited, save_dir, max_depth=1, current_depth=0)

        browser.close()

    print("Uploading to Google Drive...")
    upload_directory_to_drive(save_dir, domain)
    print("Done!")

if __name__ == "__main__":
    main()
