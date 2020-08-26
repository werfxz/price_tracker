from random import randint
from time import sleep

from scrape import  extract_product_links
from products import products
from mail import send_mail, create_mail_body

def main():
    discount_amount = 20
    while True:
        price_dict, links_dict = extract_product_links(products)
        #iterate over product
        for product_name in price_dict:
            prices = list(price_dict[product_name].values())
            #calculate average price of product
            average_price = sum(prices)/len(prices)
            print("Average price of", product_name + ":", average_price)
            #iterate over sellers
            for seller in price_dict[product_name]:
                #compare prices of sellers with average price
                #if price of seller is lower than %discount_amount of the product send e-mail 
                if price_dict[product_name][seller] < (average_price - (average_price*discount_amount/100)):
                    print(seller, "has a discount")
                    discount_link = links_dict[product_name][seller]
                    #ürünün diğer tüm linklerini birleştirdik mailde göndereceğiz kontrol etmek için
                    product_links = "\n\n".join(list(links_dict[product_name].values()))
                    
                    send_mail(create_mail_body(product_name, discount_link, product_links))
            print("**************************************")

        #wait 10 - 100 seconds randomly 
        sleep(randint(10,100))


if __name__ == "__main__":
    main()