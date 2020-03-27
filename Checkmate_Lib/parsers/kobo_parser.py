from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from PIL import Image
import requests
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
        self.search_url="https://www.kobo.com/"
        self.url_to_book_detail ="https://www.kobo.com/us/en/ebook/"#set to ebook bcs D2D deals with ebooks mainly
        
    """
    returns the volume number of  the book.

    Args:
        root-- root of the tree.
    """
    def volumeParser(self, root):
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

    
    def find_book_matches_by_attr_at_site(self, search_txt,pages=2):
        url =self.search_url
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(url)  
        #selects the form to populate 
        br.select_form(class_="search-form")
        if search_txt =='':
            return []
        br['query'] =search_txt
        self.match_list=[]
        #submit the form and get the returned page.
        res=br.submit()
        self.get_search_book_data_from_page(res.read(), None, False)#get page 1 of results
        #return self.match_list # for testing I get the first page results only
        page=2
        while(page <=pages):#limit the results we will get
            try:
                res=br.follow_link(text="Next")
                self.get_search_book_data_from_page(res.read(), None, False)
                page+=1
            except mechanize._mechanize.LinkNotFoundError:#end of results
                break
        return self.match_list

    """
    SiteBookData -> List[Tuple[SiteBookData, float]]
    
    Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
    likely matches paired with how good of a match it is (1.0 is an exact match). 
    This should take into account all the info we have about a book, including the cover.
    Different for every site. To be overriden by every site.
    params:
        book_data: a  bookSiteData.
    returns:
        match:List[Tuple[SiteBookData, float]]
    """
    def find_book_matches_at_site(self,site_book_data, pages=2):
        url =self.search_url
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(url)  
        #selects the form to populate 
        br.select_form(class_="search-form")
        search_txt =''
        #populate the field. You may need to check if this is actually working
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn_13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        br['query'] =search_txt
        self.match_list=[]
        #submit the form and get the returned page.
        res=br.submit()
        super().get_search_book_data_from_page(res.read(), site_book_data)#get page 1 of results
        #return self.match_list # for testing I get the first page results only
        page=2
        while page <=pages:#limit the results we will get
            try:
                res=br.follow_link(text="Next")
                super().get_search_book_data_from_page(res.read(), site_book_data)
                page+=1
            except mechanize._mechanize.LinkNotFoundError:#end of results
                break
        return self.match_list
            
   
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


    def saleReadyParser(self, root):
        try:
            desc= root.xpath("//h2[@class='pricing-title']")[0].text
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
            status = 'F'

        return status


    def extraParser(self, root):
        return {}




 