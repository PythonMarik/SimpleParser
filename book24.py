import requests
from bs4 import BeautifulSoup

class Parser:

    """Метод-конструктор, принемающий ссылку на страницу и домен страницы"""
    def __init__(self, url, domen):
        self.url = url
        self.domen = domen

        self.req = requests.get(url)
        self.soup = BeautifulSoup(self.req.text, 'html.parser')

    """Метод, собирающий название книги, и имя автора"""
    def parse_book(self):

        book_names = []
        tag_book = self.soup.find_all('a', class_='product-card__name')
        for book in tag_book:
            book_names.append(book.get('title'))

        author_names = []
        tag_author = self.soup.find_all('div', class_='author-list product-card__authors-holder')
        for a in tag_author:
            author = a.find(class_='author-list__item')
            author_names.append(author.text)

        # Запишем данные в словарь
        info = {}
        for i in range(0, len(book_names)):
            info[book_names[i]] = author_names[i]

        return info

    """Метод, собирающий цену книги"""
    def get_price(self):

        prices = []
        prices_tag = self.soup.find_all('div', class_='product-list__item')
        for i in prices_tag:
            price = i.find('article')
            prices.append(f"{price.get('data-b24-price')} Rub")

        return prices

    """Метод, который собирает ссылку на обложку книги"""
    def get_book_img(self):
        images = self.soup.find_all('img', class_='product-card__image')
        images_list = []  # Итоговый лист ссылок на изображения
        for image in images:
            if not 'https:' in image.get('data-src'):
                images_list.append(f"https:{image.get('data-src')}")
            else:
                images_list.append(image.get('data-src'))

        return images_list

parser = Parser(url='https://book24.ru/novie-knigi/', domen='https://book24.ru/')
print(parser.parse_book())
print(parser.get_price())
print(parser.get_book_img())






