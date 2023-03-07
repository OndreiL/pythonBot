from bs4 import BeautifulSoup
import requests

url = 'https://rosatom.ru/journalist/arkhiv-novostey/'
page = requests.get(url)
print(page.status_code)


filteredNews = []
sourse = []

soup = BeautifulSoup(page.text, "html.parser")

# print(soup)
allNews = soup.findAll('a', class_='whiteBG')

for data in allNews:
    if data.find('span', class_='title') is not None:
        filteredNews.append(data.text)
for data in filteredNews:
    print(data)





