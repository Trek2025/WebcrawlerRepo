# WebcrawlerRepo
Webcrawler and BeautifulSoup Repo
WebcrawlerRepo is a lightweight, production-ready Flask application that:

✅ Crawls an entire website, including all subpages

✅ Cleans and extracts readable text from HTML pages

✅ Uploads clean .txt files to Google Drive

✅ Provides a simple API endpoint to trigger the whole workflow

Built to help power Retrieval-Augmented Generation (RAG) pipelines, AI knowledge bases, and document ingestion processes with minimal setup.

🚀 Features
Website crawling using wget

Text extraction with BeautifulSoup (removes menus, scripts, footers, etc.)

Automatic upload of clean data to Google Drive

Cloud-deployable (designed for platforms like Render.com)

Simple API interface — send a POST request, get results

🛠 Project Structure
plaintext
Copy
Edit
/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── utils/
│   ├── crawler.py          # Crawls websites using wget
│   ├── cleaner.py          # Cleans and extracts readable text
│   └── uploader.py         # Uploads files to Google Drive
├── README.md               # This file
├── .gitignore              # Python cache + auth file exclusions
⚙️ Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/WebcrawlerRepo.git
cd WebcrawlerRepo
2. Install Dependencies
Create a virtual environment (recommended):

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
Install required Python libraries:

bash
Copy
Edit
pip install -r requirements.txt
3. Configure Google Drive Authentication
This app uses PyDrive to upload files.
You'll need to authenticate the first time manually:

bash
Copy
Edit
python
>>> from pydrive.auth import GoogleAuth
>>> gauth = GoogleAuth()
>>> gauth.LocalWebserverAuth()
Follow the browser popup and login process.
It will save your credentials locally.

4. Run Locally
bash
Copy
Edit
python app.py
App will start at http://localhost:8000.

🌐 API Usage
📍 POST /crawl
Endpoint:
/crawl

Body Parameters:

json
Copy
Edit
{
  "url": "https://example.com"
}
What happens:

Crawls the full website

Extracts clean text

Uploads .txt files to Google Drive

Responds with a success or error message

🚀 Deploying to Render
You can easily deploy this app to Render.com:

Create a new Web Service.

Connect your GitHub repo.

Set:

Build Command: pip install -r requirements.txt

Start Command: python app.py

Set environment to Python 3.

Hit Deploy!

⚡ Improvements (Future Roadmap)
Auto-create a new Google Drive folder for each website crawl

Compress extracted text into a .zip archive for easy download

Support scheduled crawling (e.g., daily/weekly updates)

Add multi-threaded crawling for large websites

Optional S3 / Azure blob storage upload instead of Drive

🤝 Contributions
Pull requests and contributions are welcome!
Please open an issue first to discuss major changes.

📜 License
This project is licensed under the MIT License.
