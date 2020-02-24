from site_book_data import SiteBookData
import io
from lxml import etree
import requests

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
        print(root)
        title_element = root.xpath(".//h1/span[@class='title product-field']")[0]
        title = title_element.text
        print(title)
        return title

    def subtitleParser(self,content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        subtitle = ''
        if root.xpath(".//h2/span[@class='subtitle product-field']"):
            subtitle = root.xpath(".//h2/span[@class='subtitle product-field']")[0].text
        print(subtitle)
        return subtitle
        
        

    def authorsParser(self,content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        author_elements = root.xpath("//span[@class='visible-contributors']/a[@class='contributor-name']")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
            print(auth_element.text)
        return authors

    def isbnParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() #prove that isbn_13 is always 3rd li/span item.
        isbn_element = root.xpath("//div[@class='bookitem-secondary-metadata']/ul/li")[3].xpath('./span')[0]
        isbn = isbn_element.text
        print(isbn)
        return isbn

    def formatParser(self, content):
        #Kobo only has ebooks
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        format_element = root.xpath("//div[@class='bookitem-secondary-metadata']/h2")[0]
        form = format_element.text.strip().split(' ')[0]
        print(form)
        return form
        

    def imageParser(self, content):
        pass # need to figure out this part

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        desc_elements = root.xpath("//div[@class='synopsis-description']/p")[0]
        desc= etree.tostring(desc_elements, method='html', with_tail='False')
        # need to decide whther to take all or only the 1st p tag content
        print(desc) 
        return desc

    def seriesParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()  
        series_element = ''
        if root.xpath(".//span[@class='product-sequence-field']/a"):
            series_element = root.xpath(".//span[@class='product-sequence-field']/a")[0] 
            series = series_element.text

        #Seperate series number from series title
        series_split = series.split('#')
        print(series_split[0]) #volume is include in the series, find a way return both.
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
            volume = series_split[1]
        print(volume)
        return volume

    def saleReadyParser(self, content):
        pass

    def imageUrlParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()  
        imgUrl_element = root.xpath("//img[@class='cover-image  notranslate_alt']/@src")[0] 
        imgUrl = imgUrl_element
        print(imgUrl)
        return imgUrl

    def extraParser(self, content):
        pass



    

    #parseAll parses all data, prints it, and 
    #stores it in a SiteBookData Object
    def parseAll(content, SiteBookData):
        pass

   
   
    ############# End of Class #################



def main():
    url = "https://www.kobo.com/us/en/ebook/the-lion-the-witch-and-the-wardrobe-1"
   # url = prompt("Enter a url");
    content = fetch(url)
    site = KoboSite() 
    #site.titleParser(content)
    #site.authorsParser(content)
    #site.isbnParser(content)
    #site.formatParser(content)
    #site.descParser(content)
    #site.subtitleParser(content)
    #site.seriesParser(content)
    #site.volumeParser(content)
    #site.imageUrlParser(content)
    site.saleReadyParser(content)
  
def fetch(url):
    response = requests.get(url)
    return response.content








if __name__ == "__main__":
    main()










