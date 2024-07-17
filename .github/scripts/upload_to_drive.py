from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json
import base64

def upload_to_drive(file_path, credentials_info, folder_id):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    try:
        # Decode the base64-encoded JSON credentials
        credentials_json = base64.b64decode(credentials_info).decode('utf-8')
        credentials_data = json.loads(credentials_json)
    except Exception as e:
        print("Failed to decode JSON from credentials info.")
        print(f"Error: {e}")
        raise
    
    credentials = service_account.Credentials.from_service_account_info(
        credentials_data, scopes=SCOPES)

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
    credentials_info = os.getenv("GCP_CREDENTIALS_JSON")
    folder_id = os.getenv("GCP_FOLDER_ID")
    
    if not credentials_info:
        print("GCP_CREDENTIALS_JSON environment variable is not set.")
        raise ValueError("GCP_CREDENTIALS_JSON is not set.")
    
    uploaded_file = upload_to_drive(file_path, credentials_info, folder_id)
    print(f'File ID: {uploaded_file.get("id")}')
