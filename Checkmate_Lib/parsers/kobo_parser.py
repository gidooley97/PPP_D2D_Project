from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from PIL import Image
from io import BytesIO
import urllib.request
from bookSite import BookSite
import mechanize
from bs4 import BeautifulSoup

############ KoboSite Class ################
"""parses the book data from kobo"""
class KoboSite(BookSite):
    
    def __init__(self):
        super().__init__()
        self.site_slug='KO'
        self.search_url="https://www.kobo.com/"
        self.url_to_book_detail ="https://www.kobo.com/us/en/ebook/"#set to ebook bcs D2D deals with ebooks mainly
        
    """
    returns the volume number of  the book.

    Args:
        root-- root of the tree.
    """
    def volume_parser(self, root):
        path = self.get_volume_path()
        series_element = ''
        volume = ''
        try:
            if root.xpath(path):
                #Seperate series number from series title
                series_split = series.split('#')
                if len(series_split) > 1:
                    volume = series_split[1]
        except:
            volume = None
        return volume
    """
    gets the isbn field of the book.

    this method overrides isbnParser in the base class
    params:
        root: root of the html etree
    return:
        isbn: isbn-13 of the book
    """

    def isbn_parser(self, root):
        path = self.get_isbn_path()
        try:
            isbn_elements = root.xpath(path)
            isbn=''
            for isbn_tmp in isbn_elements:
                if isbn_tmp.text.strip()=='ISBN:':
                    isbn =isbn_tmp.xpath('./span')[0].text
        except:
            isbn = None#Fail
        return isbn
    #override
    def desc_parser(self, root):
        path = self.get_desc_path()
        try:
            desc_element_list = root.xpath(path)[0]
            xmlstr = etree.tostring(desc_element_list, encoding='utf8', method='xml')  
            desc = BeautifulSoup(xmlstr,features="lxml") 
        except:
            desc = None    
        return desc.get_text()
    #override
    def format_parser(self, root):
        path = self.get_format_path()
        try: 
            format_element = root.xpath(path)[0]
            format = format_element.text.strip().split(' ')[0]
        except:
            format = None
        return format

    #override
    def image_url_parser(self, root):
        path = self.get_img_url_path()
        try:
            imgUrl_element = root.xpath(path)[0] 
            imgUrl = "http:" + imgUrl_element
        except:
            imgUrl = None
        return imgUrl

  
    """
    str -> SiteBookData

    Given a direct link to a book page at a site,
    parse it and return the SiteBookData of the info.
    args:
        url: direct url to a book.
    return:
        book_site_data: a SiteBookData object
    """
    def get_book_data_from_site(self,url):
        return super().get_book_data_from_site(url)

    
    """
    returns the xpath taht helps to get urls.

    params:
        None
    return:
        xpath: xpath

    """
    def get_search_urls_after_search_path(self):
        return  ".//p[@class='title product-field']/a/@href"


    """
    Given a book_id, return the direct url for the book.

    To be overriden by all sites.
    params:
        book_id: the book unique identifier.
    return:
        url:direct url to the book. 
    """
    def convert_book_id_to_url(self,book_id):
        return self.url_to_book_detail+book_id

    def get_title_path(self):
        return ".//h1/span[@class='title product-field']"
    
    def get_subtitle_path(self):
        return ".//h2/span[@class='subtitle product-field']"
    
    def get_authors_path(self):
        return "//span[@class='visible-contributors']/a[@class='contributor-name']"

    def get_isbn_path(self):
        return "//div[@class='bookitem-secondary-metadata']/ul/li"

    def get_format_path(self):
        return "//div[@class='bookitem-secondary-metadata']/h2"

    def get_img_url_path(self):
        return "//img[@class='cover-image  notranslate_alt']/@src"

    def get_desc_path(self):
        return "//div[@class='synopsis-description']"

    def get_series_path(self):
        return ".//span[@class='product-sequence-field']/a"   

    def get_volume_path(self):
        return ".//span[@class='product-sequence-field']/a"

    def get_sale_ready_path(self):
        return "//h2[@class='pricing-title']"

    def sale_ready_parser(self, root):
        xpath = self.get_sale_ready_path()
        try:
            desc= root.xpath(xpath)[0].text
            sale_flag = 0 # 0 = Buy   1 = Pre-order
            status = ""
            # Check for the words 'Buy' and 'Pre-Order
            desc_list = desc.split(' ')
            for word in desc_list:
                if word == 'Buy':
                    sale_flag = 0
                    status = "Buy Now"
                if word == 'Pre-Order':
                    sale_flag = 1
                    status = "Pre-order"
        except:
            status = None

        return status


    def extraParser(self, root):
        return {}




 