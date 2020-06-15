import click
import requests
from bs4 import BeautifulSoup

def slugify(string):
    return string.lower().replace(' ', '-')

def convert_international(price: str) -> int:
    return int(price.replace('.', ''))

@click.command()
@click.option('-u', '--get-url', 'get_url', flag_value=True, default=False)
@click.option('-l', '--get-list', 'get_list', flag_value=True, default=False)
@click.option('-a', '--get-average', 'get_average', flag_value=True, default=False)
@click.option('-p', '--prices-number', 'prices_number', type=int, default=40)
@click.argument('string_search', type=str)
def main(string_search, get_url, get_list, prices_number, get_average):
    url = 'https://listado.mercadolibre.com.ar/'
    search = slugify(string_search)

    complete_url = url + search # + '_OrderId_PRICE*DESC'

    # glenlivet-founder-reserve
    response = requests.get(complete_url)

    parsed = BeautifulSoup(response.text, 'html.parser')

    price_tags = parsed.findAll('span', attrs={ 'class' : 'price__fraction' })

    # Getting raw prices (int values)
    prices = [ convert_international(price.getText(strip=True, )) for price in price_tags ]
    prices.sort()

    max_prices = len(prices)

    if prices_number > max_prices:
        raise click.ClickException('Exceeded the max number of prices (50). ')

    prices = prices[:prices_number]

    average = 0

    for value in prices:
        average += value

    average //= len(prices)

    minimum = prices[0]
    maximum = prices[-1]

    print(f'Max price: {maximum}')
    print(f'Min price: {minimum}')

    if get_url:
        print(complete_url)

    if get_list:
        print(prices)

    if get_average:
        print(f'Average: {average}')

if __name__ == '__main__':
    main()
