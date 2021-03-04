from bs4 import BeautifulSoup


def archive_links(link_labels, archive_paths):
    # create an empty HTML page
    html_str = """
    <!doctype html>
    <html lang="en"></html>
    """
    soup = BeautifulSoup(html_str, "html.parser")
    html_tag = soup.html
    # add links to the HTML
    for i, archive_path in enumerate(archive_paths):
        if archive_path is None:
            continue
        link_tag = soup.new_tag("a", href=archive_path)
        link_tag.string = link_labels[i]
        html_tag.append(link_tag)
        html_tag.append(soup.new_tag("br"))
    html = soup.prettify()
    with open("archive_links.html", "w", encoding="utf-8") as f:
        f.write(html)
