import json
import pandas as pd
from math import floor
from bs4 import BeautifulSoup
from urllib import parse
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager

BASEURL = 'https://megamarket.ru'


def get_pages_html(url, parsing_page=1):
    options = ChromeOptions()
    options.add_argument('--width=1200')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    items = []
    try:
        for page in range(1, parsing_page + 1):
            print(f'[+] Страница {page}')
            current_url_page = url.replace(f'page_num', f'page-{page}')
            driver.get(url=current_url_page)
            WebDriverWait(driver, 60).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'catalog-items-list'))
            )
            if not get_items(driver.page_source, items, current_url_page):
                break
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    return items


def get_items(html, items, current_url_page):
    soup = BeautifulSoup(html, 'html.parser')
    items_divs = soup.find('div', class_='catalog-items-list').find_all('div', recursive=False)
    if len(items_divs) == 0:
        return False
    for item in items_divs:
        link = BASEURL + a.get('href') if (a := item.find('a', class_='ddl_product_link')) else '-'
        item_price_result = item_price.find('span').get_text() if (
            item_price := item.find('div', class_='item-price')) else '-'
        item_title = item.find('div', class_='item-title').find('a').get_text().strip()
        item_bonus_amount = item_bonus.find('span', class_='bonus-amount').get_text() if (
            item_bonus := item.find('div', class_='item-bonus')) else '-'
        item_merchant_name = merchant_name.get_text().strip() if (
            merchant_name := item.find('span', class_='merchant-info__name')) else '-'
        price = int(item_price_result.replace(' ', '').replace(u'\xa0₽', ''))
        bonus = int(item_bonus_amount) if item_bonus_amount.isdigit() else 0
        bonus_percent = floor(bonus / price * 100)
        items.append({
            'Наименование': item_title,
            'Продавец': item_merchant_name,
            'Цена': price,
            'Сумма бонусов': bonus,
            'Процент бонуса': bonus_percent,
            'Ссылка на страницу с товарами': current_url_page,
            'Ссылка на товар': link,
        })
    return True


def save_to_excel(data: list, filename: str):
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(f'{filename}.xlsx')
    df.to_excel(writer, sheet_name='data', index=False)
    writer.close()


def start():
    target = input('Введите название товара: ')
    parsing_page = int(parsing_page_input) if (
        (parsing_page_input := input('Введите количество страниц для парсинга (enter, 1): ')).isdigit()) else 1
    min_price = input('Минимальная цена (enter, 0): ')
    min_price = min_price if min_price != '' else '0'
    max_price = input('Максимальная цена (enter, 9999999): ')
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
    items = get_pages_html(target_url, parsing_page)
    save_to_excel(items, target)


if __name__ == '__main__':
    start()
