from random import randint
from time import sleep

from scrape import Scraper
from products import products
from mail import Mail
from database import Database

def main():

    sc = Scraper()
    mail = Mail()
    db = Database()
    discount_amount = 20
    while True:
        product_list = sc.scrape_product_links(products)
        #iterate over product
        for product in product_list:
            #print average price of product
            print("Average price of", product.name + ":", product.average_price())
            #insert price of the product to database
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

        #wait 10 - 100 seconds randomly 
        sleep(randint(3500,3600))


if __name__ == "__main__":
    main()