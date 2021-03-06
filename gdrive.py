import io
import os
from multiprocessing.dummy import Pool
from urllib.request import urlopen
import zipfile

from apiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials

from utils import print_exception


class DriveDownloader():
    def __init__(self, cred_json_path):
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json_path, SCOPES)
        self.service = build("drive", "v3", credentials=creds)

        # number of threads to use when multithreading
        self.num_threads = 4

    def archive_urls(self, docs_urls, update_archive=False):
        """Archive Docs from their URLs

        Args:
            docs_urls (list): List of URLs to Google Docs
            update_archive (bool, optional): Whether to redownload and update archived Docs.
                                             Defaults to False.

        Returns:
            list: List of archive paths or None
        """
        # get file IDs
        docs_file_ids = self.get_doc_ids(docs_urls)
        # download documents
        file_paths = self.save_docs(docs_file_ids, update_archive=update_archive)
        # extract zips
        for i, file_path in enumerate(file_paths):
            if file_path is not None and file_path[-4:] == ".zip":
                with zipfile.ZipFile(file_path, "r") as zip_f:
                    folder_path = file_path[:-4]
                    zip_f.extractall(folder_path)
                    # change filepath to the html file
                    html_file_name = None
                    for zip_info in zip_f.filelist:
                        file_name = zip_info.filename
                        if len(file_name) > 5 and file_name[-5:] == ".html":
                            html_file_name = file_name
                            break
                    file_paths[i] = os.path.join(folder_path, html_file_name)
        return file_paths

    def save_doc(self, file_id, update_archive=False):
        """Save document in archive

        Args:
            file_id (str): ID for the Google Doc
            update_archive (bool, optional): Whether to redownload and update archived Docs.
                                             Defaults to False.
        """
        if file_id is None:
            return None
        file_path = None
        try:
            # get name and download type from Docs
            file_name = self.sanitize_name(self.get_doc_name(file_id))
            download_type = self.get_download_type(file_id)
            # map Docs file type to proper file extension
            type_to_extension = {
                "application/pdf": ".pdf",
                "application/zip": ".zip",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx"
            }
            if download_type not in type_to_extension:
                raise ValueError("File with unhandled type:\n" + download_type)
            file_ext = type_to_extension[download_type]
            # create file path without duplicate extensions
            if file_name[-len(file_ext):] != file_ext:
                file_path = "archive/" + file_name + file_ext
            else:
                file_path = "archive/" + file_name
            # get rid of invalid trailing characters for ZIP files (causes issues when extracting)
            if file_path[-4:] == ".zip":
                invalid_chars = [" ", "."]
                while file_path[-5] in invalid_chars:
                    file_path = file_path[:-5] + ".zip"
            # download and write file if not archived already or if updating archive
            if not os.path.exists(file_path) or update_archive:
                file_buffer, _ = self.download_doc(file_id, download_type)
                with open(file_path, "wb") as f:
                    f.write(file_buffer.getbuffer())
        except Exception as e:
            print_exception("Exception for file ID:", file_id, e)
            file_path = None
        return file_path

    def save_docs(self, file_ids, update_archive=False):
        """Save document in archive

        Args:
            file_ids (str): List of IDs for the Google Docs or None
            update_archive (bool, optional): Whether to redownload and update archived Docs.
                                             Defaults to False.
        """
        # process downloads
        file_paths = [self.save_doc(file_id, update_archive) for file_id in file_ids]
        return file_paths

    def download_doc(self, file_id, download_type=None):
        """Download a Google Doc from the file id

        Args:
            file_id (str): ID for the Google Doc
            download_type (str, optional): mimeType to download file as. Defaults to None.

        Returns:
            (io.BytesIO, str): Binary stream representing the file,
                               Type of file stream
        """
        request = self.download_request(file_id, download_type)
        # construct buffer and downloader
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)
        # download the file
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return file_buffer, download_type

    def download_request(self, file_id, download_type=None):
        """Create request to download a Google Doc from the file id

        Args:
            file_id (str): ID for the Google Doc
            download_type (str, optional): mimeType to download file as. Defaults to None.

        Returns:
            HttpRequest: Request to download a Google Doc from the file id
        """
        # determine type to export document as
        if download_type is None:
            download_type = self.get_download_type(file_id)
        # determine download method from mimeType
        export_types = ["application/zip",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
        download_types = ["application/pdf"]
        if download_type in export_types:
            # construct request for export URLs
            url_request = self.service.files().get(fileId=file_id, fields="exportLinks")
            export_urls = url_request.execute()["exportLinks"]
            # construct request to get exported file
            request = self.service.files().export_media(fileId=file_id, mimeType=download_type)
            # use export links to avoid file size limit instead of export function
            request.uri = export_urls[download_type]
        elif download_type in download_types:
            request = self.service.files().get_media(fileId=file_id)
        else:
            raise ValueError("Unexpected download type:\n" + download_type)
        return request

    def get_doc_id(self, docs_url):
        docs_file_id = None
        redirect_url = None
        try:
            # update url if it redirects
            response = urlopen(docs_url)
            redirect_url = response.url
            if redirect_url != docs_url:
                print("Redirecting URL:")
                print(docs_url + " => " + redirect_url + "\n")
        except Exception as e:
            print_exception("Exception for URL request:", docs_url, e)
        if redirect_url is not None:
            try:
                # get the docs file id for export
                file_id = self.url_to_file_id(redirect_url)
                docs_file_id = file_id
            except Exception as e:
                print_exception("Exception for URL:", redirect_url, e)
        return docs_file_id

    def get_doc_ids(self, docs_urls):
        """Gets Docs IDs needed for API calls

        Args:
            docs_urls (list): URLs linking or redirecting to Docs files

        Returns:
            (list, list): List of Docs IDs
                          List of failed urls
        """
        # process Docs IDs on multiple threads
        thread_pool = Pool(self.num_threads)
        docs_file_ids = thread_pool.map(self.get_doc_id, docs_urls)
        # close threads, but don't bother waiting for them to free resources
        thread_pool.close()
        return docs_file_ids

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
            "application/vnd.google-apps.document": "application/zip",
            "application/vnd.google-apps.spreadsheet":
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
        if url.startswith("https://docs.google.com/forms/"):
            raise ValueError("Forms not supported")
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
