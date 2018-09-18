import urllib.request
from html.parser import HTMLParser
import re

extractedURLs = [] # variable for extracted urls

# pobiera kod htmlowy dostepny pod wskazanym adresem webowym (URL)
def gethtmlfromurl(url, proxy):
    # jeżli masz wartoś proxy to zdefiniuj proxy typu http
    if proxy:
        urllib.request.ProxyHandler({"http": proxy})
        
    # pobierz kod html z wskazanego adresu
    with urllib.request.urlopen(url) as response:
        htmlcode = response.read()
        return htmlcode # i go zwróc

# pobiera odnośniki typu 'a'/'href' z kodu html
def gethreffromhtml(htmlcode):
    parser = MyHTMLParser() # ninicjalizacja objektu HTMLParser
    parser.feed(str(htmlcode)) # sparsowanie kodu html
    parser.close()
    return extractedURLs
# ============================================================================
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

