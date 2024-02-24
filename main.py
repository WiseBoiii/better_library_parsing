import requests
from bs4 import BeautifulSoup
import urllib
import os
from pathvalidate import sanitize_filename
from pathvalidate import sanitize_filepath
from pathlib import Path
import urllib3
import argparse


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_txt(downloaded_book_response, title, folder='books/'):
    folder = sanitize_filepath(folder)
    created_folder = Path(folder).mkdir(parents=True, exist_ok=True)
    file_name = sanitize_filename(title) + '.txt'
    filepath = os.path.join(folder, file_name)
    with open(filepath, "w") as my_file:
        my_file.write(downloaded_book_response.text)

    return filepath


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_image(image_url, folder='previews/'):
    folder = sanitize_filepath(folder)
    picture_name = image_url.split('/')[-1]
    created_folder = Path(folder).mkdir(parents=True, exist_ok=True)
    file_name = sanitize_filename(picture_name)
    response = requests.get(image_url)
    filepath = os.path.join(folder, file_name)
    with open(filepath, "wb") as my_file:
        my_file.write(response.content)


def parse_book_page(page_response):
    parsed_book = BeautifulSoup(page_response.text, 'lxml')
    title_tag = parsed_book.find(id='content').find('h1')
    title_and_author = title_tag.text
    title_and_author = title_and_author.split('::')
    title = title_and_author[0].rstrip()
    picture = parsed_book.find('div', class_='bookimage').find('img')['src']
    image_url = urllib.parse.urljoin(url_pattern, picture)
    comment_section_tag = parsed_book.find(id='content').find_all('div', class_='texts')
    comments = []
    for comment in comment_section_tag:
        comment = comment.text.split(')')[-1]
        comments.append(comment)
    genres_tag = parsed_book.find(id='content').find('span', class_='d_book').find_all('a')
    genres = []
    for genre in genres_tag:
        genre = genre.text
        genres.append(genre)
    book_page = {
        'title': title,
        'image': image_url,
        'comments': comments,
        'genres': genres
    }
    return book_page


url_pattern = 'https://tululu.org/'
download_url = 'https://tululu.org/txt.php'
parser = argparse.ArgumentParser(
    description='Это программа является парсером бесплатной онлайн-библиотеки Tululu'
)
parser.add_argument('--start_id', help='С какого id книги мы начинаем парсинг', type=int, default=1)
parser.add_argument('--end_id', help='С какого id книги мы начинаем парсинг', type=int, default=20)
args = parser.parse_args()

for book_id in range(args.start_id, args.end_id):
    url = f"{url_pattern}b{book_id}/"
    params = {
        'id': book_id
    }
    try:
        page_response = requests.get(url)
        page_response.raise_for_status()
        check_for_redirect(page_response)
        downloaded_book_response = requests.get(download_url, params=params)
        downloaded_book_response.raise_for_status()
        check_for_redirect(downloaded_book_response)
        book_page = parse_book_page(page_response)
        download_txt(downloaded_book_response, book_page['title'])
        download_image(book_page['image'])
        print(book_page)
    except requests.exceptions.HTTPError:
        print('Такой книги не существует')