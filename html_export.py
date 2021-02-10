from bs4 import BeautifulSoup


def archive_links(docs_urls, link_labels, archive_paths, fail_urls):
    # create an empty HTML page
    html_str = """
    <!doctype html>
    <html lang="en"></html>
    """
    soup = BeautifulSoup(html_str, "html.parser")
    html_tag = soup.html
    # add links to the HTML
    fail_offset = 0
    for i, docs_url in enumerate(docs_urls):
        if docs_url in fail_urls:
            fail_offset += 1
            continue
        # TODO fix archive ordering, linking, and error handling
        link_tag = soup.new_tag("a", href=archive_paths[i - fail_offset])
        link_tag.string = link_labels[i]
        html_tag.append(link_tag)
    html = soup.prettify()
    with open("metadata/archive_links.html", "wb") as f:
        f.write(html)
