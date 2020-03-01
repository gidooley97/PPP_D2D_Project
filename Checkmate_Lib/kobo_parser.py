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


############ KoboSite Class ################
"""parses the book data from kobo"""
class KoboSite(BookSite):
    
    def __init__(self):
        self.site_slug = "KB"
        self.search_url="https://www.kobo.com/"
        self.url_to_book_detail ="https://www.kobo.com/us/en/ebook/"#set to ebook bcs D2D deals with ebooks mainly
        self.match_list=[] 
    #returns list of site books
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
        book_site_data = SiteBookData(frmt, title, img, img_url,isbn13,desc, series, 
        vol_num, subtitle, authors,book_id, site_slug, parse_status, url, content,
        ready_for_sale, extra)
        return book_site_data

        

    def find_book_matches_at_site(self,site_book_data):
        url =self.search_url
        print("url:", url)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(url)  
        #selects the form to populate 
        br.select_form(class_="search-form")
        search_txt =''
        #populate the field. You may need to check if this is actually working
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        br['query'] =search_txt
        
        #submit the form and get the returned page.
        res=br.submit()
        self.__get_book_data_from_page(res.read(), site_book_data)
        return self.match_list # for testing I get the first page results only
        while(True):
            try:
                print("nextpage")
                res=br.follow_link(text="Next")
                self.__get_book_data_from_page(res.read(), site_book_data)
            except mechanize._mechanize.LinkNotFoundError:
                print("Reached end of results")
                return self.match_list
            
    #gets url and pass it to get_book_data_from_site to get books
    def __get_book_data_from_page(self, content, book_site_dat_1):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        url_elements = root.xpath(".//p[@class='title product-field']/a/@href")

        for url in url_elements:
            #call function to get book data with url
            book_site_dat_tmp= self.get_book_data_from_site(url)
            score = self.match_percentage(book_site_dat_1, book_site_dat_tmp) 
            book_data_score =tuple([score,book_site_dat_tmp])
            #print('score', score)
            #book_site_dat_tmp.print_all()
            self.match_list.append(book_data_score)
        
                   


    # return url
    def convert_book_id_to_url(self,book_id):
        return self.url_to_book_detail+book_id

 
    #calls the match_percentage function in the super class
    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1,site_book2)



    #content specific parser methods 

    def titleParser(self, root):
        title_element = root.xpath(".//h1/span[@class='title product-field']")[0]
        title = title_element.text
        return title

    def subtitleParser(self,root):
        subtitle = ''
        if root.xpath(".//h2/span[@class='subtitle product-field']"):
            subtitle = root.xpath(".//h2/span[@class='subtitle product-field']")[0].text
        return subtitle
        
        

    def authorsParser(self,root):
        author_elements = root.xpath("//span[@class='visible-contributors']/a[@class='contributor-name']")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
        return authors

    def isbnParser(self, root):
        isbn_elements = root.xpath("//div[@class='bookitem-secondary-metadata']/ul/li")
        isbn=''
        for isbn_tmp in isbn_elements:
            if isbn_tmp.text.strip()=='ISBN:':
                isbn =isbn_tmp.xpath('./span')[0].text
        return isbn

    def book_id_parser(self, url):
        #book_id is the last part of the url
        book_id  =url.split('/')[len(url.split('/'))-1] 
        return book_id 
        
    def formatParser(self, root):
        #Kobo only has ebooks and audio books
        format_element = root.xpath("//div[@class='bookitem-secondary-metadata']/h2")[0]
        form = format_element.text.strip().split(' ')[0]
        return form
        
    def imageParser(self, url):
        #response = requests.get(url)
        image =None
        try:
            image = Image.open(urllib.request.urlopen(url))
        except:
            pass
        #image.save("here.jpg")
        return image


    def imageUrlParser(self, root): 
        imgUrl_element = root.xpath("//img[@class='cover-image  notranslate_alt']/@src")[0] 
        imgUrl = "http:" + imgUrl_element
        return imgUrl

    def descParser(self, root):
        #gets the descriptions with all the tags included.
        desc_element_list = root.xpath("//div[@class='synopsis-description']")[0]
        # need to decide whther to take all or only the 1st p tag content
        xmlstr = etree.tostring(desc_element_list, encoding='utf8', method='xml')        
        return str(xmlstr)
        

    def seriesParser(self, root):
        series_element = ''
        series = ''
        if root.xpath(".//span[@class='product-sequence-field']/a"):
            series_element = root.xpath(".//span[@class='product-sequence-field']/a")[0] 
            series = series_element.text

        #Seperate series number from series title
        series_split = series.split('#')
        return series_split[0]

    def get_parse_status(self,title, isbn13, desc, authors):
         #determine parse_status checks if we have the most basic data about a book
        if title and isbn13 and desc and authors:
            return "UNSUCCESSFUL"
        return "FULLY_PARSED"


    def volumeParser(self, root):
        series_element = ''
        volume = ''
        if root.xpath(".//span[@class='product-sequence-field']/a"):
            series_element = root.xpath(".//span[@class='product-sequence-field']/a")[0] 
            series = series_element.text
        
            #Seperate series number from series title
            
            series_split = series.split('#')
            if len(series_split) > 1:
                volume = series_split[1]
        return volume

  
    def saleReadyParser(self, root):
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

        return status


    def extraParser(self, root):
        return {}




 