from random import randint
from time import sleep

from scrape import Scraper
from products import products
from mail import send_mail, create_mail_body

def main():

    sc = Scraper()
    discount_amount = 20
    while True:
        product_list = sc.scrape_product_links(products)
        #iterate over product
        for product in product_list:
            #print average price of product
            print("Average price of", product.name + ":", product.average_price())

            #iterate over sellers
            for seller in product.prices():
                #compare prices of sellers with average price
                #if price of seller is lower than %discount_amount of the product send e-mail
                discounted_price = (product.average_price() - (product.average_price() * discount_amount / 100))
                if product.prices()[seller] < discounted_price:
                    print(seller, "has a discount")
                    discount_link = product.links()[seller]
                    #ürünün diğer tüm linklerini birleştirdik mailde göndereceğiz kontrol etmek için
                    product_links = "\n\n".join(list(product.links().keys()))
                    
                    send_mail(create_mail_body(product.name, discount_link, product_links))
            print("**************************************")

        #wait 10 - 100 seconds randomly 
        sleep(randint(10,100))


if __name__ == "__main__":
    main()