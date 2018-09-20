from tozdautils import get_html_from_url, get_href_from_html, \
    get_hrefs_by_pattern
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

# proxy switch 1 - use proxy, 0 - don't use proxy
with_proxy = 0
# proxy definition
proxy = "192.168.247.8:8080"
# link to the page containt all issues for given year
# link do strony wyświetlającej wszystkie wydania w danym roku
url = "http://pbc.biaman.pl/dlibra/publication?id=36201&tab=3"
# String distinguishes links to the particular issues (list of issues)
# in a given year
# ciąg po którym można odróżnić linki do poszczególnych wydań w danym roku
pattern = "Życie Nowogródzkie : tygodnik poświęcony sprawom"
# pattern to selecting out only links to the page of issue
issue_href_pattern = r".+http.+/\d+\?tab=1.+\d{4}."
# Start and stop position to get out http string from the whole tag
# using string.index[]
url_start_idx = "http"
url_end_idx = "?tab=1"
# chrome webdriver configuration to be run headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# get html code from the page under url link
html_code = get_html_from_url(url, proxy, with_proxy)


# sort out only href tags
hrefs = get_href_from_html(html_code)


# get urls to issues from single year
newspaper_urls = get_hrefs_by_pattern(hrefs, pattern)
issue_in_year_urls = []
for newspaper_url in newspaper_urls:
    # print(newspaper_url)
    issue_href = re.search(issue_href_pattern, str(newspaper_url))
    if issue_href:
        urlStart = newspaper_url.index(url_start_idx)
        urlStop = newspaper_url.index(url_end_idx)
        issue_in_year_urls.append(newspaper_url[urlStart:urlStop+len(url_end_idx)])


print("Info: \t\t\tFound ", len(issue_in_year_urls), " issues in!")
number_of_issues = len(issue_in_year_urls)

# execute urls from above in order to execute script and get in return
# direct url to the page of issue
url_to_issue_page = []
for issue_in_year_url in issue_in_year_urls:
    browser = webdriver.Chrome(chrome_options=chrome_options)
    print("INFO: opening url:\t\t\t", issue_in_year_url)
    browser.get(issue_in_year_url)
    print("INFO: url in return:\t\t", browser.current_url)
    number_of_issues = number_of_issues - 1
    url_to_issue_page.append(browser.current_url)
    print("INFO: Issues to go:\t\t\t", number_of_issues)
    browser.quit()


# Na stronie z końcówką tab=1 poszukaj linka zdefinowanego w zmiennej
# pattern_for_issue i na podstawie tego linak wygeneruj JSONA dla Kantu
# w formacie
# link do konkretnego wydania w formacie PDF
# pattern_for_issue = r"http://pbc.biaman.pl/Content/34863/Zycie_Nowogrodzkie_34_1927.12.31.pdf"


"""
{
    "Commands": [
        {
            "Command": "open"
            "Target": "<ODNALEZIONYLINK>",
            "Value": ""
        },
        {
            ...
        }
    ]
}
"""

# link przy pop-upie klikniętym "pobierz"
# http://pbc.biaman.pl/dlibra/doczip?id=34863
# 'http://pbc.biaman.pl/dlibra/publication/36235?tab=1
