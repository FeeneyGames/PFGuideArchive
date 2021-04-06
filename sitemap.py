from urllib.parse import urljoin

from bs4 import BeautifulSoup


site_url = "https://feeneygames.github.io/PFGuideArchive/"
with open("archive_links.html", encoding="utf8") as f:
    soup = BeautifulSoup(f, "html.parser")
with open("sitemap.txt", "w", encoding="utf8") as f:
    f.write(site_url + "\n")
    for tag in soup.find_all("a"):
        url = tag["href"].replace("\\", "/")
        url = urljoin(site_url, url)
        f.write(url + "\n")
