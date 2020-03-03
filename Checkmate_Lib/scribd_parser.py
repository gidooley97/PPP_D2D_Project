from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from PIL import Image
import requests
from io import BytesIO
import urllib.request
import re

############ Scribd Site Class ################
"""parses the book data from Scribd"""
class ScribdSite:
    def __init__(self):
        pass
     
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
        series = self.seriesParser(title)
        vol_num = self.volumeParser(title)
        subtitle = self.subtitleParser(root)
        authors = self.authorsParser(root)
        site_slug = self.site_slug
        content = content #html page content
        url = url
        book_id = self.book_id_parser(url)
        parse_status =  self.get_parse_status(title,isbn13,desc,authors)
        ready_for_sale = self.saleReadyParser(root) # figure out if 'pre-order' is considered ready for sale
        extra = self.extraParser(root)
        book_site_data = SiteBookData(frmt, title, img, img_url,isbn13,desc, series, 
        vol_num, subtitle, authors,book_id, site_slug, parse_status, url, content,
        ready_for_sale, extra)
        return book_site_data

    def find_matches_at_site(self,book_data):
        pass

    def convert_book_id_to_url(self,book_id):
        url = "https://www.scribd.com/book/"+book_id
        return url

    #------------ Utility Methods -------------
    def titleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
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
        author_elements = root.xpath(".//span[@class='author']")
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
        

    def imageParser(self, url):
        image = None
        try:
            image = Image.open(urllib.request.urlopen(url))
        except:
            print("error")
        return image

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        desc_elements = root.xpath("/html/head/meta[16]/@content")
        desc = desc_elements[0]
        print(desc) 
        return desc

    def seriesParser(self, title):
        title = ""
        num = ""
        for seriesCheck in title:
            if seriesCheck.isdigit():
                num = "#"+seriesCheck
                if title.find("series"):
                    title = "Series" 
                else:
                    num = ""
            else:
                num = ""
        series = title+" "+num
        print(series)
        return series

        
    def volumeParser(self, title):
        title = ""
        num = ""
        for volumeCheck in title:
            if volumeCheck.isdigit():
                num = "#"+volumeCheck
                if title.find("volume"):
                    title = "Volume" 
                else: 
                    title = ""
            else:
                num = ""

        volume = title+" "+num
        print(volume)
        return volume

    def saleReadyParser(self, content):
        saleReady = "Avaliable"
        print(saleReady)
        return saleReady
    
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
        print("Title: ")
        site.titleParser(content)
        print("Authors: ")
        site.authorsParser(content)
        print("ISBN: ")
        site.isbnParser(content)
        print("Format: ")
        site.formatParser(content)
        print("Description: ")
        site.descParser(content)
        print("Subtitle: ")
        site.subtitleParser(content)
        print("Series: ")
        site.seriesParser(content)
        print("Volume: ")
        site.volumeParser(content)
        print("Image URL: ")
        site.imageUrlParser(content)
        print("Ready Status: ")
        site.saleReadyParser(content)
        print("Image Saved")
        site.imageParser(content)

        def get_parse_status(self,title, isbn13, desc, authors):
         #determine parse_status checks if we have the most basic data about a book
            if title and isbn13 and desc and authors:
                return "UNSUCCESSFUL"
            return "FULLY_PARSED"

    ############# End of Class #################



def main():

    url = "https://www.scribd.com/book/322011391/The-Subtle-Art-of-Not-Giving-a-F-ck-A-Counterintuitive-Approach-to-Living-a-Good-Life"
    #url = prompt("Enter a url");
    content = fetch(url)
    site = ScribdSite() 
    title = site.titleParser(content)
    site.saleReadyParser(content)

  
def fetch(url):
    response = requests.get(url)
    return response.content

def fill_form(url):
    #This funcrion navigates the search page 
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)  
    #selects the form to populate 
    br.select_form(class_="search-form")
    #populate the field. You may need to check if this is actually working
    br['query'] ="lord of rings"
    print(br['query'])
    #submit the form and get the returned page.
    res=br.submit()
    fileobj = open("page.html","wb")#saves the returned page to a file. 
    #You can open and se the content
    fileobj.write(res.read())
    fileobj.close()
    #print(res.content)






if __name__ == "__main__":
    main()










