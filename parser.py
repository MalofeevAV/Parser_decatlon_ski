import requests
from bs4 import BeautifulSoup
import csv

CSV = 'products_list.csv'
HOST = 'https://www.decathlon.ru'
URL = 'https://www.decathlon.ru/C-261832-lyzhi'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}
PARAMS = ('',
          'N-791487-для-кого~для-мужчин',
          'N-791487-для-кого~для-женщин',
          'N-791487-для-кого~для-мальчиков',
          'N-791487-для-кого~для-девочек'
          )


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='new-product-thumbnail desktop')
    products = []
    for item in items:
        products.append(
            {
                # 'title': item.find('li', class_='new-product-thumbnail desktop').get_text(),
                # 'link_to_product': item.find('li', class_='new-product-thumbnail desktop').find('a').get('href')
                'title': item['data-product-name'],
                'price': float(item['data-product-price']),
                'product_img' : item['data-product-imgurl'],
                'link_to_product': HOST + item.a['href']
            }
        )
    return products


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта', 'Цена', 'Изображение продукта', 'Ссылка на продукт'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['product_img'], item['link_to_product']])


def parser(params):
    html = get_html(URL, params)
    if html.status_code == 200:
        products_list = [product for product in get_content(html.text)]
        save_doc(products_list, CSV)
    else:
        print('Error')


def welcome():
    message = """
    Выберите категорию
    все категории - 0
    мужчины - 1
    женщины - 2
    мальчики - 3
    девочки - 4
    Категория: 
    """
    params_index = int(input(message))
    if 0 <= params_index <= 4:
        parser(PARAMS[params_index])
    else:
        print("Не верно указано число")


welcome()
