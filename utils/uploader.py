# uploader.py
import os
import re
import requests
from urllib.parse import urlparse
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Setup Google Drive API
def authenticate_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'credentials.json'  # Update with your service account file

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

# Create folder in Google Drive
def create_folder(drive_service, folder_name, parent_folder_id=None):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')

# Upload file to Google Drive
def upload_file(drive_service, folder_id, file_path):
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# Main upload logic
def upload_crawled_files(domain, local_base_folder, drive_base_folder_id):
    drive_service = authenticate_drive()

    # Clean domain for folder naming
    safe_domain = re.sub(r'[^\w]', '_', domain)
    main_folder_name = f"{safe_domain}_crawl"

    # Create main folder under provided drive folder
    main_folder_id = create_folder(drive_service, main_folder_name, drive_base_folder_id)

    # Create subfolder webcrawl inside it
    subfolder_id = create_folder(drive_service, 'webcrawl', main_folder_id)

    # Upload files in local_base_folder/webcrawl
    target_folder = os.path.join(local_base_folder, 'webcrawl')
    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)
        if os.path.isfile(file_path):
            upload_file(drive_service, subfolder_id, file_path)

    print(f"Successfully uploaded to Google Drive under {main_folder_name}/webcrawl!")
