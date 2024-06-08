import requests
from bs4 import BeautifulSoup
import urllib
import urllib3
from main import parse_book_page, download_image, download_txt
import json
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fantastic_url_pattern = 'https://tululu.org/l55/'
book_url_pattern = 'https://tululu.org/'
downloading_url = 'https://tululu.org/txt.php'


def parse_fantastic_category(url_pattern, book_url_pattern):
    fantastic_books = []
    fantastic_parser = argparse.ArgumentParser(
        description='Это программа является парсером бесплатной онлайн-библиотеки Tululu'
    )
    fantastic_parser.add_argument('--start_page', help='С какой страницы каталога мы начинаем парсинг', type=int, default=1)
    fantastic_parser.add_argument('--end_page', help='До какой страницы каталога идёт парсинг', type=int, default=10)
    fantastic_args = fantastic_parser.parse_args()
    for page in range(fantastic_args.start_page, fantastic_args.end_page):
        url = f'{url_pattern}{page}'
        page_response = requests.get(url)
        page_response.raise_for_status()
        soup = BeautifulSoup(page_response.text, 'lxml')
        all_fantastic_book_ids = soup.select('.d_book')
        for fantastic_book in all_fantastic_book_ids:
            fantastic_book_id = fantastic_book.select_one('a')['href']
            param_id = int(fantastic_book_id.replace('/', '').lstrip('b'))
            params = {
                'id': param_id
            }
            downloaded_fantastic_book_response = requests.get(downloading_url, params=params)
            downloaded_fantastic_book_response.raise_for_status()
            fantastic_book_link = urllib.parse.urljoin(book_url_pattern, fantastic_book_id)
            fantastic_book_response = requests.get(fantastic_book_link)
            fantastic_book_response.raise_for_status()
            parsed_fantastic_book = parse_book_page(fantastic_book_link, fantastic_book_response)
            download_image(parsed_fantastic_book['image'])
            download_txt(downloaded_fantastic_book_response, parsed_fantastic_book['title'])
            fantastic_book_img_src = f"previews/{parsed_fantastic_book['image'].split('/')[-1]}"
            fantastic_book_path = f"books/{parsed_fantastic_book['title']}.txt"
            extended_parsed_fantastic_book = {
                'title': parsed_fantastic_book['title'],
                'author': parsed_fantastic_book['author'],
                'img_src': fantastic_book_img_src,
                'book_path': fantastic_book_path,
                'comments': parsed_fantastic_book['comments'],
                'genres': parsed_fantastic_book['genres']
            }
            fantastic_books.append(extended_parsed_fantastic_book)
    all_about_fantastic_books = json.dumps(fantastic_books, ensure_ascii=False).encode('utf-8')
    with open('all_about_fantastic_books.json', 'wb') as fantastic_book_file:
        fantastic_book_file.write(all_about_fantastic_books)
    return all_about_fantastic_books


print(parse_fantastic_category(fantastic_url_pattern, book_url_pattern))

parser = argparse.ArgumentParser(
        description='Это программа является парсером бесплатной онлайн-библиотеки Tululu'
    )
parser.add_argument('--start_page', help='С какой страницы каталога мы начинаем парсинг', type=int, default=1)
parser.add_argument('--end_page', help='До какой страницы каталога идёт парсинг', type=int, default=20)
args = parser.parse_args()