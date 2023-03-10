from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse, urljoin
import html5lib
from datetime import datetime, timedelta

filteredNews = {'Atom_energy':{}}
url = 'https://www.atomic-energy.ru/'
def join(ref):
    ref = ''.join(ref)
    href = urljoin(url, ref)
    return(href)

def parse():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for i in range (2,5,1):
        p=0
        v=0
        soup = soup.find("div", {"class": "content rc7"})
        for sibling in soup.div.next_siblings:
            if sibling.previous_sibling.name == 'div':
                if sibling.previous_sibling['class'] == ["date-group"]:
                    Date = sibling.previous_sibling.string
                    filteredNews['Atom_energy'][Date] = []
            if sibling.name == 'p':
                filteredNews['Atom_energy'][Date].append({sibling.text: join(sibling.a['href'])})
        page = requests.get(join(soup.find('a', {'title': f'На страницу номер {i}'})['href']))
        soup = BeautifulSoup(page.content, "html.parser")
    return filteredNews

if __name__ == '__main__':
    print (parse())
