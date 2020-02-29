from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from PIL import Image
import requests
from io import BytesIO
import urllib.request




class BookSite:

    #str -> SiteBookData
    #Given a direct link to a book page at a site,
    #parse it and return the SiteBookData of the info
    def get_book_data_from_site(self, url):
        sbd = SiteBookData()
        response = requests.get(url)
        content = response.content



        # We will add to this as we go
        sbd.book_title = self.titleParser(content)
        sbd.subtitle = self.subtitleParser(content)
        sbd.authors = self.authorsParser(content)
        sbd.isbn_13 = self.isbnParser(content)
        sbd.format =  self.formatParser(content)
        sbd.book_img = self.imageParser(content)
        sbd.book_img_url = self.imageUrlParser(content)
        sbd.description = self.descParser(content)
        sbd.series = self.seriesParser(content)
        sbd.volume_number = self.volumeParser(content)
        sbd.ready_for_sale = self.saleReadyParser(content)
        
        return sbd


        #str -> str
        #Given a book_id, return the direct url for the book
    def covert_book_id_to_url(self, book_id):
        pass

        #------------ Utility Methods -------------
    def titleParser(self, content):
        pass

    def subtitleParser(self,content):
        pass
            
    def authorsParser(self,content):
        pass

    def isbnParser(self, content):
        pass

    def formatParser(self, content):
        pass

    def imageParser(self, content):
        pass

    def imageUrlParser(self, content):
        pass

    def descParser(self, content):
        pass

    def seriesParser(self, content):
        pass

    def volumeParser(self, content):
        pass

    def saleReadyParser(self, content):
        pass

    def extraParser(self, content):
        pass
  





    #SiteBookData -> List[Tuple[SiteBookData, float]]
    #Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
    #likely matches paired with how good of a match it is (1.0 is an exact match). 
    # This should take into account all the info we have about a book, including the cover."""
        def find_book_matches_at_site(self, book_data):
            pass

##################### End of Class ##############################


def get_book_site(slug):
    site  = ""
    if slug == 'GO':
        #Google Books
        pass
    elif slug == 'KO':
        site = KoboSite() 
    elif slug == 'TB':
        #Test Bookstore
        pass
    elif slug == 'LC':
        #Livraria Clutura
        pass
    elif slug == 'SC':
        #Scribd
        pass

    return site

   

################### Begining of KoboSite ######################
"""parses the book data from kobo"""
class KoboSite(BookSite):

    #------------ Override Utility Methods -------------
    def titleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        title_element = root.xpath(".//h1/span[@class='title product-field']")[0]
        title = title_element.text
        return title

    def subtitleParser(self,content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        subtitle = ''
        if root.xpath(".//h2/span[@class='subtitle product-field']"):
            subtitle = root.xpath(".//h2/span[@class='subtitle product-field']")[0].text
        return subtitle
        
        

    def authorsParser(self,content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        author_elements = root.xpath("//span[@class='visible-contributors']/a[@class='contributor-name']")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
        return authors

    def isbnParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() #prove that isbn_13 is always 3rd li/span item.
        isbn_elements = root.xpath("//div[@class='bookitem-secondary-metadata']/ul/li")
        isbn=''
        for isbn_tmp in isbn_elements:
            if isbn_tmp.text.strip()=='ISBN:':
                isbn =isbn_tmp.xpath('./span')[0].text
        return isbn

    def formatParser(self, content):
        #Kobo only has ebooks and audio books
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        format_element = root.xpath("//div[@class='bookitem-secondary-metadata']/h2")[0]
        form = format_element.text.strip().split(' ')[0]
        return form
        
    def imageParser(self, content):
        url =   self.imageUrlParser(content)
        response = requests.get(url)
        image = Image.open(urllib.request.urlopen(url))
        image.save("book_image.jpg")


    def imageUrlParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()  
        imgUrl_element = root.xpath("//img[@class='cover-image  notranslate_alt']/@src")[0] 
        imgUrl = "http:" + imgUrl_element
        return imgUrl

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        desc_elements = root.xpath("//div[@class='synopsis-description']/p")[0]
        desc= etree.tostring(desc_elements, method='html', with_tail='False')
        # need to decide whther to take all or only the 1st p tag content
        return desc

    def seriesParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()  
        series_element = ''
        series = ''
        if root.xpath(".//span[@class='product-sequence-field']/a"):
            series_element = root.xpath(".//span[@class='product-sequence-field']/a")[0] 
            series = series_element.text

        #Seperate series number from series title
        series_split = series.split('#')
        return series_split[0]




    def volumeParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()  
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

    def saleReadyParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
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


    def extraParser(self, content):
        pass























