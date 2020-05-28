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

script = '''
  headers = {
    ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    ['cookie'] = 'BITRIX_SM_SALE_UID=8f172cfd28b150ccd863f07789c5bb22; supportOnlineTalkID=IE4pGZEUa5lF2oboTGC5Wynv1NZ25MSr; supportOnlineTalkID=IE4pGZEUa5lF2oboTGC5Wynv1NZ25MSr; sort_catalog=default; order_catalog=asc; catalog_mode=list; count_catalog=24; PHPSESSID=819f65d998b662dff5647c8153371f9e; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1590699540%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D'
  }
  splash:set_custom_headers(headers)
  splash.private_mode_enabled = false
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(1))
  return splash:html()
'''


def get_tree(url):
    response = requests.get(url=url, headers=HEADERS)
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

    resp = requests.post(url='http://localhost:8050/run',
                         json={
                             'lua_source': script,
                             'url': url
                         })
    pprint.pprint(resp.content)
    tree_from_splash = html.fromstring(resp.content)

    p = {
        'name': ' '.join([first_name.strip(), second_name.strip()]),
        'photo': urljoin(base=HOST, url=get(p_info.xpath("//div[@class='tovar-detail__image']/a/@href"))),
        'price': get(p_info.xpath("//div[@class='tovar-detail__price'][1]/span/text()")).replace(' ', ''),
        #'desc': tree_from_splash.xpath("//div[contains(@class, 'tovar-detail__description')]/div/text()"),
        'short_desc': get(p_info.xpath("//div[@class='tovar-detail__short-description']/span[2]/text()")),
        #'characteristics': get(tree_from_splash.xpath("//table[@class='characteristics']/text()")),
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
get_content('https://www.tinko.ru/catalog/product/010002/')

# print(f'{len(res)} was parsed!')
