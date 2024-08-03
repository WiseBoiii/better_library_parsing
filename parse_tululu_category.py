import requests
from bs4 import BeautifulSoup
import urllib
import urllib3
from core_functions import parse_book_page, download_image, download_txt
import json
import time
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    url_pattern = 'https://tululu.org/l55/'
    book_url_pattern = 'https://tululu.org/'
    downloading_url = 'https://tululu.org/txt.php'
    archive_fantastic_books = []
    fantastic_parser = argparse.ArgumentParser(
        description='Это программа является парсером бесплатной онлайн-библиотеки Tululu'
    )
    fantastic_parser.add_argument('--start_page', help='С какой страницы каталога мы начинаем парсинг',
                                  type=int, default=1)
    fantastic_parser.add_argument('--end_page', help='По какую страницу каталога идёт парсинг', type=int,
                                  default=10)
    fantastic_parser.add_argument('--skip_imgs', help='Параметр, отвечающий за парсинг обложек',
                                  action='store_true')
    fantastic_parser.add_argument('--skip_txt',
                                  help='Параметр, отвечающий за парсинг текста самих книг', action='store_true')
    fantastic_parser.add_argument('--dest_folder',
                                  help='Параметр, отвечающий за выбор директории',
                                  type=str, default='parsed_result/')
    fantastic_args = fantastic_parser.parse_args()
    for page_number in range(fantastic_args.start_page, fantastic_args.end_page):
        url = f'{url_pattern}{page_number}'
        try:
            page_response = requests.get(url)
            page_response.raise_for_status()
            soup = BeautifulSoup(page_response.text, 'lxml')
            fantastic_books = soup.select('.d_book')
            for fantastic_book in fantastic_books:
                fantastic_book_url = fantastic_book.select_one('a')['href']
                book_id = int(fantastic_book_url.replace('/', '').lstrip('b'))
                params = {
                    'id': book_id
                }
                fantastic_book_link = urllib.parse.urljoin(url_pattern, fantastic_book_url)
                print(fantastic_book_link)
                fantastic_book_response = requests.get(fantastic_book_link)
                fantastic_book_response.raise_for_status()
                parsed_fantastic_book = parse_book_page(fantastic_book_link, fantastic_book_response)
                if not fantastic_args.skip_imgs:
                    download_image(parsed_fantastic_book['image'], fantastic_args.dest_folder)
                if not fantastic_args.skip_txt:
                    downloaded_fantastic_book_response = requests.get(downloading_url, params=params)
                    downloaded_fantastic_book_response.raise_for_status()
                    download_txt(downloaded_fantastic_book_response, parsed_fantastic_book['title'],
                                 fantastic_args.dest_folder)
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
                archive_fantastic_books.append(extended_parsed_fantastic_book)
        except requests.exceptions.HTTPError:
            print('Такой книги не существует')
        except requests.ConnectionError:
            print('Проблемы с соединением. Идет переподключение...')
            time.sleep(5)

    all_about_fantastic_books = json.dumps(archive_fantastic_books, ensure_ascii=False).encode('utf-8')
    with open(f'{fantastic_args.dest_folder}/all_about_fantastic_books.json', 'wb') as fantastic_book_file:
        fantastic_book_file.write(all_about_fantastic_books)


if __name__ == '__main__':
    main()

