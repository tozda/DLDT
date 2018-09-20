import urllib.request
from html.parser import HTMLParser
import re

# variable for extracted urls
extracted_urls = []


# gets html code from web file under url
def get_html_from_url(url, proxy, with_proxy):

    if with_proxy == 1:  # if proxy variable define configure proxy
        urllib.request.ProxyHandler({"http": proxy})
        with urllib.request.urlopen(url) as response:
            html_code = response.read()
    else:
        with urllib.request.urlopen(url) as response:
            html_code = response.read()

    return html_code


# gets only hrefs from html file.  gets 'a' tags = http
def get_href_from_html(html_code):
    parser = MyHTMLParser()
    parser.feed(str(html_code))
    parser.close()
    return extracted_urls


def get_hrefs_by_pattern(hrefs, pattern):
    # Get only URLs referencing to the yearbooks of given newspaper
    urls_by_pattern = []
    for href in hrefs:
        href_string = str(href)
        my_href = re.search(pattern, href_string)
        if my_href:
            urls_by_pattern.append(href_string)

    return urls_by_pattern


# ==============================================================================


class MyHTMLParser(HTMLParser):
    """
    Parser for getting URLs
    Only 'a' tags considered
    TODO: 'a' tags with 'title' attribute
    """

    def handle_starttag(self, tag, attrs):

        if tag == 'a':
            for attr in attrs:
                title = re.search("title", str(attr))
                if title:
                    extracted_urls.append(attrs)

        return extracted_urls
