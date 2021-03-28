from html_export import archive_links
from gdrive import DriveDownloader
from web import save_webpages_with_path
from zenith import ZenithParser


# give Google API credentials to DriveDownloader
CRED_PATH = "pathfinderguidesguide-ace77dd25e21.json"
d_downloader = DriveDownloader(CRED_PATH)
# get master URL reference
z_parser = ZenithParser()
urls, link_labels, link_classes = z_parser.get_guide_urls()
# get URLs for non-Docs links and archive
non_docs_urls, non_docs_link_labels = z_parser.get_non_docs_urls()
non_docs_archive_paths = save_webpages_with_path(non_docs_urls)
# get URLs for Google Docs links and archive
docs_urls, docs_link_labels = z_parser.get_docs_urls()
docs_archive_paths = d_downloader.archive_urls(docs_urls)
# combine archive paths into single list
archive_paths = [None] * len(urls)
url_path_lists = [
    (non_docs_urls, ["#"] * len(non_docs_urls)),
    (docs_urls, docs_archive_paths),
]
for i, url in enumerate(urls):
    for url_list, path_list in url_path_lists:
        try:
            index = url_list.index(url)
            archive_paths[i] = path_list[index]
            break
        except ValueError:
            pass
# output metadata in HTML
archive_links(link_labels, link_classes, archive_paths)
