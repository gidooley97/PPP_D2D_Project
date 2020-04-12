from site_book_data import SiteBookData
import io
from lxml import etree, html
from PIL import Image
import requests
from io import BytesIO
import urllib.request
import lxml.html
import mechanize
from bookSite import BookSite
import re
import json
from site_book_data import isbn_10_to_isbn_13

############ LivrariaSite Class ################
"""parses the book data from Livraria"""
class LivrariaSite(BookSite):
    def __init__(self):
        self.site_slug = "LC"
        self.search_url="https://www3.livrariacultura.com.br/ebooks/" # to only return only ebooks
        self.url_to_book_detail = "https://www3.livrariacultura.com.br/"
        self.match_list=[] 

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
    SiteBookData -> List[Tuple[SiteBookData, float]]
    
    Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
    likely matches paired with how good of a match it is (1.0 is an exact match). 
    This should take into account all the info we have about a book, including the cover.
    Overrides the method in the parent class. It builds a link and then gets and goes to every
    book using the urls in the search results. Gets max = 96 books that are in the search results.
    params:
        book_data: a  bookSiteData.
        pages: number of pages  to look through. Default=2
    returns:
        match:List[Tuple[SiteBookData, float]]
    """
    
    #override
    def find_book_matches_at_site(self,site_book_data,pages=2):
        #to get the max results set pages to None. 
        # Set to 2 for testing purposes
        search_txt =''
        if site_book_data.isbn_13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        self.match_list =[]
        #this site is hard to go to the next page. We used the PS param to specify how many search 
        #results we want to see on one page. The max is 96 
        if not pages:
            results = 96 #Max
        else:
            results= pages*24
        url = self.search_url +search_txt+"?PS="+str(results)

        content = requests.get(url).content
    
        super().get_search_book_data_from_page(content,site_book_data)
               
        return self.match_list
        
        
    def convert_book_id_to_url(self,book_id):
        return self.url_to_book_detail+book_id+'/p'


#------------------------------------ Utility Methods ------------------
    
    #override
    def subtitle_parser(self,root):
        subtitle = None
        if root.xpath("//td[@class='value-field Subtitulo']"):
            subtitle = root.xpath("//td[@class='value-field Subtitulo']")[0].text
        return subtitle

    #override
    def book_id_parser(self, url):
        #book_id is the last part of the url
        try:
            book_id  =url.split('/')[len(url.split('/'))-2] 
        except:
            book_id = None
        return book_id 
        
        
    #override
    def authors_parser(self,root):
        author_elements = root.xpath("//td[@class='value-field Colaborador']/text()")
        authors = []
        if not author_elements:
            return authors
        for auth_element in author_elements:
            if auth_element.startswith('Autor:') | auth_element.startswith('Autores:') | auth_element.startswith('Tradutor:') | auth_element.startswith('Leitor/Narrador:'):
                auth_element=re.sub('Autor:', '', auth_element)
                auth_element=re.sub('Autores:', '', auth_element)
                auth_element=re.sub('Tradutor:', '', auth_element)
                auth_element=re.sub('Leitor/Narrador:', '', auth_element)
                authors.append(auth_element)
        return authors
    #override
    def format_parser(self, root): 
        xpath = self.get_format_path()
        try:
            format_element = root.xpath(xpath)[0].text
            form = format_element
        except:
            form=None
        return form
    #override
    def isbn_parser(self, root):
        isbn = super().isbn_parser(root)
        if not isbn:
            return None
        if len(isbn)==10:
            return isbn_10_to_isbn_13(isbn)
        return isbn

    #override
    def series_parser(self, root):
        return None
    #override
    def volume_parser(self, root):
        return None

    #override
    def sale_ready_parser(self, root):
       return None


  
###############################################Utility Content Parser  Methods#########################################################################
    def get_search_urls_after_search_path(self):
        return ".//h2[@class='prateleiraProduto__informacao__nome']/a/@href"

    def get_title_path(self):
        return "//*[@id='product-page']/section[2]/div/div/h1/div"
    
    def get_subtitle_path(self):
        return ""
    
    def get_authors_path(self):
        return ""

    def get_isbn_path(self):
        return "//td[@class='value-field ISBN']"

    def get_format_path(self):
        return "//td[@class='value-field Formato']"

    def get_img_url_path(self):
        return "//a[@class='image-zoom']/@href"

    def get_desc_path(self):
        return "///td[@class='value-field Sinopse']"

    def get_series_path(self):
        return ""   

    def get_volume_path(self):
        return ""

    def get_sale_ready_path(self):
        return "//h2[@class='pricing-title']"

