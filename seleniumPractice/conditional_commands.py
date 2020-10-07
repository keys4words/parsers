from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random


driver = webdriver.Chrome()
url = 'https://agregatoreat.ru/purchases/new'

driver.maximize_window()
driver.get(url)

btn_all_filters = driver.find_element_by_xpath('//button[@data-v-7755f139][2]')
btn_all_filters.click()

regions = ['москва', 'московская']
for region in regions:
    regions_dropdown = driver.find_element_by_xpath('//label[contains(text(), "Субъект РФ")]/following-sibling::div')
    regions_dropdown.click()
    regions_dropdown.send_keys(region)
    
    options_elements = driver.find_elements_by_xpath('//label[contains(text(), "Субъект РФ")]/following-sibling::div/div[3]/ul/li')[:-2]
    for el in options_elements:
        el.click()
    driver.implicitly_wait(random.randint(1, 3))
    
# print(options)

# element.is_displayed() # check displayed status of html element
# element.is_enabled() # check enabled status of html element
# element.is_selected() # check select status of html element

