import requests
from lxml import html
from urllib.parse import urljoin
from pymongo import MongoClient

from settings import MONGO_DB_CONNECTION

URL = 'https://coinmarketcap.com/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
           'accept': '*/*'}

res = []


def insert_to_db(list_currencies):
    client = MongoClient(MONGO_DB_CONNECTION)
    db = client["currencies"]
    collection = db["price"]
    for currency in list_currencies:
        exists = collection.find_one({'_id': currency['_id']})
        if exists:
            if exists['name'] == currency['name'] and (exists['price'] != currency['price']) or exists['market cap'] != currency['market cap'] or exists['volume'] != currency['volume']:
                collection.replace_one({'_id': exists['_id']}, currency)
                print(f'Old item: {exists}\tNew item: {currency}')
        else:
            collection.insert_one(currency)
    client.close()


def get(list_elements):
    try:
        return list_elements.pop(0)
    except:
        return ''


def scrape(url):
    response = requests.get(url=url, headers=HEADERS)
    tree = html.fromstring(html=response.content)

    currencies = tree.xpath("//tr[@class='cmc-table-row']")
    for currency in currencies:
        c = {
            '_id': int(get(currency.xpath(".//td[contains(@class, 'by__rank')]/div/text()"))),
            'name': get(currency.xpath("//div[@class='cmc-table__column-name sc-1kxikfi-0 eTVhdN']/a/text()")),
            'market cap': get(currency.xpath(".//td[contains(@class, 'market-cap')]/div/text()")).replace(',',''),
            'price': get(currency.xpath(".//td[contains(@class, 'price')]/a/text()")).replace(',',''),
            'volume': get(currency.xpath(".//td[contains(@class, 'volume-24-h')]/a/text()")).replace(',',''),

        }
        res.append(c)

    next_page = tree.xpath("//div[contains(@class, 'cmc-split')]//a[contains(text(), 'Next')]/@href")
    if len(next_page) != 0:
        next_page_url = urljoin(base=URL, url=next_page[0])
        scrape(url=next_page_url)

scrape(url=URL)
insert_to_db(res)
print(f'{len(res)} was parsed!')



