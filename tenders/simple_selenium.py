from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from openpyxl import Workbook
import random

'''keywords = ['АПС', 'вибрационный датчик', 'водопенное оборудование', 'воздушно пенный', 'воздушно эмульсионный', 'воздушно-пенный', 'воздушно-эмульсионный', 'генератор огнетушащего аэрозоля', 'генераторы пены', 'гидрант', 'гидротестер', 'дымоудаление', 'извещатель', 'микрокапсулирование', 'мотопомпа', 'ОВП', 'ОВЭ', 'огнетушитель', 'ОПС', 'охранно-пожарный', 'переговорные устройства', 'периметр', 'пирокорд', 'пиростикер', 'план эвакуации', 'пожарная безопасность', 'пожарная сигнализация', 'пожарная', 'пожарное оборудование', 'пожарно-охранный', 'пожаротушение', 'противодымный', 'противопожарный', 'рукав', 'самоспасатель', 'сигнализация охранная', 'сигнализация', 'систем безопасности', 'систем защиты', 'система оповещения', 'система пожарной безопасности', 'средство обнаружения', 'стволы', 'трибоэлектрический датчик', 'управление эвакуацией', 'шланг']'''

keywords = ['водопенное оборудование', 'АПС']
# random.shuffle(keywords)

res = dict()
baseUrl = 'https://agregatoreat.ru/purchases/new'

driver = webdriver.Chrome()
driver.get(baseUrl)


def check_pagination(driver):
    try:
        driver.find_elements_by_xpath('//div[@class="flex middle-xs center-xs align-center fs13 lh35 cl-black weight-700"]/div')
    except NoSuchElementException:
        return False
    return True


def parse_page(keyword, driver):
    searchbox = driver.find_element_by_xpath('//div[@class="filter-rs"]/input')
    searchbox.send_keys(keyword)

    searchBtn = driver.find_element_by_xpath('//button[@class="pt7 pb7 no-outline button-full block brdr-none align-center lh20 bg-cl-th-accent bg-cl-th-button-primary ripple fs14 cl-white relative mb11"]')
    searchBtn.click()

    delay = 3
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="container"]//div[@class="row"]//div[contains(@class, "purchase")]')))
        elements = driver.find_elements_by_xpath('//div[@class="purchase flex between-xs wrap m0 mb10 brdr-1 brdr-cl-gray3"]')
        # elements = elements[:2]
        for el in elements:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, './/div[@id="timer"]')))
            number = el.find_element_by_xpath('.//div[@class="weight-500 mb5 lh25 fs14 td-underline"]')
            number = number.text
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

def save_results():
    wb = Workbook()
    ws = wb.active
    headers = ['Наименование', 'Время до окончания подачи предложений', 'Заказчик', 'Стартовая цена', 'Информация о закупке']
    ws.append(headers)
    for tender in res:
        ws.append([tender.name, tender.timer, tender.customer, tender.price, tender.info])

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
    

driver.quit()
print(len(res))



