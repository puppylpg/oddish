import urllib.request


def open_url(url):
    page = urllib.request.urlopen(url)
    page_html = page.read().decode('utf-8')
    return page_html
