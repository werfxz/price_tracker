from random import randint
from time import sleep

from src.scrape import Scraper
from src.mail import Mail
from src.database import Database
from src.products import products


def main():

    sc = Scraper()
    mail = Mail()
    discount_amount = 20
    while True:
        product_list = sc.scrape_product_links(products)
        #iterate over product
        for product in product_list:
            print("Average price of", product.name + ":", product.average_price())
            #initialize db, if initialized before it will connect to db
            #insert price of the product to database
            with Database('products.db') as db:
                db.insert_price(product)

            #iterate over sellers
            for seller in product.prices():
                #compare prices of sellers with average price
                #if price of seller is lower than %discount_amount of the product send e-mail
                discounted_price = (product.average_price() - (product.average_price() * discount_amount / 100))
                if product.prices()[seller] < discounted_price:
                    print(seller, "has a discount")
                    discount_link = product.links()[seller]
                    
                    mail.send_mail(mail.create_mail_body(product.name, discount_link, product.links()))
            
            print("**************************************")

        #wait 1 hour randomly 
        sleep(randint(3500,3600))


if __name__ == "__main__":
    main()