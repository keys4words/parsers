from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from openpyxl import Workbook
import random, os, logging, time
from datetime import datetime
import yagmail
from config import from_email, password, to_emails, cc, bcc


# FILE_WITH_KEYWORDS = 'D:\\USERDATA\\Documents\\4git\\parsers\\tenders\\keywords\\zm_keywords.txt'
FILE_WITH_KEYWORDS = 'D:\\USERDATA\\Documents\\4git\\parsers\\tenders\\keywords\\test.txt'
FILE_WITH_REGIONS = 'D:\\USERDATA\\Documents\\4git\\parsers\\tenders\\keywords\\zm_regions.txt'
BASE_URL = 'https://zakupki.mos.ru/purchase/list?page=1&perPage=50&sortField=relevance&sortDesc=true&filter=%7B%22auctionSpecificFilter%22%3A%7B%7D%2C%22needSpecificFilter%22%3A%7B%7D%2C%22tenderSpecificFilter%22%3A%7B%7D%7D&state=%7B%22currentTab%22%3A1%7D'


def show_filters(driver):
    btn_all_filters = driver.find_element_by_xpath('//div[@class="PublicListHeaderActionsStyles__ButtonsContainer-yl44rw-5 bVVobJ"]')
    btn_all_filters.click()

    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//label[contains(text(), "Наименование закупки")]/following-sibling::div/input')))


def get_keywords(filename):
    keywords = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            keywords.append(line.strip())
        return keywords

def save_results(res):
    wb = Workbook()
    ws = wb.active
    headers = ['Номер','Наименование', 'Ссылка на тендер', 'Заказчик', 'Ссылка на Заказчика', 'Цена', 'Регион', 'Закон', 'Дата']
    ws.append(headers)
    for tender_number, tender_info in res.items():
        ws.append([tender_number, tender_info['name'], tender_info['name_url'], tender_info['customer'], tender_info['customer_url'], tender_info['price'], tender_info['region'], tender_info['law'], tender_info['tdate']])

    name = os.path.abspath(os.path.dirname(__file__))
    name = os.path.join(name, 'out', datetime.now().strftime("%d-%m-%Y_%H-%M"))

    results_file_name = name + '_zm.xlsx'
    wb.save(results_file_name)
    return results_file_name


def parse_page(driver):
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//div[@class="PublicListStyles__PublicListContentContainer-sc-1q0smku-1 kDgLPV"]')))
    elements = driver.find_elements_by_xpath('//div[@class="PublicListStyles__PublicListContentContainer-sc-1q0smku-1 kDgLPV"]/div')
    for el in elements:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, './/a[contains(@class, "MainInfoNumberHeader")]/span')))
        number = el.find_element_by_xpath('.//a[contains(@class, "MainInfoNumberHeader")]/span')
        number = number.text
        name = el.find_element_by_xpath('.//a[contains(@class, "MainInfoNameHeader")]/span')
        name = name.text
        name_url = el.find_element_by_xpath('.//a[contains(@class, "MainInfoNameHeader")]')
        name_url = name_url.get_attribute('href')
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, './/a[contains(@class, "MainInfoCustomerHeader")]')))
        customer = el.find_element_by_xpath('.//a[contains(@class, "MainInfoCustomerHeader")]')
        customer = customer.text
        customer_url = el.find_element_by_xpath('.//a[contains(@class, "MainInfoCustomerHeader")]')
        customer_url = customer_url.get_attribute('href')
        price = el.find_element_by_xpath('.//div[contains(@class, "PriceInfoNumber")]')
        price = price.text.replace('&nbsp;', '')
        region = el.find_elements_by_xpath('.//div[contains(@class, "AdditionalInfoHeader")]/span')[1]
        region = region.text
        tdate_or_law = el.find_elements_by_xpath('.//div[contains(@class, "AdditionalInfoHeader")]/span')[2]
        tdate_or_law = tdate_or_law.text
        if 'ФЗ' in tdate_or_law:
            law = tdate_or_law
            tdate = el.find_elements_by_xpath('.//div[contains(@class, "AdditionalInfoHeader")]/span')[3]
            tdate = tdate.text
        else:
            law = ''
            tdate = tdate_or_law

        res[number] = {'name': name,
                        'name_url': name_url,
                        'customer': customer,
                        'customer_url': customer_url,
                        'price': price,
                        'region': region,
                        'law': law,
                        'tdate': tdate
                        }
        driver.execute_script('window.scrollBy(0, 300)', '')


def parsing(driver, keywords):
    for keyword in keywords:
        page_num = 1
        url = f'https://zakupki.mos.ru/purchase/list?page={page_num}&perPage=50&sortField=relevance&sortDesc=true&filter=%7B%22nameLike%22%3A%22{keyword}%22%2C%22auctionSpecificFilter%22%3A%7B%22stateIdIn%22%3A%5B19000002%5D%7D%2C%22needSpecificFilter%22%3A%7B%22stateIdIn%22%3A%5B20000002%5D%7D%2C%22tenderSpecificFilter%22%3A%7B%22stateIdIn%22%3A%5B5%5D%7D%7D&state=%7B%22currentTab%22%3A1%7D'
        driver.get(url)
        try:
            parse_page(driver=driver)
        except TimeoutException:
            continue
        pagination = driver.find_elements_by_xpath('.//div[contains(@class, "PublicListPaginatorStyles")]//a[@type="pageItem"]')
        if len(pagination) > 1 and page_num != len(pagination):
            page_num += 1
            url = f'https://zakupki.mos.ru/purchase/list?page={page_num}&perPage=50&sortField=relevance&sortDesc=true&filter=%7B%22nameLike%22%3A%22{keyword}%22%2C%22auctionSpecificFilter%22%3A%7B%22stateIdIn%22%3A%5B19000002%5D%7D%2C%22needSpecificFilter%22%3A%7B%22stateIdIn%22%3A%5B20000002%5D%7D%2C%22tenderSpecificFilter%22%3A%7B%22stateIdIn%22%3A%5B5%5D%7D%7D&state=%7B%22currentTab%22%3A1%7D'
            driver.get(url)
            try:
                parse_page(driver=driver)
            except TimeoutException:
                continue
            
        

res = dict()

driver = webdriver.Chrome()
driver.maximize_window()

parsing(driver, get_keywords(FILE_WITH_KEYWORDS))
print(save_results(res))
