import os
import time
import sqlite3

class Database:

    def __init__(self):
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
        self.seller_ids = [(1, 'hepsiburada'),
                           (2, 'trendyol'),
                           (3, 'amazon'),
                           (4, 'vatan'),
                           (5, 'teknosa'),
                           (6, 'incehesap'),
                           (7, 'itopya')]
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
        self.conn.close()

    def inser_sellers(self):
        """
        This functions inserts sellers id at the db creation
        """
        c = self.conn.cursor()

        c.executemany('INSERT INTO sellers VALUES (?,?)', self.seller_ids)

        self.conn.commit()
        self.conn.close()

    def insert_price(self, product):
        """
        This functions inserts prices of the product scraped from different sellers
        """
        c = self.conn.cursor()

        c.executemany('INSERT INTO product_prices VALUES (?,?,?,?)', ('date, product_id, seller_id, price'))

        self.conn.commit()
        self.conn.close()

        pass