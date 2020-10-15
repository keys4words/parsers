import requests, random, os, logging, time, re
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime
import yagmail

from config import from_email, password, to_emails2, bcc


BASE_URL = 'https://zakupki.gov.ru'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FILE_WITH_INNS = os.path.join(BASE_DIR, 'keywords', 'zg_inns.txt')
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36', 'accept': '*/*'}


def set_logger():
    root_logger = logging.getLogger('zg')
    handler = logging.FileHandler('logs\\zg.log', 'a', 'utf-8')
    formatter = logging.Formatter(
        '%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)


def get_inns(filename):
    inns = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            inns.append(line.strip())
        return inns


def get_html(url, params=None):
    resp = requests.get(url=url, headers=HEADERS, params=params)
    return resp


def parsing(inns):
    root_logger = logging.getLogger('zg')
    for inn in inns:
        page_num = 1
        url = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={inn}&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber={page_num}&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&currencyIdGeneral=-1'

        _html = get_html(url)
        if _html.status_code == 200:
            soup = BeautifulSoup(_html.text, 'html.parser')
            if soup.find_all(
                    'div', class_='search-registry-entry-block box-shadow-search-input'):
                elements = soup.find_all(
                    'div', class_='search-registry-entry-block box-shadow-search-input')
                for el in elements:
                    number = el.find(
                        'div', class_='registry-entry__header-mid__number').a
                    tender_url = BASE_URL + number.get('href')
                    number = number.text.strip().replace('\n', '').replace('№ ', '')
                    name = el.find(text=re.compile("Объект закупки")
                                   ).parent.find_next_sibling()
                    name = name.text.strip().replace('\n', '')
                    # print(f'inn#{inn} number is {number}')
                    last_customer = ''
                    last_customer_url = ''
                    try:
                        customer = el.find(text=re.compile(
                            "Заказчик")).parent.find_next_sibling().a
                        customer_url = BASE_URL + customer.get('href')
                        customer = customer.text.strip().replace('\n', '')
                        last_customer = customer
                        last_customer_url = customer_url
                    except AttributeError:
                        customer = last_customer
                        customer_url = last_customer_url

                    price = el.find('div', class_="price-block__value")
                    price = price.text.strip().replace('\n', '').replace('\xa0', '')
                    release_date = el.find(text=re.compile(
                        "Размещено")).parent.find_next_sibling()
                    release_date = release_date.text
                    refreshing_date = el.find(text=re.compile(
                        "Обновлено")).parent.find_next_sibling()
                    refreshing_date = refreshing_date.text
                    ending_date = el.find(text=re.compile(
                        "Окончание подачи заявок")).parent.find_next_sibling()
                    ending_date = ending_date.text
                    res[number] = {
                        'name': name,
                        'url': tender_url,
                        'customer': customer,
                        'customer_url': customer_url,
                        'price': price,
                        'release_date': release_date,
                        'refreshing_date': refreshing_date,
                        'ending_date': ending_date
                    }
                root_logger.info(
                    f'Parsed {str(len(elements))} tenders for customer with INN #{inn}')
            else:
                root_logger.warning(
                    f'0 active tenders for customer with INN #{inn}')
                continue
        else:
            root_logger.warning(f'page {url} is not available')
            continue
    root_logger.info('='*36)


def save_results(res):
    wb = Workbook()
    ws = wb.active
    headers = ['Номер', 'Объект закупки', 'Ссылка на тендер', 'Заказчик',
               'Ссылка на Заказчика', 'Начальная цена', 'Размещено', 'Обновлено', 'Окончание подачи заявок']
    ws.append(headers)
    for tender_number, tender_info in res.items():
        ws.append([tender_number, tender_info['name'], tender_info['url'], tender_info['customer'],
                   tender_info['customer_url'], tender_info['price'], tender_info['release_date'], tender_info['refreshing_date'], tender_info['ending_date']])

    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 100
    ws.column_dimensions['D'].width = 80
    ws.column_dimensions['F'].width = 30
    ws.column_dimensions['G'].width = 30
    ws.column_dimensions['H'].width = 30

    name = os.path.abspath(os.path.dirname(__file__))
    name = os.path.join(name, 'out', datetime.now().strftime("%d-%m-%Y_%H-%M"))

    results_file_name = name + '_zg.xlsx'
    wb.save(results_file_name)
    root_logger = logging.getLogger('zg')
    root_logger.info(f'File {results_file_name} was successfully saved')
    return results_file_name

def sending_email(filename):
    body = "Below you find file with tenders from zakupki.gov"
    contents = [
        body,
        filename
    ]

    yagmail.register(from_email, password)
    yag = yagmail.SMTP(from_email)
    yag.send(
        to=to_emails2,
        subject="zakupki-gov",
        bcc=bcc,
        contents=contents,
    )
    root_logger = logging.getLogger('zg')
    root_logger.info(f'File {filename} was successfully sended')



res = dict()

set_logger()

parsing(get_inns(FILE_WITH_INNS))
# print(res)
sending_email(save_results(res))

root_logger = logging.getLogger('zg')
root_logger.info('='*36)
