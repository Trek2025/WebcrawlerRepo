import os
from urllib.parse import urlparse
from utils.crawler import crawl_website
from utils.uploader import upload_directory_to_drive
from utils.html_to_text import extract_texts_from_html_folder

def main():
    url = input("Enter the website URL to crawl (e.g., https://example.com): ").strip()
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.replace(".", "_")

    # Folder names
    crawl_output_dir = f"{domain_name}_crawl"
    text_output_dir = f"{domain_name}_texts"

    # Step 1: Crawl website
    print(f"\n🚀 Crawling {url}...")
    crawl_website(url, crawl_output_dir)

    # Step 2: Upload HTML files to Drive
    print(f"\n☁️ Uploading HTMLs to Google Drive folder '{domain_name}_crawl'...")
    upload_directory_to_drive(crawl_output_dir, domain_name + "_crawl")

    # Step 3: Extract text files from crawled HTMLs
    print(f"\n🧹 Extracting clean text from HTMLs...")
    extract_texts_from_html_folder(crawl_output_dir, text_output_dir)

    # Step 4: Upload TXT files to Drive
    print(f"\n☁️ Uploading clean text files to Google Drive folder '{domain_name}_texts'...")
    upload_directory_to_drive(text_output_dir, domain_name + "_texts")

    print("\n✅ All done! You can now point Flowise to the text files in Drive.")

if __name__ == "__main__":
    main()
