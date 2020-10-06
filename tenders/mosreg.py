from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from openpyxl import Workbook
import random, os, logging, time
from datetime import datetime
import yagmail
from config import from_email, password, to_emails


FILE_WITH_KEYWORDS = 'D:\\USERDATA\\Documents\\4git\\parsers\\tenders\\keywords\\test.txt'
BASE_URL = 'https://market.mosreg.ru/Trade'


def get_keywords(filename):
    keywords = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            keywords.append(line.strip())
        return keywords


def parse_page(keyword, driver):
    print(keyword)
    searchbox = driver.find_elements_by_xpath('//input[@data-bind="value: pageVM.filterTradeName"]')[0]
    searchbox.send_keys(keyword)

    searchBtn = driver.find_element_by_xpath('//button[@data-bind="click: pageVM.searchData"]')
    searchBtn.click()

    # driver.implicitly_wait(5)
    time.sleep(5)
    delay = random.randint(6, 15)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@data-bind="foreach: pageVM.listTradesTest"]/div')))
    #     # print('\t row - ok', end='')

        elements = driver.find_elements_by_xpath('//div[@data-bind="foreach: pageVM.listTradesTest"]/div')
        # print('\t elements - ok', end='')
        for el in elements:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, './/div[@class="blockResult__rightContent-suggestion"]')))
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, './/a[@class="blockResult__leftContent-linkString"]')))
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, './/span[@data-bind="text: Id"]')))
                number = el.find_element_by_xpath('.//span[@data-bind="text: Id"]')
                number = number.text
                name = el.find_element_by_xpath('.//a[@class="blockResult__leftContent-linkString"]')
                url = name.get_attribute('href')
                name = name.text
                start = el.find_element_by_xpath('.//span[contains(@data-bind, "dateString: PublicationDate, datePattern:")]')
                start = start.text
                end = el.find_element_by_xpath('.//span[@data-bind="text: FillingApplicationEndDate"]')
                end = end.text
                price = el.find_element_by_xpath('.//p[contains(@data-bind, "number: InitialPrice")]')
                price = price.text
                customer_card = el.find_element_by_xpath('.//a[contains(@data-bind, "Customer/ViewCustomerInfoById")]')
                customer_card = customer_card.get_attribute('href')
            except StaleElementReferenceException:
                print('Stale Exception!!!')
            
            if number in res:
                res[number]['start']  = start
                res[number]['end']  = end
            res[number] = {'name': name,
                           'url': url,
                           'start': start,
                           'end': end,
                           'price': price,
                           'customer_card': customer_card }
            
        logging.info(f'parsing OK with keyword: {keyword}')
        searchbox.clear()
    except TimeoutException:
        logging.warning(f'timeout with keyword: {keyword}')
        # print('something goes wrong')
        searchbox.clear()


def parsing(keywords):
    for keyword in keywords:
        parse_page(keyword=keyword, driver=driver)
        # pagination = driver.find_elements_by_xpath('//div[@class="flex middle-xs center-xs align-center fs13 lh35 cl-black weight-700"]/div')
        # if len(pagination) > 1:
        #     counter = 1
        #     while counter < len(pagination):
        #         new_url = baseUrl + '/page/' + str(counter+1)
        #         driver.get(new_url)
        #         parse_page(keyword=keyword, driver=driver)
        #         counter += 1
    logging.info(f'Parsed ' + str(len(res)))
    logging.info('='*36)


def save_results(res):
    wb = Workbook()
    ws = wb.active
    headers = ['Номер','Наименование', 'Ссылка', 'Начало приема заявок', 'Окончание приема заявок', 'Карточка Заказчика', 'Цена']
    ws.append(headers)
    for tender_number, tender_info in res.items():
        ws.append([tender_number, tender_info['name'], tender_info['url'], tender_info['start'], tender_info['end'], tender_info['price'], tender_info['customer_card']])

    name = os.path.abspath(os.path.dirname(__file__))
    name = os.path.join(name, 'out', datetime.now().strftime("%d-%m-%Y_%H-%M"))
    results_file_name = name + '_mosreg.xlsx'
    wb.save(results_file_name)
    return results_file_name



res = dict()

driver = webdriver.Chrome()
driver.get(BASE_URL)

root_logger= logging.getLogger()
handler = logging.FileHandler('reports_mosreg.log', 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
handler.setFormatter(formatter)
root_logger.addHandler(handler)

keywords = get_keywords(FILE_WITH_KEYWORDS)
parsing(keywords)

logging.info(f'Parsed ' + str(len(res)))
logging.info('='*36)

save_results(res)
# sending_email(save_results(res))
    
driver.quit()