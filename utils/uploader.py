from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def upload_to_drive(folder_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authenticate manually once
    drive = GoogleDrive(gauth)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_metadata = {'title': file}
            if folder_id:
                file_metadata['parents'] = [{'id': folder_id}]
            gfile = drive.CreateFile(file_metadata)
            gfile.SetContentFile(file_path)
            gfile.Upload()
