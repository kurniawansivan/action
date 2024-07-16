from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_to_drive(file_path, credentials_path, folder_id):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
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
    print(f'File ID: {file.get("id")}')

if __name__ == "__main__":
    file_path = "build/app/outputs/flutter-apk/app-debug.apk"
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    folder_id = "1J1lVgJqMbTzY1IIY9g40M2nACT4dKZrL"
    upload_to_drive(file_path, credentials_path, folder_id)
