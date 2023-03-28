import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    headers = {
    'Authorization': f'Bearer {token}'
    }
    payload = {'long_url': url}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(token, url):
    headers = {
    'Authorization': f'Bearer {token}'
    }
    url_components = urlparse(url)
    correct_url = f'{url_components.netloc}{url_components.path}'
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{correct_url}/clicks/summary', headers=headers) 
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, url):
    headers = {
    'Authorization': f'Bearer {token}'
    }
    url_components = urlparse(url)
    correct_url = f'{url_components.netloc}{url_components.path}'
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{correct_url}', headers=headers)
    return response.ok


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('url', help='Insert bitly link to show clicks on it or insert URL to get bitlink') 
    return parser


if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    parser = create_parser()
    url = parser.parse_args().url
    try:
        if is_bitlink(bitly_token, url):
            clicks = count_clicks(bitly_token, url)
            print('clicks:', clicks)
        else:
            bitlink = shorten_link(bitly_token, url)
            print('bitlink:', bitlink)
    except requests.exceptions.HTTPError:
        print('Incorrect url')
        