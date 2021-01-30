import os
from urllib.request import urlopen
import zipfile

from gdrive import DriveDownloader
from zenith import ZenithParser


# print exceptions nicely
def print_exception(msg, identifier, exception):
    print(msg + "\n" + identifier)
    print(exception)
    print()


# give Google API credentials to DriveDownloader
CRED_PATH = "pathfinderguidesguide-ace77dd25e21.json"
d_downloader = DriveDownloader(CRED_PATH)
# get URLs for Google Docs links
z_parser = ZenithParser()
docs_urls = z_parser.get_docs_urls()
# get file IDs
visited_urls = []
docs_file_ids = []
for url in docs_urls:
    try:
        # update url if it redirects
        response = urlopen(url)
        redirect_url = response.url
        if redirect_url != url:
            print("Redirecting URL:")
            print(url + " => " + redirect_url + "\n")
            url = redirect_url
        # skip redundant urls
        if url in visited_urls:
            continue
    except Exception as e:
        print_exception("Exception for URL request:", url, e)
        continue
    try:
        # get the docs file id for export
        visited_urls += [url]
        file_id = d_downloader.url_to_file_id(url)
        if file_id not in docs_file_ids:
            docs_file_ids += [file_id]
    except Exception as e:
        print_exception("Exception for URL:", url, e)
# download documents
for file_id in docs_file_ids:
    try:
        d_downloader.save_doc(file_id)
    except Exception as e:
        print_exception("Exception for file ID:", file_id, e)
# extract zips
archive_dir = "archive"
zip_files = [file_name for file_name in os.listdir(archive_dir)
             if os.path.isfile(os.path.join(archive_dir, file_name)) and file_name[-4:] == ".zip"]
for file_name in zip_files:
    with zipfile.ZipFile(os.path.join(archive_dir, file_name), "r") as zip_f:
        zip_f.extractall(os.path.join(archive_dir, file_name[:-4]))
