from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
import random, time


def get_keywords(filename):
    keywords = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            keywords.append(line.strip())
        return keywords

driver = webdriver.Chrome()
url = 'https://agregatoreat.ru/purchases/new'
FILE_WITH_REGIONS = 'D:\\USERDATA\\Documents\\4git\\parsers\\tenders\\keywords\\bereza_regions.txt'

driver.maximize_window()
driver.get(url)

btn_all_filters = driver.find_element_by_xpath('//button[@data-v-7755f139][2]')
btn_all_filters.click()

WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//label[contains(text(), "Субъект РФ")]/following-sibling::div')))
regions = get_keywords(FILE_WITH_REGIONS)
# print(regions)
for region in regions:
    regions_dropdown = driver.find_element_by_xpath('//label[contains(text(), "Субъект РФ")]/following-sibling::div')
    regions_dropdown_arrow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//label[contains(text(), "Субъект РФ")]/following-sibling::div/div[1]')))

    # print(regions_dropdown.get_attribute('class'))
    regions_dropdown.send_keys(region)
    time.sleep(random.randint(1, 3))
    
    options_elements = driver.find_elements_by_xpath('//label[contains(text(), "Субъект РФ")]/following-sibling::div/div[3]/ul/li')[:-2]
    for el in options_elements:
        el.click()
    # driver.implicitly_wait(random.randint(1, 3))


# print(options)

# element.is_displayed() # check displayed status of html element
# element.is_enabled() # check enabled status of html element
# element.is_selected() # check select status of html element

try:
    pass
except expression as identifier:
    pass