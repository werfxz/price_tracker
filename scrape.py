import requests
import random
from bs4 import BeautifulSoup 

#random header ve proxy oluşturma
#https://github.com/taspinar/twitterscraper/blob/0e5e269ee17e868a002b1266a0f1cd2c0de53360/twitterscraper/query.py#L45
HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

HEADER = {'User-Agent': random.choice(HEADERS_LIST), 'X-Requested-With': 'XMLHttpRequest'}

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
    response = requests.get(url, headers=HEADER, proxies={"http": get_random_proxy(PROXIES)}, timeout=timeout)
    soup = BeautifulSoup(response.content, 'html5lib') 

    return soup

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

    try:
        content = soup.find_all("span", attrs={"class": "prc-slg"})
    except IndexError:
        content = soup.find_all("span", attrs={"class": "prc-dsc"})

    #TODO Virgül ile split yapınce küsüratsız fiyatlarda ikiye ayıramıyorsun
    return content[0].get_text().split(',')[0].replace('.','')

def scrape_amazon(url, timeout=60):
    """
    This function takes amazon product url and returns price of product
    """
    soup = get_request(url, timeout)

    #if product has discount
    try:
        content = soup.find_all("span", attrs={"id": "priceblock_dealprice"})
        return content[0].get_text()
    #if product has no discount
    except IndexError:
        content = soup.find_all("span", attrs={"id": "priceblock_ourprice"})
        return content[0].get_text()
    
def scrape_vatan(url, timeout=60):
    """
    This function takes vatan product url and returns price of product
    """
    soup = get_request(url, timeout)

    content = soup.find_all("span", attrs={"class": "product-list__price"})
    
    return content[0].get_text()