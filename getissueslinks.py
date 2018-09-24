from tozdautils import get_html_from_url, get_href_from_html, \
    get_hrefs_by_pattern
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GENERAL CONFIG
# proxy switch 1 - use proxy, 0 - don't use proxy
with_proxy = 0
# proxy definition
proxy = "192.168.247.8:8080"
# chrome webdriver configuration to be run headless
chrome_options = Options()
chrome_options.add_argument("--headless")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONFIG FOR GUI TYPE 1
# gui_type = 1 # its like "Podlaska biblioteka"
# link to the page containt all issues for given year
# link do strony wyświetlającej wszystkie wydania w danym roku
# link to the page listing out all issues in a given year
# url = "http://pbc.biaman.pl/dlibra/publication?id=36201&tab=3"
# links to the pages listing out all issues in a given year
urls = ["http://pbc.biaman.pl/dlibra/publication?id=36201&tab=3",
        "http://pbc.biaman.pl/dlibra/publication?id=36841&tab=3",
        "http://pbc.biaman.pl/dlibra/publication?id=37390&tab=3",
        "http://pbc.biaman.pl/dlibra/publication?id=37824&tab=3",
        "http://pbc.biaman.pl/dlibra/publication?id=38302&tab=3",
        "http://pbc.biaman.pl/dlibra/publication?id=38540&tab=3",
        "http://pbc.biaman.pl/dlibra/publication?id=38574&tab=3",
        "http://pbc.biaman.pl/dlibra/publication?id=38646&tab=3"]
# String distinguishes links to the particular issues (list of issues)
# in a given year
# ciąg po którym można odróżnić linki do poszczególnych wydań w danym roku
pattern = "Życie Nowogródzkie : tygodnik poświęcony sprawom"
# pattern for getting year of the issue
year_pattern = r"\s\d{4}\s"
# pattern to selecting out only links to the page of issue
issue_href_pattern = r".+http.+/\d+\?tab=1.+\d{4}."
# Start and stop position to get out http string from the whole tag
# using string.index[]
url_start_idx = "http"
url_end_idx = "?tab=1"
# lint to zip file pattern
link_to_zip_file_pattern = r"\d{4,8}"
# beginning of URL to the zip file ling. Is attached to the zip_id variable
url_to_zip = "http://pbc.biaman.pl/Content/"
# file name in which urls to zip will be stored
final_urls_filename = "urls2zips.txt"


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONFIG FOR GUI TYPE 2

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MAIN
for url in urls:

    # get html code from the page under url link
    html_code = get_html_from_url(url, proxy, with_proxy)

    # sort out only href tags
    hrefs = get_href_from_html(html_code)

    # get urls to issues from single year
    newspaper_urls = get_hrefs_by_pattern(hrefs, pattern)
    issue_year = re.search(year_pattern, str(newspaper_urls[0]))
    print("Info: processing issues from year" + str(issue_year.group(0)))
    issue_in_year_urls = []
    for newspaper_url in newspaper_urls:

        # print(newspaper_url)
        issue_href = re.search(issue_href_pattern, str(newspaper_url))

        if issue_href:
            urlStart = newspaper_url.index(url_start_idx)
            urlStop = newspaper_url.index(url_end_idx)
            issue_in_year_urls.append(newspaper_url[urlStart:urlStop+len(url_end_idx)])

    print("\tINFO: Found ", len(issue_in_year_urls), " issues in",
          issue_year.group(0), "year!")

    number_of_issues = len(issue_in_year_urls)

    # execute urls from above in order to execute script and get in return
    # direct url to the page of issue
    urls_to_zips = []
    browser = webdriver.Chrome(chrome_options=chrome_options)
    for issue_in_year_url in issue_in_year_urls:
        print("\tINFO: opening url:\t\t\t", issue_in_year_url)
        browser.get(issue_in_year_url)
        issue_url = browser.current_url
        zip_id = re.search(link_to_zip_file_pattern, issue_url)
        issue_url_zip = url_to_zip + str(zip_id.group(0)) + "/zip/\n"
        print("\tINFO: url in return:\t\t", issue_url_zip)
        # writing urls aside in file
        file_final_urls = open(final_urls_filename, "a")
        file_final_urls.write(issue_url_zip)
        file_final_urls.close()
        urls_to_zips.append(issue_url_zip)
        number_of_issues = number_of_issues - 1
        print("\tINFO: Issues to go:\t\t\t", number_of_issues)
    browser.quit()

    # download all zips
    newbrowser = webdriver.Chrome()
    for url_to_zip in urls_to_zips:
        print("\tINFO: Getting zip package:\t\t\t", url_to_zip)
        newbrowser.get(url_to_zip)

    newbrowser.close()
    print("INFO: Year" + str(issue_year.group(0)) + "completed!")


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
