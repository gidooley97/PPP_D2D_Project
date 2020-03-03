from site_book_data import SiteBookData
import io
from lxml import etree
import requests

############ Scribd Site Class ################
"""parses the book data from Scribd"""
class ScribdSite:
    def __init__(self):
        pass
     
    def get_book_data_from_site(self,url):
        pass

    def find_matches_at_site(self,book_data):
        #query is search?query='string'
        return string

    def convert_book_id_to_url(self,book_id):
        url = "https://www.scribd.com/book/"+book_id
        return url

    #------------ Utility Methods -------------
    def titleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        print(root)
        title_element = root.xpath(".//h1[@class='document_title']")[0]
        title = title_element.text
        print(title)
        return title

    def subtitleParser(self,content):
        pass

    def authorsParser(self,content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        author_elements = root.xpath(".//a[contains(@href,'https://www.scribd.com/author')]")
        print(author_elements)
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
            print(auth_element.text)
        return authors

    def isbnParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        isbn_element = root.xpath("/html/head/meta[18]/@content")
        isbn = isbn_element[0]
        print(isbn)
        return isbn


    def formatParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        format_element = root.xpath("/html/head/meta[13]/@content")
        form = format_element[0]
        print(form)
        return form
        

    def imageParser(self, content):
        url =   self.imageUrlParser(content)
        print("Image Function: " + url)
        response = requests.get(url)
        image = Image.open(urllib.request.urlopen(url))
        image.save("here.jpg")

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        desc_elements = root.xpath("/html/head/meta[16]/@content")
        desc = desc_elements[0]
        print(desc) 
        return desc

    def seriesParser(self, title):
        for seriesCheck in title:
            if seriesCheck.isdigit():
                num = seriesCheck

        if title.find("series"):
                title = "Series"            
        
        print(title+" #"+num)
        return title

        
    def volumeParser(self, title):
        for volumeCheck in title:
            if volumeCheck.isdigit():
                num = "#"+volumeCheck
            else:
                num = "None"

        if title.find("volume"):
            title = "Volume" 
        else: 
            title = "None"
        
        print(title+" "+num)
        return title

    def editionParser(self, title):
        for editionCheck in title:
            if editionCheck.isdigit():
                num = editionCheck
            else:
                num = "None"

        if title.find("edition"):
            title = "Edition:" 
        else: 
            title = "None"
        
        print(title+" "+num)
        return title

    def saleReadyParser(content):
        pass

    def extraParser(content):
        pass

    def imageUrlParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        imageUrlParser_element = root.xpath("/html/head/link[5]/@href")
        imageURL = imageUrlParser_element[0]
        print(imageURL) 
        return imageURL

    #parseAll parses all data, prints it, and 
    #stores it in a SiteBookData Object
    def parseAll(content, SiteBookData):
        pass

    ############# End of Class #################



def main():
    url = "https://www.scribd.com/book/163638327/Good-Omens-The-Nice-and-Accurate-Prophecies-of-Agnes-Nutter-Witch"
    #url = prompt("Enter a url");
    content = fetch(url)
    site = ScribdSite() 
    title = site.titleParser(content)
    site.authorsParser(content)


  
def fetch(url):
    response = requests.get(url)
    return response.content


if __name__ == "__main__":
    main()
