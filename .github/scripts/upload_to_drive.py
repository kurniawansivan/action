from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_to_drive(file_path, credentials_path, folder_id):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    if not os.path.exists(credentials_path):
        print(f"Credentials file does not exist: {credentials_path}")
        raise FileNotFoundError(f"Credentials file does not exist: {credentials_path}")
    
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='application/vnd.android.package-archive')

    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    return file

if __name__ == "__main__":
    file_path = os.getenv("APK_PATH")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    folder_id = os.getenv("GCP_FOLDER_ID")
    
    print(f"Using credentials file: {credentials_path}")
    print(f"Uploading APK: {file_path} to folder: {folder_id}")

    uploaded_file = upload_to_drive(file_path, credentials_path, folder_id)
    print(f'File ID: {uploaded_file.get("id")}')
