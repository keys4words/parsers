from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from openpyxl import Workbook
import random, os, logging
from datetime import datetime
import yagmail
from config import from_email, password, to_emails


FILE_WITH_KEYWORDS = 'D:\\USERDATA\\Documents\\4git\\parsers\\tenders\\keywords\\marketMosreg.txt'
BASE_URL = 'https://market.mosreg.ru/Trade'


def get_keywords(filename):
    keywords = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            keywords.append(line.strip())
        return keywords


def parse_page(keyword, driver):
    searchbox = driver.find_elements_by_xpath('//input[@data-bind="value: pageVM.filterTradeName"]')[0]
    searchbox.send_keys(keyword)

    searchBtn = driver.find_element_by_xpath('//button[@data-bind="click: pageVM.searchData"]')
    searchBtn.click()

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
            except StaleElementReferenceException:
                number = '#'
            
            name = el.find_element_by_xpath('.//a[@class="blockResult__leftContent-linkString"]')
            # name = name.get_attribute('href')
            # name = '#'
    #         timer = el.find_element_by_xpath('.//div[@id="timer"]')
    #         timer = (timer.text).replace('\n', '')
    #         customer = el.find_element_by_xpath('.//div[@class="cl-black fs12 weight-500 lh20 td-underline"]')
    #         customer = customer.text
    #         price = el.find_element_by_xpath('.//div[@class="cl-green weight-400 fs10"]/span')
    #         price = price.text
    #         info = el.find_element_by_xpath('.//a[@class="brdr-l-1 cl-green brdr-cl-gray3 px15 py5 flex wrap no-underline"]')
    #         info = info.get_attribute('href')
    #         if number in res:
    #             res[number]['timer']  = timer
            res[number] = {'name': name}
    #                        'timer': timer,
    #                        'customer': customer,
    #                        'price': price,
    #                        'info': info}
            
    #     logging.info(f'parsing OK with keyword: {keyword}')
        searchbox.clear()
    except TimeoutException:
    #     logging.warning(f'timeout with keyword: {keyword}')
        print('something goes wrong')
    #     searchbox.clear()


res = dict()

driver = webdriver.Chrome()
driver.get(BASE_URL)

partial = get_keywords(FILE_WITH_KEYWORDS)
parse_page(partial[14], driver)
print(res)
    
driver.quit()