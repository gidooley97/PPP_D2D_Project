from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from PIL import Image
import requests
from io import BytesIO
import urllib.request
from checkmate import BookSite

############ KoboSite Class ################
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
        image.save("here.jpg")


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
















