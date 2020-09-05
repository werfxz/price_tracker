import sqlite3
import os

class Database:

    def __init__(self):
        #connect db if it exist 
        if os.path.isfile('products.db'):
            self.conn = sqlite3.connect('products.db')
        #if db doesn't exist then first create db then tables
        else:
            self.conn = sqlite3.connect('products.db')
            self.create_tables()

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

        self.conn.commit()
        self.conn.close()
    
    