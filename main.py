from random import randint
from time import sleep

from scrape import  extract_product_links
from products import products
from mail import send_mail, create_mail_body


if __name__ == "__main__":

    while True:
        price_dict = extract_product_links(products)
        #iterate over product
        for product_name in price_dict:
            prices = list(price_dict[product_name].values())
            #calculate average price of product
            average_price = sum(prices)/len(prices)
            print("Average price of", product_name + ":", average_price)
            #iterate over sellers
            for seller in price_dict[product_name]:
                #compare prices of sellers with average price
                #if price of seller is lower than %20 of the product send e-mail 
                if price_dict[product_name][seller] < (average_price - (average_price*20/100)):
                    print(seller, "has a discount")
                    #TODO seller yerine URL getirmemiz lazım direk mailden ürün linkine tıklayabilirim
                    send_mail(create_mail_body(product_name, seller))
            print("**************************************")

        #wait 10 - 100 seconds randomly 
        sleep(randint(10,100))