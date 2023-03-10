from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse, urljoin
import html5lib
from datetime import datetime, timedelta

url = 'https://mephi.ru/press/news/'
page = requests.get(url)
print(page.status_code)

def join(ref):
    ref = ''.join(ref)
    href = urljoin(url, ref)
    return(href)

def parse():
    filteredNews = {'Mephi':{}}
    soup = BeautifulSoup(page.text, "html.parser")
    soup = soup.find('div', id='block-system-main')
    for i in range (1,13,1):
        allNews = soup.findAll('div', class_=f"views-row-{i}")
        Date = str(datetime.now()).split(' ')[0]
        if i == 0:
            filteredNews['Mephi'][Date] = []
        for data in allNews:
            if data.find('a') is not None:
                    Date = str(datetime.strptime(data.find('span', {'class': "date-display-single"}).text, "%d.%m.%Y")).split(' ')[0]
                    pattern = '\d{5}'
                    data = data.find('div', class_='views-field-title')
                    num = re.findall(pattern, str(data))
                    try:
                        filteredNews['Mephi'][Date].append({data.text: join(num)})
                    except (KeyError):
                        filteredNews['Mephi'][Date] = []
                        filteredNews['Mephi'][Date].append({data.text: join(num)})
    return filteredNews

if __name__ == '__main__':
    print (parse())
