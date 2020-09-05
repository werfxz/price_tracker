class Product:

    def __init__(self, name):
        self.name = name
        #self.prices = None
        #self.links = None

        self.hepsi_price = None
        self.trendyol_price = None
        self.amazon_price = None
        self.vatan_price = None
        self.teknosa_price = None
        self.incehesap_price = None
        self.itopya_price = None

        self.hepsi_link = None
        self.trendyol_link = None
        self.amazon_link = None
        self.vatan_link = None
        self.teknosa_link = None
        self.incehesap_link = None
        self.itopya_link = None
    
    def filter_nulls(self, some_list):
        #Filter Nulls from list
        filtered_list = [] 
        for val in some_list: 
            if val != None : 
                filtered_list.append(val) 

        return filtered_list

    def average_price(self):
        """
        This function returns average price of the product
        """

        price_list = [self.hepsi_price, self.trendyol_price,
                      self.amazon_price, self.vatan_price,
                      self.teknosa_price, self.incehesap_price,
                      self.itopya_price]

        #remove Null prices
        prices = self.filter_nulls(price_list)
        
        return sum(prices)/len(prices)

    def clean_nulls(self, d):
        """
        This function removes dictionary elements which has None value
        """
        return {k:v 
                for k, v in d.items() 
                if v is not None}

    def prices(self):
        """
        This function returns Seller:Price dictionary
        """

        prices = {"Hepsiburada": self.hepsi_price,
                  "Trendyol": self.trendyol_price,
                  "Amazon": self.amazon_price,
                  "Vatan Bilgisayar": self.vatan_price,
                  "Teknosa": self.teknosa_price,
                  "İnce Hesap": self.incehesap_price,
                  "İtopya": self.itopya_price}
        
        return self.clean_nulls(prices)

    def links(self):
        """
        This function returns Seller:Product url
        """

        links = {"Hepsiburada": self.hepsi_link,
                  "Trendyol": self.trendyol_link,
                  "Amazon": self.amazon_link,
                  "Vatan Bilgisayar": self.vatan_link,
                  "Teknosa": self.teknosa_link,
                  "İnce Hesap": self.incehesap_link,
                  "İtopya": self.itopya_link}
        
        return self.clean_nulls(links)



#links dictionary format {"product name": [links]}
products = {"Asus RTX 2080 Super": ["https://www.incehesap.com/asus-rog-strix-rtx2080s-a8g-gaming-ekran-karti-fiyati-43239/",
                                    "https://www.amazon.com.tr/GEFORCE-ROG-STRIX-RTX2080S-A8G-GAMING-256bit-1860MHz-1xTYPE-C/dp/B07VM9V59H/ref=sr_1_2?__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=ASUS+GEFORCE+ROG-STRIX-RTX2080S-A8G&qid=1598294342&s=computers&sr=1-2/",
                                    "https://www.hepsiburada.com/asus-geforce-rog-strix-rtx-2080s-gaming-advanced-edition-8gb-256bit-gddr6-dx12-pci-e-3-0-ekran-karti-rog-strix-rtx2080s-a8g-gaming-p-HBV00000M4L5E/",
                                    "https://www.itopya.com/asus-rog-strix-geforce-rtx-2080-super-advanced-edition-8gb-gddr6-256-bit-ekran-karti/",
                                    "https://www.vatanbilgisayar.com/asus-geforce-rog-strix-rtx2080s-gaming-8gb-gddr6-256bit-dx12-nvidia-ekran-karti.html/"]}




