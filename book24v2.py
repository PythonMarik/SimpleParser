import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import json

@dataclass
class Product:
    title: str
    price: int
    brand: str
    id: str

def get_html(page):
    url = f"https://book24.ru/novie-knigi/page-{page}/"
    resp = httpx.get(url)

    return HTMLParser(resp.text)


def parse_products(html):
    content = html.css('div.product-list__item')

    results = []
    for item in content:
        new_item = Product(
            title=item.css_first('article').attrs['data-b24-name'],
            price=int(item.css_first('article').attrs['data-b24-price']),
            brand=item.css_first('article').attrs['data-b24-brand'],
            id=item.css_first('article').attrs['data-b24-id']
        )

        results.append(asdict(new_item))

    return results

def main():

    # Scraping from page 2 to page 20
    for x in range(2, 21):
        html = get_html(x)
        data = parse_products(html)
        json.dumps(data, indent=2)

        with open('data_book24.json', 'w', encoding='utf-8') as jsonFile:
            json.dump(data, jsonFile, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()




