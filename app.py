from flask import Flask, request, jsonify
import os
from utils.crawler import crawl_website
from utils.cleaner import extract_texts_from_html
from utils.uploader import upload_to_drive

app = Flask(__name__)

@app.route('/')
def index():
    return "Website Crawler and Cleaner is Running!"

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.json
    website = data.get('url')

    if not website:
        return jsonify({"error": "No URL provided"}), 400

    crawl_path = '/tmp/crawled_site'
    clean_path = '/tmp/clean_text'

    try:
        crawl_website(website, crawl_path)
        extract_texts_from_html(crawl_path, clean_path)
        upload_to_drive(clean_path, folder_id='1HMUSzFQHoVJi0ZMZUGEhfBzfOU3iaFAI')

        return jsonify({"message": f"Website crawled, cleaned, and uploaded for {website}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
