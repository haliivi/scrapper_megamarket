import json
from urllib import parse

BASEURL = 'https://megamarket.ru'


def get_pages_html(url):
    pass


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
