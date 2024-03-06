import requests
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time
import validators

base_url = 'https://www.amazon.it/'
url = 'https://www.amazon.it/dp/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}

# Make a request to the product URL
base_response = requests.get(base_url, headers=headers)
cookies = base_response.cookies


def is_valid_url(input_url):
    return validators.url(input_url)


def get_id():
    # Ask for user input
    user_url = input("Enter the URL: ")

    # Check if the entered URL is valid
    if is_valid_url(user_url):
        print(f"The entered URL '{user_url}' is valid.")

        # Extract the product ID
        start_index = user_url.find("dp/") + 3
        end_index = user_url.find("/", start_index)
        product_id = user_url[start_index:end_index]

        print(f"Product ID: {product_id}")
    else:
        print(f"The entered URL '{user_url}' is not valid.")

    return product_id


def scrape_amazon_product(prod=get_id()):
    try:
        print(datetime.now())

        product_response = requests.get(url + prod, headers=headers, cookies=cookies)
        soup = BeautifulSoup(product_response.text, 'html.parser')

        product_name = soup.find('span', id="productTitle").text.strip()
        product_price = soup.find('span', {'class': 'a-offscreen'}).text.strip()

        price_float = float(product_price.replace('€', '').replace(',', '.'))

        print(f"Name: {product_name}")
        print(f"ID: {prod}" + f" - Price: {product_price}")

    except Exception as e:
        print(f"An error occurred: {e}")


schedule.every(5).seconds.do(scrape_amazon_product)
while True:
    schedule.run_pending()
    time.sleep(1)
