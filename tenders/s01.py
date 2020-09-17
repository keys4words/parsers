from selenium import webdriver

# PATH = "C:\chromedriver\chromedriver.exe"
# driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome()
driver.get('https://yandex.ru')
print(driver.title)
driver.quit()
