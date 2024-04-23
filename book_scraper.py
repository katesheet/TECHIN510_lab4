
import os
from db import Database
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()


def get_data(db:Database):
    page_num = 1
    stop = False
    rating_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5}
    while not stop:
        URL= f'https://books.toscrape.com/catalogue/page-{page_num}.html'
        page_num += 1
        res = requests.get(URL)
        if res.status_code != 200:
            stop = True
            return
        soup = BeautifulSoup(res.text, 'html.parser')
        book_list = soup.select('article.product_pod')
        for book in book_list:
            rating = rating_dict[book.select('p')[0]['class'][-1].lower()]
            stock = book.select('p.instock.availability')[0].text.strip()
            title = book.select('a')[1]['title']
            price = book.select('p.price_color')[0].text[2:]
            print(title, price, rating, stock)
            d = {}
            d['title'] = title
            d['price'] = price
            d['rating'] = rating
            d['stock'] = stock
            db.insert_book(d)

with Database(os.getenv('DATABASE_URL')) as db:
    db.truncate_table()
    db.create_table()
    get_data(db)
    