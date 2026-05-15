import asyncio
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')  # Path to the service account JSON file
# Define the root path based on the known location of main.py
ROOT_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOCAL_FILE_PATH = os.path.join(ROOT_FOLDER_PATH, 'labour_management.db')
REMOTE_FILE_NAME = 'labour_management.db'  # File name on Google Drive

# Google Drive API Scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    """Authenticate with Google Drive API using a service account."""
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

async def upload_file_to_drive(service):
    """Uploads or updates the SQLite file on Google Drive."""
    loop = asyncio.get_running_loop()
    try:
        # Search for an existing file by name in the specified Google Drive folder
        request = service.files().list(
            q=f"name='{REMOTE_FILE_NAME}' and '{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed=false",
            fields="files(id, name)"
        )
        results = await loop.run_in_executor(None, request.execute)

        # Delete existing file if found
        if results.get('files'):
            for file in results['files']:
                delete_request = service.files().delete(fileId=file['id'])
                await loop.run_in_executor(None, delete_request.execute)
                print(f"Deleted existing file '{file['name']}' on Google Drive.")
        else:
            print(f"File '{REMOTE_FILE_NAME}' not found; a new file will be uploaded.")

        # Upload the new file
        file_metadata = {
            'name': REMOTE_FILE_NAME,
            'parents': [GOOGLE_DRIVE_FOLDER_ID]
        }
        media = MediaFileUpload(LOCAL_FILE_PATH, resumable=True)
        create_request = service.files().create(body=file_metadata, media_body=media, fields='id')
        uploaded_file = await loop.run_in_executor(None, create_request.execute)
        print(f"File uploaded to Google Drive successfully. File ID: {uploaded_file.get('id')}")

    except HttpError as e:
        print(f"Failed to upload file to Google Drive: {e}")


async def download_file_from_drive(service):
    """Downloads the latest SQLite file from Google Drive to LOCAL_FILE_PATH."""
    loop = asyncio.get_running_loop()
    try:
        # Search for the file by name
        request = service.files().list(
            q=f"name='{REMOTE_FILE_NAME}' and '{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed=false",
            fields="files(id, name)"
        )
        results = await loop.run_in_executor(None, request.execute)

        if not results.get('files'):
            print(f"File '{REMOTE_FILE_NAME}' not found in Google Drive.")
            return

        # Download the file
        file_id = results['files'][0]['id']
        request = service.files().get_media(fileId=file_id)

        def download_sync():
            with open(LOCAL_FILE_PATH, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Download progress: {int(status.progress() * 100)}%")

        await loop.run_in_executor(None, download_sync)

        print(f"Downloaded file to {LOCAL_FILE_PATH} successfully.")

    except HttpError as e:
        print(f"Failed to download file from Google Drive: {e}")
