import os
import re
import pickle
import mimetypes
import io
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive folder ID where all crawls will be organized
DRIVE_PARENT_FOLDER_ID = "1rIhsYfYUh4I3cdtM9-8-OjJzsG7r3ys-"  # Change this

# Google API Scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = service_account.Credentials.from_service_account_file(
                'credentials.json', scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def sanitize_folder_name(domain):
    domain = domain.lower().replace('.', '_')
    domain = re.sub(r'[^a-z0-9_]', '_', domain)
    return f"{domain}_crawl"

def create_subfolder(service, parent_folder_id, folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_folder_id}' in parents"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if items:
        print(f"Folder '{folder_name}' already exists in Drive.")
        return items[0]['id']
    else:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Created folder '{folder_name}' in Drive.")
        return folder.get('id')

def upload_file(service, file_path, folder_id):
    file_name = os.path.basename(file_path)
    mimetype, _ = mimetypes.guess_type(file_path)
    media = MediaFileUpload(file_path, mimetype=mimetype)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    uploaded = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded file '{file_name}' to folder ID {folder_id}")

def upload_directory_to_drive(local_directory, website_domain):
    service = authenticate_drive()
    sanitized_folder_name = sanitize_folder_name(website_domain)
    domain_folder_id = create_subfolder(service, DRIVE_PARENT_FOLDER_ID, sanitized_folder_name)

    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            upload_file(service, local_path, domain_folder_id)
