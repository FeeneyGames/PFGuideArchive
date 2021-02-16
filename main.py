from html_export import archive_links
from gdrive import DriveDownloader
from zenith import ZenithParser


# give Google API credentials to DriveDownloader
CRED_PATH = "pathfinderguidesguide-ace77dd25e21.json"
d_downloader = DriveDownloader(CRED_PATH)
# get URLs for Google Docs links
z_parser = ZenithParser()
docs_urls, link_labels = z_parser.get_docs_urls()
# archive Google Docs
archive_paths = d_downloader.archive_urls(docs_urls)
# output metadata in HTML
archive_links(link_labels, archive_paths)
