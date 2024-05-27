import json
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager

BASEURL = 'https://megamarket.ru'


def get_pages_html(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    items = []
    try:
        for page in range(1, 4):
            print(f'[+] Страница {page}')
            driver.get(url=url.replace(f'page_num', f'page-{page}'))
            WebDriverWait(driver, 60).until(
                ec.presence_of_element_located((By.TAG_NAME, 'html'))
            )
            if not get_items(driver.page_source, items):
                break
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def get_items(html, items):
    pass


def save_to_excel(data, filename):
    pass


def start():
    target = input('Введите название товара: ')
    min_price = input('Минимальная цена (enter, чтобы пропустить): ')
    min_price = min_price if min_price != '' else '0'
    max_price = input('Максимальная цена (enter, чтобы пропустить): ')
    max_price = max_price if max_price != '' else '9999999'
    target_url = f"{BASEURL}/catalog/page_num/?q={target}"
    if all([max_price, min_price, max_price.isdigit(), min_price.isdigit()]):
        filter = {
            '88C83F68482F447C9F4E401955196697': {'min': int(min_price), 'max': int(max_price)},  # фильтр по цене
            '4CB2C27EAAFC4EB39378C4B7487E6C9E': ['1']  # наличие товара
        }
        json_data = json.dumps(filter)
        url_encoded_data = parse.quote(json_data)
        target_url += '#?filters=' + url_encoded_data
    items = get_pages_html(target_url)
    save_to_excel(items, target)


if __name__ == '__main__':
    start()
