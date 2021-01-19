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
        """Download a Google Doc from the file id

        Args:
            file_id (str): ID for the Google Doc

        Raises:
            Exception: [description]

        Returns:
            io.BytesIO: Binary stream representing the file
        """
        # determine correct mimeType
        cur_type = self.get_doc_type(file_id)
        type_map = {
            "application/pdf": "application/pdf",
            "application/vnd.google-apps.document": "application/zip"
        }
        if cur_type not in type_map:
            raise ValueError("File ID identifies document with unhandled type:\n" + cur_type)
        else:
            download_type = type_map[cur_type]
        # construct request to Google Docs
        request = self.service.files().export_media(fileId=file_id, mimeType=download_type)
        # construct buffer and downloader
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)
        # download the file
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return file_buffer

    def get_doc_metadata(self, file_id):
        # gets default metadata fields
        response_dict = self.service.files().get(fileId=file_id).execute()
        return response_dict

    def get_doc_type(self, file_id):
        return self.get_doc_metadata(file_id)["mimeType"]

    def get_doc_name(self, file_id):
        return self.get_doc_metadata(file_id)["name"]

    def url_to_file_id(self, url):
        if not (url.startswith("https://docs.google.com") or
                url.startswith("https://drive.google.com")):
            raise ValueError("Unexpected URL domain")
        if url.startswith("https://docs.google.com/spreadsheet/"):
            raise ValueError("Spreadsheets not yet handled")
        file_id = None
        if "/d/" in url:
            start_ind = url.find("/d/")
            if start_ind > -1:
                start_ind += 3
                file_id = url[start_ind:]
                end_ind = file_id.find("/")
                if end_ind > -1:
                    file_id = file_id[:end_ind]
        else:
            fields = ["id", "docid", "srcid"]
            for field in fields:
                if "?" + field + "=" in url or \
                   "&" + field + "=" in url:
                    file_id = self.extract_url_query_field(url, field)
                    break
        if file_id is None:
            raise ValueError("URL does not match known patterns:\n" + url)
        if file_id.endswith("#"):
            file_id[:-1]
        return file_id

    def extract_url_query_field(self, url, field):
        start_ind = url.find(field + "=") + len(field) + 1
        field = url[start_ind:]
        end_ind = field.find("&")
        if end_ind > -1:
            field = field[:end_ind]
        return field
