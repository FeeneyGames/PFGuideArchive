from html_export import archive_links
from gdrive import DriveDownloader
from zenith import ZenithParser


# give Google API credentials to DriveDownloader
CRED_PATH = "pathfinderguidesguide-ace77dd25e21.json"
d_downloader = DriveDownloader(CRED_PATH)
# get master URL reference
z_parser = ZenithParser()
urls, link_labels, link_classes = z_parser.get_guide_urls()
# get URLs for Google Docs links
docs_urls, docs_link_labels = z_parser.get_docs_urls()
# archive Google Docs
docs_archive_paths = d_downloader.archive_urls(docs_urls)
# output metadata in HTML
archive_links(docs_link_labels, docs_archive_paths)
