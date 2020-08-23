import re
import requests
import random
from bs4 import BeautifulSoup 

#creating random headers ve proxies
#https://github.com/taspinar/twitterscraper/blob/0e5e269ee17e868a002b1266a0f1cd2c0de53360/twitterscraper/query.py#L45
HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

def get_random_header():

    header = {'User-Agent': random.choice(HEADERS_LIST), 'X-Requested-With': 'XMLHttpRequest'}
    return header

PROXY_URL = 'https://free-proxy-list.net/'

def get_proxies():
    response = requests.get(PROXY_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table',id='proxylisttable')
    list_tr = table.find_all('tr')
    list_td = [elem.find_all('td') for elem in list_tr]
    list_td = list(filter(None, list_td))
    list_ip = [elem[0].text for elem in list_td]
    list_ports = [elem[1].text for elem in list_td]
    list_proxies = [':'.join(elem) for elem in list(zip(list_ip, list_ports))]
    return list_proxies 

PROXIES = get_proxies()

def get_random_proxy(proxies):

    return random.choice(proxies)

def get_request(url, timeout):
    """
    This function sends get request and return bs4 soup object
    """
    response = requests.get(url, headers=get_random_header(), 
                                 proxies={"http": get_random_proxy(PROXIES)}, timeout=timeout)
    soup = BeautifulSoup(response.content, 'html5lib') 

    return soup


def extract_price(price_string):
    """
    This function takes messy price string and convert it to integer
    It cuts the decimal point there is no rounding
    """
    #first remove decimal point from price then remove non numeric chars
    extracted_price = re.sub("[^0-9]", "", price_string.split(',')[0])
    return int(extracted_price)

def scrape_hepsi(url, timeout=60):
    """
    This function takes hepsiburada product url and returns price of product
    """
    soup = get_request(url, timeout)
    
    content = soup.find_all("span", attrs={"itemprop": "price"})
    price = content[0]['content']

    return round(float(price))

def scrape_trendyol(url, timeout=60):
    """
    This function takes trendyol product url and returns price of product
    """
    soup = get_request(url, timeout)
    
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

    return extract_price(content[0].get_text())

def scrape_amazon(url, timeout=60):
    """
    This function takes amazon product url and returns price of product
    """
    soup = get_request(url, timeout)

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
    return extract_price(content[0].get_text())
    
def scrape_vatan(url, timeout=60):
    """
    This function takes vatan product url and returns price of product
    """
    soup = get_request(url, timeout)

    content = soup.find_all(
                   "div", attrs= {"class": "product-list__content"})[0].find_all(
                   "span", attrs={"class": "product-list__price"})
    
    #first remove decimal point from price then remove non numeric chars
    return extract_price(content[0].get_text())

def scrape_teknosa(url, timeout=60):
    """
    This function takes teknosa product url and returns price of product
    """
    soup = get_request(url, timeout)
    
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

    return extract_price(content[0].get_text())

def scrape_incehesap(url, timeout=60):
    """
    This function takes incehesap product url and returns price of product
    """
    soup = get_request(url, timeout)
    
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

    return extract_price(content[0].get_text())

def scrape_itopya(url, timeout=60):
    """
    This function takes itopya product url and returns price of product
    """
    soup = get_request(url, timeout)

    content = soup.find_all(
                   "div", attrs= {"class": "product-info"})[0].select(
                   'div[class="new text-right"]')

    #Remove decimal price because it is specified with "." same as thousand seperation
    #decimal point is written seperateley like "<sup>.65</sup>"
    return extract_price(
           content[0].get_text().replace(
                                content[0].find("sup").get_text(), ""))
    


def extract_domainname(url):
    """
    This function takes full url of website and returns domain name
    www.amazon.com.tr --> returns "amazon"
    """
    domain = re.findall(r'www\.(.+?)\.com',url)[0]

    return domain

def extract_product_links(products):
    """
    This function takes product dictionary and scrape the links
    Store the prices as a nested dict
    """
    products_price_dict = {}
    for product_name in products:
        price_dict = {}
        print("Product name:", product_name)
        for product_link in products[product_name]:
            try:
                if extract_domainname(product_link) == "hepsiburada":
                    print(extract_domainname(product_link), scrape_hepsi(product_link))
                    price_dict["hepsiburada"] = int(scrape_hepsi(product_link))
                if extract_domainname(product_link) == "trendyol":
                    print(extract_domainname(product_link), scrape_trendyol(product_link))
                    price_dict["trendyol"] = int(scrape_trendyol(product_link))
                if extract_domainname(product_link) == "amazon":
                    print(extract_domainname(product_link), scrape_amazon(product_link))
                    price_dict["amazon"] = int(scrape_amazon(product_link))
                if extract_domainname(product_link) == "vatanbilgisayar":
                    print(extract_domainname(product_link), scrape_vatan(product_link))
                    price_dict["vatanbilgisayar"] = int(scrape_vatan(product_link))
                if extract_domainname(product_link) == "teknosa":
                    print(extract_domainname(product_link), scrape_teknosa(product_link))
                    price_dict["teknosa"] = int(scrape_teknosa(product_link))
                if extract_domainname(product_link) == "incehesap":
                    print(extract_domainname(product_link), scrape_incehesap(product_link))
                    price_dict["incehesap"] = int(scrape_incehesap(product_link))
                if extract_domainname(product_link) == "itopya":
                    print(extract_domainname(product_link), scrape_itopya(product_link))
                    price_dict["itopya"] = int(scrape_itopya(product_link))
            except Exception as e:
                print("Cant scrape the price from:", extract_domainname(product_link))
                print(e)

        products_price_dict[product_name] = price_dict

    return products_price_dict


