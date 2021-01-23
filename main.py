import os
import zipfile

from gdrive import DriveDownloader
from zenith import ZenithParser

# give Google API credentials to DriveDownloader
CRED_PATH = "pathfinderguidesguide-ace77dd25e21.json"
d_downloader = DriveDownloader(CRED_PATH)
# get URLs for Google Docs links
z_parser = ZenithParser()
docs_urls = z_parser.get_docs_urls()
# get file IDs
docs_file_ids = []
for url in docs_urls:
    try:
        file_id = d_downloader.url_to_file_id(url)
        if file_id not in docs_file_ids:
            docs_file_ids += [d_downloader.url_to_file_id(url)]
    except Exception as e:
        print("Exception for URL:\n" + url)
        print(e)
# download documents
for file_id in docs_file_ids:
    try:
        d_downloader.save_doc(file_id)
    except Exception as e:
        print("Exception for file ID:\n" + file_id)
        print(e)
# extract zips
archive_dir = "archive"
zip_files = [file_name for file_name in os.listdir(archive_dir)
             if os.path.isfile(os.path.join(archive_dir, file_name)) and file_name[-4:] == ".zip"]
for file_name in zip_files:
    with zipfile.ZipFile(os.path.join(archive_dir, file_name), "r") as zip_f:
        zip_f.extractall(os.path.join(archive_dir, file_name[:-4]))
