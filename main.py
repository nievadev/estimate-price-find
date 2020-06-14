import click
import requests
from bs4 import BeautifulSoup

def convert_international(price: str) -> int:
    price = int(price.replace('.', ''))

    return price

response = requests.get('https://listado.mercadolibre.com.ar/glenlivet-founder-reserve')

parsed = BeautifulSoup(response.text, 'html.parser')

price_tags = parsed.findAll('span', attrs={ 'class' : 'price__fraction' })

# Getting raw prices (int values)
prices = [ convert_international(price.getText(strip=True, )) for price in price_tags ]
prices.sort(reverse=True)

print(prices)
