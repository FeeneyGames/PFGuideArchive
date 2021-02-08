from gdrive import DriveDownloader
from zenith import ZenithParser


# give Google API credentials to DriveDownloader
CRED_PATH = "pathfinderguidesguide-ace77dd25e21.json"
d_downloader = DriveDownloader(CRED_PATH)
# get URLs for Google Docs links
z_parser = ZenithParser()
docs_urls = z_parser.get_docs_urls()
# archive Google Docs
d_downloader.archive_urls(docs_urls)
