from site_book_data import SiteBookData
import io
from lxml import etree, html
from PIL import Image
import requests
from io import BytesIO
import urllib.request
import requests
import lxml.html

############ KoboSite Class ################

class LivrariaSite:
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
        title_element = root.xpath("//*[@id='product-page']/section[2]/div/div/h1/div")[0]
        title = title_element.text
        print(title)
        return title

    def subtitleParser(self,content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        subtitle = ''
        if root.xpath("//td[@class='value-field Subtitulo']"):
            subtitle = root.xpath("//td[@class='value-field Subtitulo']")[0].text
        print(subtitle)
        return subtitle
        
        

    def authorsParser(self,content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        author_elements = root.xpath("//td[@class='value-field Colaborador']/text()")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element)
            print(auth_element)
        return authors


    def isbnParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() #prove that isbn_13 is always 3rd li/span item.
        isbn_element = root.xpath("//td[@class='value-field ISBN']")[0].text
        isbn = isbn_element
        print(isbn)
        return isbn

    def formatParser(self, content):
        #Kobo only has ebooks
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        format_element = root.xpath("//td[@class='value-field Formato']")[0].text
        form = format_element
        print(form)
        return form
        

    def imageParser(self, content):
        url =   self.imageUrlParser(content)
        #url = "https://kbimages1-a.akamaihd.net/20f0c659-1d66-4f47-b034-219eb8f9a6a2/353/569/90/False/the-lion-the-witch-and-the-wardrobe-1.jpg"
        print("Image Function: " + url)
        #url = "https://kbimages1-a.akamaihd.net/20f0c659-1d66-4f47-b034-219eb8f9a6a2/353/569/90/False/the-lion-the-witch-and-the-wardrobe-1.jpg"
        #new_url = "http:" + url
        #image = Image.open(new_url)
       # image.save("here.jpg")

        response = requests.get(url)
        image = Image.open(urllib.request.urlopen(url))
        image.save("here.jpg")

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        desc_elements = root.xpath("//td[@class='value-field Sinopse']")[0].text
        #desc= etree.tostring(desc_elements, method='html', with_tail='False')
        # need to decide whther to take all or only the 1st p tag content
        desc=desc_elements
        print(desc) 
        return desc

    #def seriesParser(self, content):
        #parser = etree.HTMLParser(remove_pis=True)
        #tree = etree.parse(io.BytesIO(content), parser)
        #root = tree.getroot()  
        #series_element = ''
        #if root.xpath(".//span[@class='product-sequence-field']/a"):
            #series_element = root.xpath(".//span[@class='product-sequence-field']/a")[0] 
            #series = series_element.text

        #Seperate series number from series title
        #series_split = series.split('#')
        #print(series_split[0]) #volume is include in the series, find a way return both.
        #return series_split[0]




    #def volumeParser(self, content):
     #   parser = etree.HTMLParser(remove_pis=True)
      #  tree = etree.parse(io.BytesIO(content), parser)
       # root = tree.getroot()  
        #series_element = ''
        #volume = ''
        #if root.xpath(".//span[@class='product-sequence-field']/a"):
         #   series_element = root.xpath(".//span[@class='product-sequence-field']/a")[0] 
        #    series = series_element.text
        
            #Seperate series number from series title
         #   series_split = series.split('#')
          #  volume = series_split[1]
        #print(volume)
        #return volume

    def saleReadyParser(self, content): #need to work on the sales flag this weekend.
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        #desc= root.xpath("//li[@class='list-item']/text()")
        if root.xpath("//div[@class='store-pickup box-shadow d-flex']/text()"):
            desc = root.xpath("//div[@class='store-pickup box-shadow d-flex']/text()")
        print(desc)
        return desc

    def imageUrlParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()  
        imgUrl_element = root.xpath("//a[@class='image-zoom']/@href")[0]
        imgUrl = imgUrl_element
        print(imgUrl)
        return imgUrl

    def extraParser(self, content):
        pass



    

    #parseAll parses all data, prints it, and 
    #stores it in a SiteBookData Object
    def parseAll(self, content, SiteBookData):
        pass

   
   
    ############# End of Class #################



def main():
    url = "https://www3.livrariacultura.com.br/sapiens-2011667923/p"
   # url = prompt("Enter a url");
    content = fetch(url)
    
    site = LivrariaSite() 
    site.titleParser(content)
    site.authorsParser(content)
    site.isbnParser(content)
    site.formatParser(content)
    site.descParser(content)
    site.subtitleParser(content)
    #site.seriesParser(content)
    #site.volumeParser(content)
    site.imageUrlParser(content)
    #site.saleReadyParser(content)
  
def fetch(url):
    response = requests.get(url)
    return response.content
    








if __name__ == "__main__":
    main()










