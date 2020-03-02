from site_book_data import SiteBookData
import io
from lxml import etree, html
from PIL import Image
import requests
from io import BytesIO
import urllib.request
import requests
import lxml.html
import mechanize

############ KoboSite Class ################

class LivrariaSite:
    def __init__(self):
        self.site_slug = "LC"
        self.search_url="https://www3.livrariacultura.com.br"
        self.url_to_book_detail = "https://www3.livrariacultura.com.br/ebooks"
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
        #br.select_form(class_="busca")
        print(br)
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

    def convert_book_id_to_url(self,book_id):
        return self.url_to_book_detail+book_id

    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1,site_book2)

    #------------ Utility Methods -------------
    
    def titleParser(self, root):
        title_element = root.xpath("//*[@id='product-page']/section[2]/div/div/h1/div")[0]
        title = title_element.text
        return title

    def subtitleParser(self,root):
        subtitle = ''
        if root.xpath("//td[@class='value-field Subtitulo']"):
            subtitle = root.xpath("//td[@class='value-field Subtitulo']")[0].text
        return subtitle

    def book_id_parser(self, url):
        #book_id is the last part of the url
        book_id  =url.split('/')[len(url.split('/'))-1] 
        return book_id 
        
        

    def authorsParser(self,root):
        author_elements = root.xpath("//td[@class='value-field Colaborador']/text()")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element)
        return authors


    def isbnParser(self, root):
        isbn_element = root.xpath("//td[@class='value-field ISBN']")[0].text
        isbn = isbn_element
        return isbn

    def formatParser(self, root): 
        format_element = root.xpath("//td[@class='value-field Formato']")[0].text
        form = format_element
        return form

    def seriesParser(self, root):
        series = ''
        return series

    def volumeParser(self, root):
        volume = ''
        return volume
    
    def get_parse_status(self,title, isbn13, desc, authors):
         #determine parse_status checks if we have the most basic data about a book
        if title and isbn13 and desc and authors:
            return "UNSUCCESSFUL"
        return "FULLY_PARSED"
        

    def imageParser(self, url):
        #response = requests.get(url)
        image =None
        try:
            image = Image.open(urllib.request.urlopen(url))
        except:
            pass
        #image.save("here.jpg")
        return image

    def descParser(self, root):
        desc_elements = root.xpath("//td[@class='value-field Sinopse']")[0].text
        #desc= etree.tostring(desc_elements, method='html', with_tail='False')
        # need to decide whther to take all or only the 1st p tag content
        desc=desc_elements
        return desc


    def saleReadyParser(self, root): 
        status = ""
        # Check for the words 'Buy' and 'Pre-Order
        

        return status

    def imageUrlParser(self, root):  
        imgUrl_element = root.xpath("//a[@class='image-zoom']/@href")[0]
        imgUrl = imgUrl_element
        return imgUrl

    def extraParser(self, root):
        return {}
   
    ############# End of Class #################



#def main():
 #   url = "https://www3.livrariacultura.com.br/sapiens-2011667923/p"
   # url = prompt("Enter a url");
  #  content = fetch(url)
    
    #site = LivrariaSite() 
    #site.titleParser(content)
    #site.authorsParser(content)
    #site.isbnParser(content)
    #site.formatParser(content)
    #site.descParser(content)
    #site.subtitleParser(content)
    #site.seriesParser(content)
    #site.volumeParser(content)
    #site.imageUrlParser(content)
    #site.saleReadyParser(content)
  
#def fetch(url):
 #   response = requests.get(url)
  #  return response.content
    








#if __name__ == "__main__":
 #   main()










