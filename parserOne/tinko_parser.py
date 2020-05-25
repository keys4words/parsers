import requests
import time
from bs4 import BeautifulSoup
import csv
from lxml import html
from urllib.parse import urljoin
import pprint


HOST = 'https://www.tinko.ru'
URL = 'https://www.tinko.ru/catalog/category/30/'
URL = URL + '?count=24'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
           'accept': '*/*'}
FILE = 'output/tinko.csv'

res = []

def get_tree(url):
    response = requests.get(url=url, headers=HEADERS)
    print(response.content)
    return html.fromstring(html=response.content)


def get(list_elements):
    try:
        return str(list_elements.pop(0)).strip().replace('\n', '')
    except:
        return ''


def get_content(url):
    p_info = get_tree(url)
    first_name = str(get(p_info.xpath("//h2/text()")))
    second_name = str(get(p_info.xpath("//h1/text()")))
    p = {
        'name': ' '.join([first_name.strip(), second_name.strip()]),
        'photo': urljoin(base=HOST, url=get(p_info.xpath("//div[@class='tovar-detail__image']/a/@href"))),
        'price': get(p_info.xpath("//li[1]/div[1]/span[1]/text()")).replace(' ', ''),
        'desc': str(p_info.xpath("//div[contains(@class, 'tovar-detail__description active')]/div/text()")),
        'short_desc': get(p_info.xpath("//div[@class='tovar-detail__short-description']/span[2]/text()")),
        'characteristics': get(p_info.xpath("//table[@class='characteristics']/text()")),
        'url': url,
    }
    return p


def scrape(url):
    tree = get_tree(url)
    products_list = tree.xpath("//div[@class='catalog-products__item-title']")
    for product_info in products_list:
        product_url = product_info.xpath("./a/@href")[0]
        product_url = urljoin(base=HOST, url=product_url)
        product = get_content(product_url)
        res.append(product)

    next_page = tree.xpath("//div[contains(@class, 'bot-pagination')]//a[contains(text(), 'Следующая')]/@href")
    if len(next_page) != 0:
        next_page_url = urljoin(base=HOST, url=next_page[0])
        scrape(url=next_page_url)



# scrape(url=URL)
pprint.pprint(get_content('https://www.tinko.ru/catalog/product/010002/'))

# print(f'{len(res)} was parsed!')
