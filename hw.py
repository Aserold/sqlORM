import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from hwmod import create_tables, Publisher, Book, Shop, Stock, Sale

user = 'postgres'
password = ''
host = 'localhost'
port = '5432'
db_name = 'netology_db'


DSN = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


publisher_identifier = input("Введите имя или идентификатор издателя: ")

try:
    id_ = int(publisher_identifier)
    publisher = session.query(Publisher).filter_by(id=id_).first()
except ValueError:
    publisher = session.query(Publisher).filter_by(name=publisher_identifier).first()



if not publisher:
    print("Издатель не найден.")
else:
    sales = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Stock, Stock.id_book == Book.id).join(Sale, Sale.id_stock == Stock.id).join(Shop, Shop.id == Stock.id_shop).filter(Book.publisher == publisher)


    for title, shop_name, price, date_sale in sales:
        print(f"Название книги: {title} | Магазин: {shop_name} | Стоимость: {price} | Дата покупки: {date_sale}")
    


session.close()
