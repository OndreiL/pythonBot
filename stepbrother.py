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
    filteredNews = []
    soup = BeautifulSoup(page.text, "html.parser")
    soup = soup.find('div', id='block-system-main')
    for i in range (1,12,1):
        allNews = soup.findAll('div', class_=f"views-row-{i}")
        for data in allNews:
            if data.find('a') is not None:
                if datetime.strptime(data.find('span',{'class':"date-display-single"}).text,"%d.%m.%Y") > datetime.now() - timedelta(days=2):
                    #filteredNews.append(data.text)
                    pattern = '\d{5}'
                    data = data.find('div', class_='views-field-title')
                    num = re.findall(pattern, str(data))
                    filteredNews.append(f'{data.text} \n {join(num)}')
        #print(filteredNews)
    return filteredNews

if __name__ == '__main__':
    print (parse())
