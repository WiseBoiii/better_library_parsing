import requests
from bs4 import BeautifulSoup
import urllib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fantastic_url_pattern = 'https://tululu.org/l55/'
book_url_pattern = 'https://tululu.org/'


def parse_book_category(url_pattern, book_url_pattern):
    for page in range(10):
        url = f'{url_pattern}{page}'
        page_response = requests.get(url)
        page_response.raise_for_status()
        soup = BeautifulSoup(page_response.text, 'lxml')
        all_fantastic_book_ids = soup.find_all(class_='d_book')
        for fantastic_book in all_fantastic_book_ids:
            fantastic_book_id = fantastic_book.find('a')['href']
            fantastic_book_link = urllib.parse.urljoin(book_url_pattern, fantastic_book_id)
            print(fantastic_book_link)


parse_book_category(fantastic_url_pattern, book_url_pattern)
