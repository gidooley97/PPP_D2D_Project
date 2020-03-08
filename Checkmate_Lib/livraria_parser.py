from site_book_data import SiteBookData
import io
from lxml import etree, html
from PIL import Image
import requests
from io import BytesIO
import urllib.request
import requests
import lxml.html
import mechanize
from bookSite import BookSite
import re
import json

############ KoboSite Class ################

class LivrariaSite(BookSite):
    def __init__(self):
        self.site_slug = "LC"
        self.search_url="https://www3.livrariacultura.com.br/ebooks/" # to only return only ebooks
        self.url_to_book_detail = "https://www3.livrariacultura.com.br/"
        self.match_list=[] 
    def get_book_data_from_site(self,url):
        content = requests.get(url).content#gets the book's page 
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        title = self.titleParser(root)
        img_url = self.imageUrlParser(root)
        img = self.imageParser(img_url)#use the img url to get image
        isbn13= self.isbnParser(root)
        desc = self.descParser(root)
        frmt = self.formatParser(root)
        series = self.seriesParser(root)
        vol_num = self.volumeParser(root)
        subtitle = self.subtitleParser(root)
        authors = self.authorsParser(root)
        site_slug = self.site_slug
        content =content #html page content
        url = url
        book_id = self.book_id_parser(url)
        parse_status =  self.get_parse_status(title,isbn13,desc,authors)
        ready_for_sale = self.saleReadyParser(root) # figure out if 'pre-order' is considered ready for sale
        extra = self.extraParser(root)
        book_site_data = SiteBookData(format=frmt, book_title=title, book_img= img, book_img_url=img_url, isbn_13=isbn13, description=desc, series=series, 
        volume=vol_num, subtitle=subtitle, authors=authors, book_id=book_id, site_slug=site_slug, parse_status=parse_status, url=url, content=content,
        ready_for_sale=ready_for_sale, extra=extra)
        return book_site_data

    def find_book_matches_at_site(self,site_book_data,pages=2):
        #to get the max results set pages to None. 
        # Set to 2 for testing purposes
        search_txt =''
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        self.match_list =[]
        #this site is hard to go to the next page. We used the PS param t specify how many search 
        #results we want to see on one page. The max is 96 
        print("search", search_txt)
        
        if not pages:
            results = 96 #Max
        else:
            results= pages*24
        url = self.search_url +search_txt+"?PS="+str(results)

        content = requests.get(url).content
        #print(content)
        self.__get_book_data_from_page(content,site_book_data)
               
        return self.match_list
        

    def __get_book_data_from_page(self, content, book_site_dat_1):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        url_elements = root.xpath(".//h2[@class='prateleiraProduto__informacao__nome']/a/@href")

        for url in url_elements:
            book_site_dat_tmp= self.get_book_data_from_site(url)
            score = self.match_percentage(book_site_dat_1, book_site_dat_tmp) 
            book_data_score =tuple([score,book_site_dat_tmp])
            self.match_list.append(book_data_score)

    def convert_book_id_to_url(self,book_id):
        return self.url_to_book_detail+book_id+'/p'

    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1,site_book2)

    #------------ Utility Methods -------------
    
    def titleParser(self, root):
        title_element = root.xpath("//*[@id='product-page']/section[2]/div/div/h1/div")[0]
        title = title_element.text
        return title

    def subtitleParser(self,root):
        subtitle = ''
        if root.xpath("//td[@class='value-field Subtitulo']"):
            subtitle = root.xpath("//td[@class='value-field Subtitulo']")[0].text
        return subtitle

    def book_id_parser(self, url):
        #book_id is the last part of the url
        book_id  =url.split('/')[len(url.split('/'))-1] 
        return book_id 
        
        

    def authorsParser(self,root):
        author_elements = root.xpath("//td[@class='value-field Colaborador']/text()")
        authors = []
        for auth_element in author_elements:
            if auth_element.startswith('Autor:') | auth_element.startswith('Autores:') | auth_element.startswith('Tradutor:') | auth_element.startswith('Leitor/Narrador:'):
                auth_element=re.sub('Autor:', '', auth_element)
                auth_element=re.sub('Autores:', '', auth_element)
                auth_element=re.sub('Tradutor:', '', auth_element)
                auth_element=re.sub('Leitor/Narrador:', '', auth_element)
                authors.append(auth_element)
            else:
                authors.append("No authors")
        return authors


    def isbnParser(self, root):
        try:
            isbn_element = root.xpath("//td[@class='value-field ISBN']")[0].text
            isbn = isbn_element
        except:
            isbn=''
        return isbn

    def formatParser(self, root): 
        try:
            format_element = root.xpath("//td[@class='value-field Formato']")[0].text
            form = format_element
        except:
            form=''
        return form

    def seriesParser(self, root):
        series = ''
        return series

    def volumeParser(self, root):
        volume = ''
        return volume
    
    def get_parse_status(self,title, isbn13, desc, authors):
         #determine parse_status checks if we have the most basic data about a book
        if title and isbn13 and desc and authors:
            return "UNSUCCESSFUL"
        return "FULLY_PARSED"
        

    def imageParser(self, url):
        #response = requests.get(url)
        image =None
        try:
            image = Image.open(urllib.request.urlopen(url))
        except:
            pass
        return image

    def descParser(self, root):
        try:
            desc_elements = root.xpath("//td[@class='value-field Sinopse']")[0].text
            desc=desc_elements
        except:
            desc =''
        return desc


    def saleReadyParser(self, root):
        try:
            sale_flag = 0 # 0 = For Sale   1 = Not For Sale
            status = "For Sale"
            checker = root.xpath("//script")[208]
            print(checker)
            # sale_flag = 1
            status='Not For Sale'
        except:
            status = 'F'

        return status

    def imageUrlParser(self, root):  
        imgUrl_element = root.xpath("//a[@class='image-zoom']/@href")[0]
        imgUrl = imgUrl_element
        return imgUrl

    def extraParser(self, root):
        return {}
   
    ############# End of Class #################



