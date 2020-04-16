import requests
import os
from dotenv import load_dotenv
import argparse

HOST = 'https://api-ssl.bitly.com'
API_VERSION = 'v4'


def get_request_url(method, version=API_VERSION):
    return f'{HOST}/{version}/{method}'


def shorten_link(url, token):
    headers = {
        'Authorization': 'Bearer ' + token
    }
    body = {
        'long_url': url,
        # 'title': ''
    }
    with requests.session() as session:
        request_url = get_request_url('bitlinks')
        response = session.post(request_url, headers=headers, json=body)
        response.raise_for_status()
        short_link = response.json()['link']

    return short_link


def count_clicks(bitlink, token):
    headers = {
        'Authorization': 'Bearer ' + token
    }
    params = {
        'unit': 'day',
        'units': -1
    }
    with requests.session() as session:
        request_url = get_request_url(f'bitlinks/{bitlink}/clicks')
        response = session.get(request_url, headers=headers, params=params)
        response.raise_for_status()
        clicks_array = response.json()['link_clicks']
        clicks_output = (f"{row['date'][:10]}: {row['clicks']}" for row in clicks_array if int(row['clicks']) != 0)

    return '\n'.join(clicks_output)


def main():
    parser = argparse.ArgumentParser(description='Получить сокращенную ссылку (bitlink) / '
                                                 'получить количество переходов по сокращенной ссылке')
    parser.add_argument('url', help='Ссылка')
    args = parser.parse_args()

    load_dotenv()

    bitly_token = os.getenv('BITLY_TOKEN')
    url = args.url

    try:
        if not url.startswith('bit.ly/'):
            print('Битлинк', shorten_link(url, bitly_token))
        else:
            print('Статистика переходов по ссылке:\n', count_clicks(url, bitly_token))
    except requests.exceptions.HTTPError as ex:
        print(ex, '\n')


if __name__ == '__main__':
    main()
