from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome()
# https://www.seleniumeasy.com/
# https://petstore.swagger.io/
# http://demo.automationtesting.in/
# https://demoqa.com/
url = 'https://www.seleniumeasy.com/test/'
driver.get(url)
# print(driver.title)
# print(driver.current_url)

driver.find_element_by_xpath('//a[@id="btn_basic_example"]').click()
time.sleep(5)
driver.get('https://yandex.ru')
print(driver.current_url)
driver.back()
print(driver.current_url)
driver.forward()
print(driver.current_url)
time.sleep(5)
# driver.close()
driver.quit()