from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from openpyxl import Workbook
import random

keywords = []
with open('keywords.txt', 'r', encoding='utf-8') as f:
    for line in f:
        keywords.append(line.strip())

# random.shuffle(keywords)

res = dict()
baseUrl = 'https://agregatoreat.ru/purchases/new'

driver = webdriver.Chrome()
driver.get(baseUrl)


def parse_page(keyword, driver):
    searchbox = driver.find_element_by_xpath('//div[@class="filter-rs"]/input')
    searchbox.send_keys(keyword)

    searchBtn = driver.find_element_by_xpath('//button[@class="pt7 pb7 no-outline button-full block brdr-none align-center lh20 bg-cl-th-accent bg-cl-th-button-primary ripple fs14 cl-white relative mb11"]')
    searchBtn.click()

    delay = random.randint(6, 15)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="container"]//div[@class="row"]//div[contains(@class, "purchase")]')))
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
            
        searchbox.clear()
    except TimeoutException:
        print(f'timeout with keyword: {keyword}')
        searchbox.clear()

def save_results(res):
    wb = Workbook()
    ws = wb.active
    headers = ['Номер','Наименование', 'Время до окончания подачи предложений', 'Заказчик', 'Стартовая цена', 'Информация о закупке']
    ws.append(headers)
    for tender_number, tender_info in res.items():
        ws.append([tender_number, tender_info['name'], tender_info['timer'], tender_info['customer'], tender_info['price'], tender_info['info']])

    wb.save('D:\\USERDATA\\Documents\\4git\\parsers\\data\\tenders.xlsx')



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
    
save_results(res)

driver.quit()
print('Parsed ' + str(len(res)))