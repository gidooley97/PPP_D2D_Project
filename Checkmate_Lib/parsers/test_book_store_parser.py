from site_book_data import SiteBookData
from bookSite import BookSite
import io
from lxml import etree
import requests
import re
import mechanize

############ TestSite Class ################
"""parses the book data from test bookstore"""
class TestSite(BookSite):
    def __init__(self):
        super().__init__()
        self.site_slug = "TB"
        self.search_url = "http://127.0.0.1:8000/books/search/"
        self.url_to_book_detail ="http://127.0.0.1:8000/books/"
     
    def get_book_data_from_site(self,url):
        return super().get_book_data_from_site(url)


    #override
    def convert_book_id_to_url(self,book_id):
        url = self.url_to_book_detail+book_id
        return url

    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1,site_book2)

#----------------------------- Utility Methods -------------------------------------
    def titleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        title_element = root.xpath(".//h1")[0]
        title = title_element.text
        return title

    #override the method in the parent class
    def authors_parser(self, root):
        try:
            author_element = root.xpath(self.get_authors_path())[0]
            author = author_element.text[3:]
            authors = author.split(',')
        except:
            authors = None
        return authors

    #override this method in the parent class
    def image_parser(self, url):
        return None

    #override this method
    def image_url_parser(self, root):
        return None

    #override this method
    def desc_parser(self, root):
        try: 
            desc_elements = root.xpath("/html/body/div[3]/div/div/p[@class='indent_this']/text()")[0]
        except IndexError:
            desc_elements = root.xpath("/html/body/div[3]/div/div/p/text()")
            full_desc = ""
            for desc in desc_elements:
                full_desc = full_desc+desc

            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, ' ', full_desc)
            return cleantext
        return desc_elements

    #override
    def volume_parser(self, root):
        xpath = self.get_volume_path()
        try: 
            volume = root.xpath(xpath)[0]
        except IndexError:
            volume = None
        return volume
        
        
    #override
    def price_parser(self, root):
        try:
            price = root.xpath("/html/body/div[3]/div/div/h6[1]/text()")[0]
        except:
            price=None
        return price

    #override

    def format_parser(self, root):
        path = self.get_format_path()
        try: 
            format = root.xpath(path)[0]
        except:
            format = None
        return format


    #override
    def extra_parser(self, root):
        return {"price":self.price_parser(root)}
#--------------------------------------------------------------------------------------------------------------------------

####################################### Get XPath Functions ######################################
    """
    Return specific xpath.

    These methods should be overriden. otherwise it won't work.
        params:
            None
        return:
            xpath-specific xpath(str) 
    """
    def get_search_urls_after_search_path(self):
        return ".//button[@class='button button2 text-right']/a/@href"
    def get_title_path(self):
        return ".//h1"
    
    def get_subtitle_path(self):
        return "/html/body/div[3]/div/h2"
    
    def get_authors_path(self):
        return ".//h3"

    def get_isbn_path(self):
        return "/html/body/div[3]/div/div/h6[4]/text()"

    def get_format_path(self):
        return "/html/body/div[3]/div/div/h6[6]/text()"

    def get_img_url_path(self):
        return "//img[@class='cover-image  notranslate_alt']/@src"

    def get_desc_path(self):
        return "//div[@class='synopsis-description']"

    def get_series_path(self):
        return "/html/body/div[3]/div/div/h6[2]/text()"   

    def get_volume_path(self):
        return "/html/body/div[3]/div/div/h6[3]/text()"

    def get_sale_ready_path(self):
        return "/html/body/div[3]/div/div/p[@style='color: red;' or @style='color: green;']/text()"

##########################################################################################

