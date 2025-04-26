import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from utils.uploader import upload_directory_to_drive

def crawl_website(url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    filename = os.path.join(output_dir, 'index.html')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f"Saved {url} to {filename}")

    for link_tag in soup.find_all('a', href=True):
        link = urljoin(url, link_tag['href'])
        parsed = urlparse(link)
        if parsed.netloc != urlparse(url).netloc:
            continue  # Skip external links
        if parsed.path.endswith('.html'):
            try:
                sub_response = requests.get(link)
                sub_response.raise_for_status()
                sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
                sub_filename = os.path.join(output_dir, parsed.path.lstrip('/').replace('/', '_'))
                os.makedirs(os.path.dirname(sub_filename), exist_ok=True)
                with open(sub_filename, 'w', encoding='utf-8') as f:
                    f.write(sub_soup.prettify())
                print(f"Saved {link} to {sub_filename}")
            except Exception as e:
                print(f"Failed to fetch {link}: {e}")

def main():
    website_url = input("Enter the website URL to crawl (e.g., https://example.com): ").strip()
    parsed_url = urlparse(website_url)
    domain_name = parsed_url.netloc

    # Local directory named after the domain
    local_directory = f"{domain_name.replace('.', '_')}_crawl"

    print(f"Crawling {website_url}...")
    crawl_website(website_url, local_directory)

    print("Uploading to Google Drive...")
    upload_directory_to_drive(local_directory, domain_name)

    print("✅ Done!")

if __name__ == "__main__":
    main()
