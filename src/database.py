import os
from datetime import datetime
import sqlite3

class Database:

    def __init__(self, db_name):
        self.seller_ids = [(1, 'hepsiburada'),
                           (2, 'trendyol'),
                           (3, 'amazon'),
                           (4, 'vatan'),
                           (5, 'teknosa'),
                           (6, 'incehesap'),
                           (7, 'itopya')]
        
        self.is_db_exist = os.path.isfile(db_name)

        #connect db if it exist, if not empty db will be created
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

        #if db doesn't exist create tables
        if not self.is_db_exist:
            #create tables
            self.create_tables()
            #inser seller ids to database
            self.insert_sellers(self.seller_ids)
            print("Database Created")

    #db connection closing with context managers https://codereview.stackexchange.com/a/182706
    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def create_tables(self):
        """
        This functions creates tables db created for the first time
        """
        #Product look-up table
        self.cur.execute('''CREATE TABLE products(
            product_id integer PRIMARY KEY, 
            product_name text)
        ''')

        #seller look-up table
        self.cur.execute('''CREATE TABLE sellers(
            seller_id integer PRIMARY KEY,
            seller_name text)
        ''')

        #Price of the product table
        self.cur.execute('''CREATE TABLE products_prices(
            date_time text, 
            product_id integer, 
            seller_id integer, 
            price real)
        ''')
    
        self.conn.commit()

    def insert_sellers(self, seller_ids):
        """
        This functions inserts sellers id at the db creation
        """
        self.cur.executemany('INSERT INTO sellers VALUES (?,?)', seller_ids)

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
        self.cur.execute("""SELECT DISTINCT PRODUCT_ID 
                       FROM PRODUCTS 
                      WHERE PRODUCT_NAME = ? """, (product_name,))
        product_id = self.cur.fetchone()
        
        #if product found from products table
        if product_id is not None:
            return product_id[0]
        #if product cannot found from product table
        else:
            #create new product id by adding +1 to max product_id
            self.cur.execute('SELECT MAX(PRODUCT_ID) FROM PRODUCTS')
            max_product_id = self.cur.fetchone()[0] #self.cur.fetchone() returns tuple like (None,)

            #if there is no product in the table this is the first product
            if max_product_id is None:
                new_product_id = 1
            else:
                new_product_id = max_product_id + 1
            #insert new id with product name to products table
            self.cur.execute('INSERT INTO PRODUCTS VALUES (?,?)', (new_product_id, product_name))
            self.conn.commit()

            return new_product_id
        
    def insert_price(self, product):
        """
        This functions inserts prices of the product scraped from different sellers
        """
        now = datetime.now()
        # YYYY-MM-DD HH:MM
        date_time = now.strftime("%Y-%m-%d %H:%M")

        for seller in product.prices():
            seller_id = self.find_seller_id(seller)
            price = product.prices()[seller]
            product_id = self.find_product_id(product.name)
            self.cur.execute('INSERT INTO PRODUCTS_PRICES VALUES (?,?,?,?)', (date_time, product_id, seller_id, price))

        self.conn.commit()