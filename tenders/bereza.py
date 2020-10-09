from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from openpyxl import Workbook
import random, os, logging, time
from datetime import datetime
import yagmail
from config import from_email, password, to_emails, cc, bcc


FILE_WITH_KEYWORDS = 'D:\\USERDATA\\Documents\\4git\\parsers\\tenders\\keywords\\bz_keywords.txt'
FILE_WITH_REGIONS = 'D:\\USERDATA\\Documents\\4git\\parsers\\tenders\\keywords\\bz_regions.txt'
BASE_URL = 'https://agregatoreat.ru/purchases/new'


def set_logger():
    root_logger = logging.getLogger('bz')
    handler = logging.FileHandler('logs\\reports_bz.log', 'a', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)


def get_keywords(filename):
    keywords = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            keywords.append(line.strip())
        return keywords

# random.shuffle(keywords)

def parse_page(keyword, driver):
    searchbox = driver.find_element_by_xpath('//div[@class="filter-rs"]/input')
    searchbox.send_keys(keyword)

    searchBtn = driver.find_element_by_xpath('//button[@class="pt7 pb7 no-outline button-full block brdr-none align-center lh20 bg-cl-th-accent bg-cl-th-button-primary ripple fs14 cl-white relative mb11"]')
    searchBtn.click()

    delay = random.randint(6, 15)
    root_logger = logging.getLogger('bz')
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="container"]//div[@class="row"]//div[contains(@class, "purchase")]')))
        # EC.element_to_be_clickable()
        # print('\t row - ok', end='')
        elements = driver.find_elements_by_xpath('//div[@class="purchase flex between-xs wrap m0 mb10 brdr-1 brdr-cl-gray3"]')
        # print('\t elements - ok', end='')
        for el in elements:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, './/div[@class="weight-500 mb5 lh25 fs14 td-underline"]')))
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, './/div[@id="timer"]')))
            try:
                number = el.find_element_by_xpath('.//div[@class="weight-500 mb5 lh25 fs14 td-underline"]')
                number = number.text
            except StaleElementReferenceException:
                number = '#'
            name = el.find_element_by_xpath('.//div[@class="cl-black fs12 weight-500 lh20 td-underline wwrap-bw"]')
            name = name.text
            timer = el.find_element_by_xpath('.//div[@id="timer"]')
            timer = (timer.text).replace('\n', '')
            customer = el.find_element_by_xpath('.//div[@class="cl-black fs12 weight-500 lh20 td-underline"]')
            customer = customer.text
            price = el.find_element_by_xpath('.//div[@class="cl-green weight-400 fs10"]/span')
            price = price.text
            info = el.find_element_by_xpath('.//a[@class="brdr-l-1 cl-green brdr-cl-gray3 px15 py5 flex wrap no-underline"]')
            info = info.get_attribute('href')
            if number in res:
                res[number]['timer']  = timer
            res[number] = {'name': name,
                           'timer': timer,
                           'customer': customer,
                           'price': price,
                           'info': info}
            
        root_logger.info(f'parsing OK with keyword: {keyword}')
        searchbox.clear()
    except TimeoutException:
        root_logger.warning(f'timeout with keyword: {keyword}')
        searchbox.clear()

def save_results(res):
    wb = Workbook()
    ws = wb.active
    headers = ['Номер','Наименование', 'Время до окончания подачи предложений', 'Заказчик', 'Стартовая цена', 'Информация о закупке']
    ws.append(headers)
    for tender_number, tender_info in res.items():
        ws.append([tender_number, tender_info['name'], tender_info['timer'], tender_info['customer'], tender_info['price'], tender_info['info']])

    name = os.path.abspath(os.path.dirname(__file__))
    name = os.path.join(name, 'out', datetime.now().strftime("%d-%m-%Y_%H-%M"))
    results_file_name = name + '.xlsx'
    wb.save(results_file_name)
    root_logger = logging.getLogger('bz')
    root_logger.info(f'File {results_file_name} was successfully saved')
    return results_file_name
        

def parsing(keywords):
    btn_all_filters = driver.find_element_by_xpath('//button[@data-v-7755f139][2]')
    btn_all_filters.click()

    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//label[contains(text(), "Субъект РФ")]/following-sibling::div')))
    regions = get_keywords(FILE_WITH_REGIONS)
    # print(regions)
    for index, region in enumerate(regions):
        regions_dropdown = driver.find_element_by_xpath('//label[contains(text(), "Субъект РФ")]/following-sibling::div')
        regions_dropdown_arrow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//label[contains(text(), "Субъект РФ")]/following-sibling::div/div[1]')))

        # print(regions_dropdown.get_attribute('class'))
        regions_dropdown.send_keys(region)
        time.sleep(random.randint(2, 3))

        if index%4 == 0:
            driver.execute_script('window.scrollBy(0, 20)', '')
        
        options_elements = driver.find_elements_by_xpath('//label[contains(text(), "Субъект РФ")]/following-sibling::div/div[3]/ul/li')[:-2]
        for el in options_elements:
            try:
                el.click()
            except ElementClickInterceptedException:
                driver.execute_script('window.scrollBy(0, 20)', '')
                el.click()

    for keyword in keywords:
        parse_page(keyword=keyword, driver=driver)
        pagination = driver.find_elements_by_xpath('//div[@class="flex middle-xs center-xs align-center fs13 lh35 cl-black weight-700"]/div')
        if len(pagination) > 1:
            counter = 1
            while counter < len(pagination):
                new_url = baseUrl + '/page/' + str(counter+1)
                driver.get(new_url)
                parse_page(keyword=keyword, driver=driver)
                counter += 1
    root_logger = logging.getLogger('bz')
    root_logger.info(f'Parsed ' + str(len(res)) + ' tenders')


def sending_email(filename):
    body = "Below you find file with actual tenders from Berezka platform"
    contents = [
        body,
        filename
    ]

    yagmail.register(from_email, password)
    yag = yagmail.SMTP(from_email)
    yag.send(
        to=to_emails,
        subject="Berezka Tenders",
        cc=cc,
        bcc=bcc,
        contents=contents,
        # attachments=filename,
    )
    root_logger = logging.getLogger('bz')
    root_logger.info(f'File {filename} was successfully sended')


############################################################
res = dict()

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(BASE_URL)

set_logger()

parsing(get_keywords(FILE_WITH_KEYWORDS))

if len(res)>= 1:
    sending_email(save_results(res))
else:
    root_logger = logging.getLogger('bz')
    root_logger.info('There is NO tenders')
root_logger.info('='*36)


driver.quit()