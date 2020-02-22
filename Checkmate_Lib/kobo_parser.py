from site_book_data import SiteBookData
import io
from lxml import etree
import requests

############ KoboSite Class ################
"""parses the book data from kobo"""
class KoboSite:
    def __init__():
        pass
     
    def get_book_data_from_site(self,url):
        pass

    def find_matches_at_site(self,book_data):
        pass

    def convert_book_id_to_url(self,book_id):
        pass

    #------------ Utility Methods -------------
    def titleParser(content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        #title_element = root.xpath(".//h1[@itemprop='name']")[0]
        #title = title_element.text
        return title

    def subtitleParser(contnet):
        pass
        

    def authorsParser(content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        #author_element = root.xpath(".//span[@id='key-contributors']/a")[0]
        #author = author_element.text
        return author

    def isbnParser(content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        return isbn

    def formatParser(content):
        pass

    def imageParser(content):
        pass

    def descParser(content):
        pass

    def seriesParser(content):
        pass

    def volumeParser(content):
        pass

    def contentParser(content):
        pass

    def saleReadyParser(content):
        pass

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
    url = "https://www.kobo.com/us/en/ebook/the-green-mile-2"
   # url = prompt("Enter a url");
    content = fetch(url)
    site = KoboSite() 
    site.titleParser()
  
def fetch(url):
    response = requests.get(url)
    return response.content








if __name__ == "__main__":
    main()










