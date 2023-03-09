from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse, urljoin
import html5lib
from datetime import datetime, timedelta

url = 'https://www.atomic-energy.ru/'
page = requests.get(url)
print(page.status_code)

def join(ref):
    ref = ''.join(ref)
    href = urljoin(url, ref)
    return(href)

def parse():
    filteredNews = []
    soup = BeautifulSoup(page.text, "html.parser")
    soup = soup.find("div", {"class": "content rc7"})
    #print (soup)
    #allNews = soup.contents
    #allNews = soup.findAll('p')
    for sibling in soup.div.next_siblings:
        if sibling.previous_sibling.name == 'div':
            if sibling.previous_sibling['class'] == ["date-group"]:
             filteredNews.append(sibling.previous_sibling.string)
        if sibling.name == 'p':
            filteredNews.append(join(sibling.a['href']))
    return filteredNews

if __name__ == '__main__':
    print (parse())
