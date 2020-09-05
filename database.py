import os
from datetime import datetime
import sqlite3

class Database:

    def __init__(self):
        self.seller_ids = [(1, 'hepsiburada'),
                           (2, 'trendyol'),
                           (3, 'amazon'),
                           (4, 'vatan'),
                           (5, 'teknosa'),
                           (6, 'incehesap'),
                           (7, 'itopya')]

        #connect db if it exist 
        if os.path.isfile('products.db'):
            self.conn = sqlite3.connect('products.db')
        #if db doesn't exist first create db then tables
        else:
            #crete db
            self.conn = sqlite3.connect('products.db')
            #create tables
            self.create_tables()
            #inser seller ids to database
            self.inser_sellers()

    def create_tables(self):
        """
        This functions creates tables db created for the first time
        """

        c = self.conn.cursor()

        #Product look-up table
        c.execute('''CREATE TABLE products
             (product_id integer, product_name text)''')

        #seller look-up table
        c.execute('''CREATE TABLE sellers
             (seller_id integer, seller_name text)''')

        #Price of the product table
        c.execute('''CREATE TABLE products_prices
             (date text, product_id integer, seller_id integer, price real)''')
    
        c.executemany('INSERT INTO sellers VALUES (?,?)', self.seller_ids)

        self.conn.commit()

    def inser_sellers(self):
        """
        This functions inserts sellers id at the db creation
        """
        c = self.conn.cursor()

        c.executemany('INSERT INTO sellers VALUES (?,?)', self.seller_ids)

        self.conn.commit()

    def find_seller_id(self, seller_name):
        """
        This function finds the id of the seller from seller_ids list
        """
        for seller in self.seller_ids:
            if seller[1] == seller_name:
                return seller[0]

    def find_product_id(self, product_name):
        """
        This function finds the id of the product from database
        If no product found then new id will be created
        """
        
        c = self.conn.cursor()

        c.execute('SELECT DISTINCT PRODUCT_ID FROM PRODUCTS WHERE PRODUCT_NAME=?', (product_name,))
        product_id = c.fetchone()
        
        #if product found from products table
        if product_id is not None:
            return product_id[0]
        #if product cannot found from product table
        else:
            #create new product id by adding +1 to max product_id
            c.execute('SELECT MAX(PRODUCT_ID) FROM PRODUCTS')
            max_product_id = c.fetchone()[0] #c.fetchone() returns tuple like (None,)

            #if there is no product in the table this is the first product
            if max_product_id is None:
                new_product_id = 1
            else:
                new_product_id = max_product_id + 1
            #insert new id with product name to products table
            c.execute('INSERT INTO PRODUCTS VALUES (?,?)', (new_product_id, product_name))
            self.conn.commit()

            return new_product_id
        

    def insert_price(self, product):
        """
        This functions inserts prices of the product scraped from different sellers
        """
        now = datetime.now()
        # dd.mm.YY H:M:S
        date_time = now.strftime("%d.%m.%Y %H:%M:%S")

        c = self.conn.cursor()

        for seller in product.prices():
            seller_id = self.find_seller_id(seller)
            price = product.prices()[seller]
            product_id = self.find_product_id(product.name)
            c.execute('INSERT INTO PRODUCTS_PRICES VALUES (?,?,?,?)', (date_time, product_id, seller_id, price))

        self.conn.commit()
        #self.conn.close()