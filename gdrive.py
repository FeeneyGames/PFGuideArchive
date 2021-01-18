import io

from apiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials


class DriveDownloader():
    def __init__(self, cred_json_path):
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json_path, SCOPES)
        self.service = build("drive", "v3", credentials=creds)

    def download_doc(self, file_id):
        """Download a Google Doc from the URL

        Args:
            file_id (str): ID for the Google Doc

        Raises:
            Exception: [description]

        Returns:
            io.BytesIO: Binary stream representing the file
        """
        # construct request to Google Docs
        # TODO determine correct mimeType
        request = self.service.files().export_media(fileId=file_id, mimeType='text/html')
        # construct buffer and downloader
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)
        # download the file
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        return file_buffer

    def get_doc_type(self, file_id):
        # gets default metadata fields
        response_dict = self.service.files().get(fileId=file_id).execute()
        return response_dict["mimeType"]
