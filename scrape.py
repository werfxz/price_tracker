import re
import requests
import random
from bs4 import BeautifulSoup
from products import Product

class Scraper():

    proxy_url = 'https://free-proxy-list.net/'
    header_file = 'header_list.txt' 

    def __init__(self):
        self.header_list = self.get_headers()
        self.proxies = self.get_proxies()

    #creating random headers ve proxies
    #https://github.com/taspinar/twitterscraper/blob/0e5e269ee17e868a002b1266a0f1cd2c0de53360/twitterscraper/query.py#L45

    def get_headers(self):

        with open(self.header_file, 'r') as reader:
            # Read & print the entire file
            return reader.read().splitlines()

    def get_random_header(self, header_list):

        header = {'user-agent': random.choice(header_list), 
                  'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'accept-encoding': 'gzip, deflate, br'}
                  
        return header

    def get_proxies(self):
        response = requests.get(self.proxy_url)
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table',id='proxylisttable')
        list_tr = table.find_all('tr')
        list_td = [elem.find_all('td') for elem in list_tr]
        list_td = list(filter(None, list_td))
        list_ip = [elem[0].text for elem in list_td]
        list_ports = [elem[1].text for elem in list_td]
        list_proxies = [':'.join(elem) for elem in list(zip(list_ip, list_ports))]
        return list_proxies 

    def get_random_proxy(self, proxies):

        return random.choice(proxies)

    def get_request(self, url, timeout):
        """
        This function sends get request and return bs4 soup object
        """
        response = requests.get(url, headers=self.get_random_header(self.header_list), 
                                    proxies={"http": self.get_random_proxy(self.proxies)}, timeout=timeout)

        if response.status_code == 404:
            raise Exception("404 Status code")
        
        soup = BeautifulSoup(response.content, 'html5lib') 

        return soup


    def extract_price(self, price_string):
        """
        This function takes messy price string and convert it to integer
        It cuts the decimal point there is no rounding
        """
        #first remove decimal point from price then remove non numeric chars
        extracted_price = re.sub("[^0-9]", "", price_string.split(',')[0])
        return int(extracted_price)

    def scrape_hepsi(self, url, timeout=60):
        """
        This function takes hepsiburada product url and returns price of product
        """
        soup = self.get_request(url, timeout)
        
        content = soup.find_all("span", attrs={"itemprop": "price"})
        price = content[0]['content']

        return round(float(price))

    def scrape_trendyol(self, url, timeout=60):
        """
        This function takes trendyol product url and returns price of product
        """
        soup = self.get_request(url, timeout)
        
        #if there is no basket discount
        if len(soup.find_all(
                    "div", attrs={"class": "pr-cn"})[0].select(
                    'span[class="prc-slg"]')) == 1:
            content = soup.find_all(
                        "div",attrs={"class": "pr-cn"})[0].select(
                        'span[class="prc-slg"]')
        #if there is a basket discount
        elif len(soup.find_all(
                    "div", attrs={"class": "pr-cn"})[0].find_all(
                    "span", attrs={"class": "prc-dsc"})) == 1:
            content = soup.find_all(
                        "div", attrs={"class": "pr-cn"})[0].find_all(
                        "span", attrs={"class": "prc-dsc"})
        else:
            print("Can't find price of the Trendyol Product")
            return 0

        return self.extract_price(content[0].get_text())

    def scrape_amazon(self, url, timeout=60):
        """
        This function takes amazon product url and returns price of product
        """
        soup = self.get_request(url, timeout)

        #if product has discount
        if len(soup.find_all("span", attrs={"id": "priceblock_dealprice"})) == 1:
            content = soup.find_all("span", attrs={"id": "priceblock_dealprice"})
        #if product has no discount
        elif len(soup.find_all("span", attrs={"id": "priceblock_ourprice"})) == 1:
            content = soup.find_all("span", attrs={"id": "priceblock_ourprice"})
        elif len(soup.find_all("span", attrs={"id": "priceblock_saleprice"})) == 1:
            content = soup.find_all("span", attrs={"id": "priceblock_saleprice"})
        else:
            print("Can't find price of the Amazon Product")
            return 0

        #first remove decimal point from price then remove non numeric chars
        return self.extract_price(content[0].get_text())
        
    def scrape_vatan(self, url, timeout=60):
        """
        This function takes vatan product url and returns price of product
        """
        soup = self.get_request(url, timeout)

        content = soup.find_all(
                    "div", attrs= {"class": "product-list__content"})[0].find_all(
                    "span", attrs={"class": "product-list__price"})
        
        #first remove decimal point from price then remove non numeric chars
        return self.extract_price(content[0].get_text())

    def scrape_teknosa(self, url, timeout=60):
        """
        This function takes teknosa product url and returns price of product
        """
        soup = self.get_request(url, timeout)
        
        #if product has no discount
        if len(soup.find_all(
                    "div", attrs={"class": "product-detail-text"})[0].find_all(
                    "div", attrs={"class": "default-price"})) == 1:
            content = soup.find_all(
                        "div", attrs={"class": "product-detail-text"})[0].find_all(
                        "div", attrs={"class": "default-price"})
        #if product has discount
        elif len(soup.find_all(
                    "div", attrs={"class": "product-detail-text"})[0].find_all(
                    "div", attrs={"class": "new-price"})) == 1:
            content = soup.find_all(
                        "div", attrs={"class": "product-detail-text"})[0].find_all(
                        "div", attrs={"class": "new-price"})
        else:
            print("Can't find price of the Teknosa Product")
            return 0

        return self.extract_price(content[0].get_text())

    def scrape_incehesap(self ,url, timeout=60):
        """
        This function takes incehesap product url and returns price of product
        """
        soup = self.get_request(url, timeout)
        
        if len(soup.select(
                    'div[class="container first"]')[0].find_all(
                    "span", attrs={"class": "cur"})) == 1:
            content = soup.select(
                            'div[class="container first"]')[0].find_all(
                            "span", attrs={"class": "cur"})
        elif len(soup.select(
                    'div[class="container first"]')[0].find_all(
                    "div", attrs={"class": "arti-indirimli-fiyat cur"})) == 1:
            content = soup.select(
                        'div[class="container first"]')[0].find_all(
                        "div", attrs={"class": "arti-indirimli-fiyat cur"})
        else:
            print("Can't find price of the İnce hesap Product")
            return 0

        return self.extract_price(content[0].get_text())

    def scrape_itopya(self, url, timeout=60):
        """
        This function takes itopya product url and returns price of product
        """
        soup = self.get_request(url, timeout)

        content = soup.find_all(
                    "div", attrs= {"class": "product-info"})[0].select(
                    'div[class="new text-right"]')

        #Remove decimal price because it is specified with "." same as thousand seperation
        #decimal point is written seperateley like "<sup>.65</sup>"
        return self.extract_price(
            content[0].get_text().replace(
                                    content[0].find("sup").get_text(), ""))
        


    def extract_domainname(self, url):
        """
        This function takes full url of website and returns domain name
        www.amazon.com.tr --> returns "amazon"
        """
        domain = re.findall(r'www\.(.+?)\.com',url)[0]

        return domain

    def scrape_product_links(self, products):
        """
        This function takes product dictionary and scrape the links and returns both links and prices
        Store the links and prices as a product object
        """

        products_list = []

        for product_name in products:
            product = Product(product_name)
            print("Product name:", product.name)
            for product_link in products[product_name]:
                try:
                    if self.extract_domainname(product_link) == "hepsiburada":
                        price_hepsi = int(self.scrape_hepsi(product_link))
                        product.hepsi_price = price_hepsi
                        product.hepsi_link = product_link
                        print(self.extract_domainname(product_link), price_hepsi)
                    if self.extract_domainname(product_link) == "trendyol":
                        price_trendyol = int(self.scrape_trendyol(product_link))
                        product.trendyol_price = price_trendyol
                        product.trendyol_link = product_link
                        print(self.extract_domainname(product_link), price_trendyol)
                    if self.extract_domainname(product_link) == "amazon":
                        price_amazon = int(self.scrape_amazon(product_link))
                        product.amazon_price= price_amazon
                        product.amazon_link = product_link
                        print(self.extract_domainname(product_link), price_amazon)
                    if self.extract_domainname(product_link) == "vatanbilgisayar":
                        price_vatan = int(self.scrape_vatan(product_link))
                        product.vatan_price = price_vatan
                        product.vatan_link = product_link
                        print(self.extract_domainname(product_link), price_vatan)
                    if self.extract_domainname(product_link) == "teknosa":
                        price_teknosa = int(self.scrape_teknosa(product_link))
                        product.teknosa_price = price_teknosa
                        product.teknosa_link = product_link
                        print(self.extract_domainname(product_link), price_teknosa)
                    if self.extract_domainname(product_link) == "incehesap":
                        price_incehesap = int(self.scrape_incehesap(product_link))
                        product.incehesap_price = price_incehesap
                        product.incehesap_link = product_link
                        print(self.extract_domainname(product_link), price_incehesap)
                    if self.extract_domainname(product_link) == "itopya":
                        price_itopya = int(self.scrape_itopya(product_link))
                        product.itopya_price = price_itopya
                        product.itopya_link = product_link 
                        print(self.extract_domainname(product_link), price_itopya)
                except Exception as e:
                    print("Cant scrape the price from:", self.extract_domainname(product_link))
                    print(e)

            products_list.append(product)   

        return products_list


