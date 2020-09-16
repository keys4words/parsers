from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from openpyxl import Workbook


class Tender:
    def __init__(self, name, timer, customer, price, info):
        self.name = name
        self.timer = timer
        self.customer = customer
        self.price = price
        self.info = info


driver = webdriver.Chrome()
driver.get('https://agregatoreat.ru/purchases/new')
searchbox = driver.find_element_by_xpath('//div[@class="filter-rs"]/input')

keyword = 'огнетушител'
searchbox.send_keys(keyword)

searchBtn = driver.find_element_by_xpath('//button[@class="pt7 pb7 no-outline button-full block brdr-none align-center lh20 bg-cl-th-accent bg-cl-th-button-primary ripple fs14 cl-white relative mb11"]')
searchBtn.click()

delay = 3
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="container"]//div[@class="row"]//div[contains(@class, "purchase")]')))
    elements = driver.find_elements_by_xpath('//div[@class="purchase flex between-xs wrap m0 mb10 brdr-1 brdr-cl-gray3"]')
    # elements = elements[:2]
    res = []
    for el in elements:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, './/div[@id="timer"]')))
        timer = el.find_element_by_xpath('.//div[@id="timer"]')
        timer = (timer.text).replace('\n', '')
        name = el.find_element_by_xpath('.//div[@class="cl-black fs12 weight-500 lh20 td-underline wwrap-bw"]')
        name = name.text
        customer = el.find_element_by_xpath('.//div[@class="cl-black fs12 weight-500 lh20 td-underline"]')
        customer = customer.text
        price = el.find_element_by_xpath('.//div[@class="cl-green weight-400 fs10"]/span')
        price = price.text
        info = el.find_element_by_xpath('.//a[@class="brdr-l-1 cl-green brdr-cl-gray3 px15 py5 flex wrap no-underline"]')
        info = info.get_attribute('href')
        res.append(Tender(name, timer, customer, price, info))
except TimeoutException:
    print('Page was NOT loaded!')

wb = Workbook()
ws = wb.active
headers = ['Наименование', 'Время до окончания подачи предложений', 'Заказчик', 'Стартовая цена', 'Информация о закупке']
ws.append(headers)
for tender in res:
    ws.append([tender.name, tender.timer, tender.customer, tender.price, tender.info])

wb.save('D:\\USERDATA\\Documents\\4git\\parsers\\data\\tenders.xlsx')



