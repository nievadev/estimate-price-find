import click
import requests
from bs4 import BeautifulSoup

def slugify(string):
    result = string.lower().replace(' ', '-')

    return result

def convert_international(price: str) -> int:
    price = int(price.replace('.', ''))

    return price

@click.command()
@click.option('-u', '--get-url', 'get_url', flag_value=True, default=False)
@click.option('-p', '--prices-number', 'prices_number', type=int, default=10)
@click.argument('string_search', type=str)
def main(string_search, get_url, prices_number):
    url = 'https://listado.mercadolibre.com.ar/'
    search = slugify(string_search)

    complete_url = url + search

    # glenlivet-founder-reserve
    response = requests.get(complete_url)

    parsed = BeautifulSoup(response.text, 'html.parser')

    price_tags = parsed.findAll('span', attrs={ 'class' : 'price__fraction' })

    # Getting raw prices (int values)
    prices = [ convert_international(price.getText(strip=True, )) for price in price_tags ][:prices_number]
    prices.sort(reverse=True)

    minimum = prices[-1]
    maximum = prices[0]

    print(f'Max price: {maximum}\nMin price: {minimum}')

    if get_url:
        print(complete_url)

if __name__ == '__main__':
    main()
