import io
import os

from apiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials


class DriveDownloader():
    def __init__(self, cred_json_path):
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json_path, SCOPES)
        self.service = build("drive", "v3", credentials=creds)

    def save_doc(self, file_id, update_archive=False):
        """Save document in archive

        Args:
            file_id (str): ID for the Google Doc
            update_archive (bool, optional): Whether to redownload and update archived Docs.
                                             Defaults to False.

        Raises:
            ValueError: File with unhandled type.
        """
        # get name and download type from Docs
        file_name = self.sanitize_name(self.get_doc_name(file_id))
        download_type = self.get_download_type(file_id)
        # map Docs file type to proper file extension
        type_to_extension = {
            "application/pdf": ".pdf",
            "application/zip": ".zip"
        }
        if download_type not in type_to_extension:
            raise ValueError("File with unhandled type:\n" + download_type)
        file_ext = type_to_extension[download_type]
        # download and write file if not archived or updating archive
        file_path = "archive/" + file_name + file_ext
        if not os.path.exists(file_path) or update_archive:
            file_buffer, _ = self.download_doc(file_id, download_type)
            with open(file_path, "wb") as f:
                f.write(file_buffer.getbuffer())

    def download_doc(self, file_id, download_type=None):
        """Download a Google Doc from the file id

        Args:
            file_id (str): ID for the Google Doc
            download_type (str, optional): mimeType to export file as. Defaults to None.

        Returns:
            (io.BytesIO, str): Binary stream representing the file,
                               Type of file stream
        """
        # determine type to export document as
        if download_type is None:
            download_type = self.get_download_type(file_id)
        # construct request for export URLs
        url_request = self.service.files().get(fileId=file_id, fields="exportLinks")
        export_urls = url_request.execute()["exportLinks"]
        # construct request to get exported file
        request = self.service.files().export_media(fileId=file_id, mimeType=download_type)
        # use export links to avoid file size limit instead of export function
        request.uri = export_urls[download_type]
        # construct buffer and downloader
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)
        # download the file
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return file_buffer, download_type

    def get_doc_metadata(self, file_id):
        """Gets default Docs metadata fields

        Args:
            file_id (str): ID for the Google Doc

        Returns:
            dict: Metadata dict
        """
        response_dict = self.service.files().get(fileId=file_id).execute()
        return response_dict

    def get_doc_type(self, file_id):
        """Gets Doc mimeType

        Args:
            file_id (str): ID for the Google Doc

        Returns:
            str: mimeType for the Doc
        """
        return self.get_doc_metadata(file_id)["mimeType"]

    def get_download_type(self, file_id):
        """Convert Doc mimeType to desired export mimeType

        Args:
            file_id (str): ID for the Google Doc

        Raises:
            ValueError: File ID identifies document with unhandled type.

        Returns:
            str: Desired export mimeType
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
        return download_type

    def get_doc_name(self, file_id):
        """Gets Doc name

        Args:
            file_id (str): ID for the Google Doc

        Returns:
            str: Name of the Doc
        """
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

    def sanitize_name(self, name):
        """Map invalid path character to a similar unicode character

        Args:
            name (str): Name to sanitize

        Returns:
            str: Name sanitized for filepath usage
        """
        char_to_sanitized = {
            "<": "˂",
            ">": "˃",
            ":": "։",
            "\"": "ʺ",
            "/": "∕",
            "\\": "∖",
            "|": "ǀ",
            "?": "Ɂ",
            "*": "∗"
        }
        return "".join(char_to_sanitized[char] if char in char_to_sanitized else char
                       for char in name)
