import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from openpyxl import Workbook
import random, os, logging, time
from datetime import datetime
import yagmail
from config import from_email, password, to_emails, cc, bcc


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
    res = requests.get(url=url, headers=HEADERS, params=params)
    return res


def parsing(driver, inns):
    root_logger = logging.getLogger('zg')
    for inn in inns:
        page_num = 1
        url = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={inn}&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber={page_num}&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&currencyIdGeneral=-1'
        
        html = get_html(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html, 'html.parser')
            pagination = soup.find_all('span', class_="page-item mhide")

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


            try:
                parse_page(driver=driver)
                root_logger.info(f'parsing OK with INN: {inn}')
            except TimeoutException:
                root_logger.warning(f'timeout with INN: {inn}')
                continue
    root_logger.info(f'Parsed ' + str(len(res)) + ' tenders')


def parse_page(driver):
    pass




res = dict()

driver = webdriver.Chrome()
driver.maximize_window()
set_logger()

parsing(driver, get_inns(FILE_WITH_INNS))

root_logger = logging.getLogger('zg')
root_logger.info('There is NO tenders')
root_logger.info('='*36)

driver.quit()
