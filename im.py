from bs4 import BeautifulSoup
import requests

url = 'https://proryv2020.ru/ '
page = requests.get(url)
#print(page.status_code)


filteredNews = []
sourse = []
def imp():
    soup = BeautifulSoup(page.text, "html.parser")

    # print(soup)
    allNews = soup.findAll('div', class_='news-content')


    for data in allNews:
        if data.find('h4') is not None:
            filteredNews.append(data.text)
    # for data in filteredNews:
        # print(data)
    return (filteredNews)