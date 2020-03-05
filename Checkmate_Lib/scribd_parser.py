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

############ Scribd Site Class ################
"""parses the book data from Scribd"""
class ScribdSite:
    def __init__(self):
        self.site_slug = "SC"
        self.search_url = "https://www.scribd.com"
        self.url_to_book_detail ="https://www.scribd.com/book"#set to ebook bcs D2D deals with ebooks mainly
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
        book_site_data = SiteBookData(content=content, book_title=title, authors=authors, isbn_13=isbn13, format=frmt,
         description=desc, series=series, volume=vol_num, ready_for_sale=ready_for_sale)
        return book_site_data

    def find_matches_at_site(self,site_book_data):
        search_txt =''
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []

        payload ={'ft':search_txt, 'originalText':search_txt}
        content = requests.get(self.search_url,params=payload).content
        url =  requests.get(self.search_url,params=payload).url
        self.__get_book_data_from_page(content,site_book_data)
        page=1
        while(True):
            print('Page',page)
            content= requests.get(url+"#"+str(page)).content

            parser = etree.HTMLParser(remove_pis=True)
            tree = etree.parse(io.BytesIO(content), parser)
            root = tree.getroot()
          
            self.__get_book_data_from_page(content, site_book_data)
            if root.xpath(".//nav[@aria-label='Pagination']"):
                if root.xpath(".//nav[@aria-label='Pagination']/ul/li[6]/a"):
                    print("done!")
                    break
                else:
                    page+=1
            else:
                print("done!")
                break
        
        return self.match_list

    def __get_book_data_from_page(self, content, book_site_dat_1):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        url_elements = root.xpath(".//div[@class='list_anchor_container']/a/@href")

        for url in url_elements:
            #call function to get book data with url
            #print('url', url)
            book_site_dat_tmp= self.get_book_data_from_site(url)
            score = self.match_percentage(book_site_dat_1, book_site_dat_tmp) 
            book_data_score =tuple([score,book_site_dat_tmp])
            self.match_list.append(book_data_score)

    def convert_book_id_to_url(self,book_id):
        url = "https://www.scribd.com/book/"+book_id
        return url

    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1,site_book2)

    #------------ Utility Methods -------------
    def titleParser(self, root):
        title_element = root.xpath(".//h1[@class='document_title']")[0]
        title = title_element.text
        return title

    def subtitleParser(self,root):
        pass

    def authorsParser(self,root):
        author_elements = root.xpath(".//a[contains(@href,'https://www.scribd.com/author')]")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
        return authors

    def isbnParser(self, root):
        isbn_element = root.xpath("/html/head/meta[18]/@content")
        isbn = isbn_element[0]
        return isbn

    def book_id_parser(self, url): 
        book_id = url.split('/')[len(url.split('/'))-2]
        return book_id

    def formatParser(self, root):
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

    def descParser(self, root):
        desc_elements = root.xpath("/html/head/meta[16]/@content")
        desc = desc_elements
        print(desc) 
        return str(desc)

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

    def saleReadyParser(self, root):
        saleReady = "Avaliable"
        print(saleReady)
        return saleReady
    
    def extraParser(self,root):
        pass

    def imageUrlParser(self, root):
        imageUrlParser_element = root.xpath("/html/head/link[5]/@href")
        imageURL = imageUrlParser_element[0]
        print(imageURL) 
        return imageURL

    def get_parse_status(self,title, isbn13, desc, authors):
        #determine parse_status checks if we have the most basic data about a book
        if title and isbn13 and desc and authors:
            return "UNSUCCESSFUL"
        return "FULLY_PARSED"

  ############# End of Class #################


def main():
    url = "https://www.scribd.com/book/163638327"
    content = fetch(url)
    site = ScribdSite() 
    
    book = site.get_book_data_from_site(url)
    matches = site.find_matches_at_site(book)
    for x in matches:
        x.print_all()
        
    

  
def fetch(url):
    response = requests.get(url)
    return response.content


if __name__ == "__main__":
    main()
