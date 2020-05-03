import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
           'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'output/cars.csv'

def get_html(url, params=None):
    res = requests.get(url=url, headers=HEADERS, params=params)
    return res

def get_pagination(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_="page-item mhide")
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition_area')
    cars = []
    for item in items:
        usd_price = item.find('span', class_='green bold size18')
        if usd_price:
            usd_price = usd_price.get_text().replace(' ', '').replace('$','')
        else:
            usd_price = 'Цену уточняйте'
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'link': HOST + item.find('a').get('href'),
            'uah_price': item.find('span', class_='grey size13').get_text().replace(' грн', '').replace(' ', ''),
            'usd_price': usd_price,
            'city': item.find('svg', class_='svg svg-i16_pin').find_next('strong').get_text(),
        })
    return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'цена в гривнах', 'Цена в $', 'Город'])
        for row in items:
            writer.writerow([row['title'], row['link'], row['uah_price'], row['usd_price'], row['city']])

def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pagination(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count} ...')
            html = get_html(URL, params={'page': page})
            get_content((html.text))
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'--- {len(cars)} позиций спарсено ---')
        os.startfile(FILE)
    else:
        print('Error')

parse()