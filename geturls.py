import urllib.request
from html.parser import HTMLParser
import re


# variable for <a href=* tags
extractedURLs = []

# URL to top level of structure
level1structure = 'http://dlibra.kul.pl/dlibra/publication?id=14887'
# From GUI like Biblioteka Cyfrowa KUL i am looking for this string
# into 'title' attribute of href tag
level2structure = 'Ziemianin : organ Związku Ziemian. R.'


# liczę na to że tutaj znajdę podstawę do budowania
# linków bezpośrednich do PDFa aby mieć link do
# ściągnięcia go.

class MyHTMLParser(HTMLParser): # Parser html
    """
    Parser for getting URLs
    Only 'a' tags with 'title' attribute considered
    """
    # Only tag 'a'
    def handle_starttag(self, tag, attrs):

        if tag == 'a':
            extractedURLs.append(attrs)

        return extractedURLs

# if you have proxy uncomment and adjust line below
# urllib.request.ProxyHandler({"http": "192.168.247.8:8080"})  # proxy

# get html code from the online site
with urllib.request.urlopen(level1structure) as response:
    htmlcode = response.read()
parser = MyHTMLParser()
parser.feed(str(htmlcode))
parser.close()

# just show what you have
level2pattern = re.compile('*Ziemianin : organ Związku Ziemian\. R\.*')
level2urls = []
for extractedURL in extractedURLs:
#    print(extractedURL)
    level2match = level2pattern.match(str(extractedURL))
    if level2match:
        level2urls.append(extractedURL)


    print(level2urls)

print("EOF")  # debug
