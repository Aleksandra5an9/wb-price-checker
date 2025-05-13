from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = 'https://www.wildberries.ru/catalog/260800583/detail.aspx'

# Настройки для headless-браузера
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.get(url)

# Ждём, чтобы страница успела прогрузиться
time.sleep(5)

# Ищем цену
try:
    price_element = driver.find_element('css selector', 'span.price-block__price')
    print('Цена с сайта:', price_element.text)
except:
    print('Не удалось найти цену.')

driver.quit()
