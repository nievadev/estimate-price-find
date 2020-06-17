import click
import requests
import re
from bs4 import BeautifulSoup

def slugify(string):
    return string.lower().replace(' ', '-')

def convert_international(price: str) -> int:
    return int(price.replace('.', ''))

@click.command()
@click.option('-u', '--get-url', 'get_url', flag_value=True, default=False)
@click.option('-l', '--get-list', 'get_list', flag_value=True, default=False)
@click.option('-a', '--get-avg', 'get_avg', flag_value=True, default=False)
@click.argument('string_search', type=str)
def main(string_search, get_avg, get_url, get_list):
    url = 'https://listado.mercadolibre.com.ar/'
    search = slugify(string_search)

    complete_url = url + search # + '_OrderId_PRICE*DESC'

    response = requests.get(complete_url)

    parsed = BeautifulSoup(response.text, 'html.parser')

    keywords = string_search.replace('\'', ' ')
    keywords = string_search.replace('`', ' ')
    keywords = keywords.split(' ')

    keywords = [ word.lower() for word in keywords ]

    def has_keywords(post):
        attrs = ' '.join(post.attrs.get('class', [])).strip()

        if attrs != 'rowItem item highlighted item--stack new' or post.name != 'div':
            return False

        found_dict = { key : False for key in keywords }

        text = post.find('h2', recursive=True).getText()

        text = text.replace('\'', ' ')

        words = text.split(' ')

        words = [ word.lower() for word in words if len(word) > 0 ]

        for keyword in keywords:
            for word in words:
                if keyword in word:
                    found_dict[keyword] = True

        for key, value in found_dict.items():
            if not value:
                return False

        return True

    posts = parsed.find_all(has_keywords)

    list_posts_names = [ post.find('h2').getText().strip() for post in posts ]

    prices = list()

    dict_info = dict()

    for post in posts:
        title_post = post.find('h2').getText().strip()

        price = post.find('span', attrs={ 'class' : 'price__fraction' })

        price = convert_international(price.getText())

        prices.append(price)

        dict_info[title_post] = price

    sorted_dict_info = sorted(dict_info.items(), key=lambda x: x[1])

    prices.sort()

    if get_url:
        print('-' * 25)
        print(complete_url)

    if get_list:
        print('-' * 25)
        print(list_posts_names)

    print('-' * 25)
    print(f'Got {len(prices)} results. ')

    if len(prices) > 2:
        maximum = sorted_dict_info[-1]
        b_maximum = sorted_dict_info[-2]

        minimum = sorted_dict_info[0]
        b_minimum = sorted_dict_info[1]

        average = 0
        
        for price in prices:
            average += price

        average //= len(prices)

        average_calculated = (maximum[1] - average) * 0.5 + average

        print(f'Max price -> {maximum[0]}: {maximum[1]}')
        print(f'2nd max price -> {b_maximum[0]}: {b_maximum[1]}')

        print(f'2nd min price -> {b_minimum[0]}: {b_minimum[1]}')
        print(f'Min price -> {minimum[0]}: {minimum[1]}')

        # print(f'50% more than average: {average_calculated}')

        if get_avg:
            print(f'Average price: {average}')

    else:
        print(sorted_dict_info)

    print('-' * 25)

if __name__ == '__main__':
    main()
