from bs4 import BeautifulSoup


ZENITH_BACKUP_PATH = r"ZenithGames\Zenith Games The Comprehensive Pathfinder Guides Guide.html"
ZENITH_DIV_ID = "post-body-500675332292381825"


class ZenithParser():
    """Parse "The Comprehensive Pathfinder Guides Guide" by Zenith Games
    """
    def __init__(self):
        with open(ZENITH_BACKUP_PATH) as f:
            soup = BeautifulSoup(f, "html.parser")
        self.post_div = soup.find(id=ZENITH_DIV_ID)

    def get_docs_urls(self):
        """Get Google Docs URLs linked in the HTML

        Returns:
            (list, list): List of Google Docs URLs
                          List of labels given to the links
        """
        docs_urls = []
        link_labels = []
        for tag in self.post_div.find_all("a"):
            url = tag["href"]
            if url.startswith("https://docs.google.com") or \
               url.startswith("https://drive.google.com"):
                docs_urls += [url]
                link_labels += [tag.text]
        return docs_urls, link_labels
