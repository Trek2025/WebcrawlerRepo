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
            gfile = drive.CreateFile({'title': file})
            gfile.SetContentFile(file_path)
            gfile.Upload()
