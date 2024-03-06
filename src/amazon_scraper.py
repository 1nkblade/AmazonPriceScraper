import requests
from bs4 import BeautifulSoup
from datetime import datetime

product_list = ['B07STGHZK8', 'B07J2WBKXF', 'B01N0Z1YKE']
base_url = 'https://www.amazon.it/'
url = 'https://www.amazon.it/dp/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}

# Make a request to the product URL
base_response = requests.get(base_url, headers=headers)
cookies = base_response.cookies


def scrape_amazon_product():
    print(datetime.now())

    for prod in product_list:
        product_response = requests.get(url + prod, headers=headers, cookies=cookies)
        soup = BeautifulSoup(product_response.text, 'html.parser')

        product_name = soup.find(id="productTitle").text.strip()
        product_price = soup.find('span', {'class': 'a-offscreen'}).text.strip()

        price_float = float(product_price.replace('€', '').replace(',', '.'))


        print(f"Name: {product_name}")
        print(f"ID: {prod}" + f" - Price: {product_price}")
