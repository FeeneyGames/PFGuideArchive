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
# combine archive paths into single list
archive_paths = [None for _ in range(len(urls))]
for i, url in enumerate(urls):
    try:
        index = docs_urls.index(url)
        archive_paths[i] = docs_archive_paths[index]
    except ValueError:
        pass
# output metadata in HTML
archive_links(link_labels, link_classes, archive_paths)
