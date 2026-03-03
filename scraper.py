import requests
from bs4 import BeautifulSoup
import sys


def fetching_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except:
        print("Error: ",url)
        sys.exit(1)
def parsing_page(html):
    soup_ = BeautifulSoup(html,"html.parser")
    title = soup_.title.get_text(strip=True)if soup_.title else "No tittle"
    body=soup_.body.get_text(" ",strip=True)if soup_.body else ""
    links= [a["href"]for a in soup_.find_all("a",href=True)]
    return title,body,links

if len(sys.argv)!= 2:
    print("puthon scraper.py <url>")
    sys.exit(1)
url = sys.argv[1]
html =  fetching_html(url)
title,body,links= parsing_page(html)

print("Page title:", title)
print("\n")
print(body)
print("\nLinks: ")
for link in links:
    print(link)

