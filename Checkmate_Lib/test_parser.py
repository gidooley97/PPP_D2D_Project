from site_book_data import SiteBookData
import io
from lxml import etree
import requests
import re

############ KoboSite Class ################
"""parses the book data from kobo"""
class KoboSite:
    def __init__(self):
        pass
     
    def get_book_data_from_site(self,url):
        pass

    def find_matches_at_site(self,book_data):
        pass

    def convert_book_id_to_url(self,book_id):
        pass

    #------------ Utility Methods -------------
    def titleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        title_element = root.xpath(".//h1")[0]
        title = title_element.text
        return title

    def subtitleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        subtitle_element = root.xpath("/html/body/div[3]/div/h2")[0]
        subtitle = subtitle_element.text
        return subtitle
        
        

    def authorsParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        author_element = root.xpath(".//h3")[0]
        author = author_element.text[3:]
        author = author.split(',')
        return author

    def isbnParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        isbn_element = root.xpath("/html/body/div[3]/div/div/h6[4]/text()")
        isbn = isbn_element
        return isbn

    def formatParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        format_type = root.xpath("/html/body/div[3]/div/div/h6[6]/text()")[0]
        return format_type

    def imageParser(content):
        pass

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        desc_elements = root.xpath("/html/body/div[3]/div/div/p[@class='indent_this']/text()")
        full_desc = ""
        print(desc_elements)
        for desc in desc_elements:
            full_desc = full_desc+desc
        if len(full_desc) == 0:
            full_desc
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', full_desc)

        return cleantext

    def seriesParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        series = root.xpath("/html/body/div[3]/div/div/h6[2]/text()")[0]
        return series

    def volumeParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        volume = root.xpath("/html/body/div[3]/div/div/h6[3]/text()")[0]
        return volume

    def contentParser(content):
        pass

    def saleReadyParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        saleReady = root.xpath("/html/body/div[3]/div/div/p[2]")[0]
        return saleReady

    def extraParser(content):
        pass

    def imageUrlParser(content):
        pass

    #parseAll parses all data, prints it, and 
    #stores it in a SiteBookData Object
    def parseAll(content, SiteBookData):
        pass

    def tester(content):
        print("Hello")
   

############# End of Class #################



def main():
    url = "http://127.0.0.1:8000/books/4/"
    #url = prompt("Enter a url");
    content = fetch(url)
    site = KoboSite() 
    print(site.titleParser(content))
    print(site.authorsParser(content))
    print(site.isbnParser(content))
    print(site.descParser(content))
    print(site.formatParser(content))
    print(site.subtitleParser(content))
    print(site.seriesParser(content))
    print(site.volumeParser(content))
    print(site.saleReadyParser(content))

  
def fetch(url):
    response = requests.get(url)
    return response.content

if __name__ == "__main__":
    main()