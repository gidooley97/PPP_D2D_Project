from site_book_data import SiteBookData
from bookSite import BookSite
import io
from lxml import etree
import requests
import re
import mechanize
############ TestSite Class ################
"""parses the book data from test bookstore"""
class TestSite(BookSite):
    def __init__(self):
        self.site_slug = "TB"
        self.search_url = "http://127.0.0.1:8000/books/search/"
        self.url_to_book_detail ="http://127.0.0.1:8000/books/"
        self.match_list=[]
     
    def get_book_data_from_site(self,url):
        content = requests.get(url).content
        title = self.titleParser(content)
        author = self.authorsParser(content)
        subtitle = self.subtitleParser(content)
        isbn = self.isbnParser(content)
        frmt = self.formatParser(content)
        description = self.descParser(content)
        series = self.seriesParser(content)
        volume = self.volumeParser(content)
        sale_ready = self.saleReadyParser(content)
        price = self.priceParser(content)
        siteBookData = SiteBookData(content=content, book_title=title, authors=author, subtitle=subtitle, isbn_13=isbn, format=frmt,
         description=description, series=series, volume=volume, ready_for_sale=sale_ready, price=price)
        return siteBookData

        

    def find_book_matches_at_site(self,site_book_data, pages=2):
        url =self.search_url
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(url)  
        #selects the form to populate 
        br.select_form(class_="search-form")
        search_txt =''
        #populate the field. You may need to check if this is actually working
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        br['s_bar'] =search_txt
        
        #submit the form and get the returned page.
        res=br.submit()
        self.__get_book_data_from_page(res.read(), site_book_data)
        page=1
        #return self.match_list # for testing I get the first page results only
        while(page<=pages):
            try:
                res=br.follow_link(text="next")
                self.__get_book_data_from_page(res.read(), site_book_data)
                page+=1
            except mechanize._mechanize.LinkNotFoundError:
                break
        return self.match_list
    def find_book_matches_by_attr_at_site(self,search_txt, pages=2):
        url =self.search_url
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(url)  
        #selects the form to populate 
        br.select_form(class_="search-form")
        if search_txt =='':    
            return []

        br['s_bar'] =search_txt
        
        #submit the form and get the returned page.
        res=br.submit()
        self.__get_book_data_from_page(res.read(), None,False)
        page=1
        #return self.match_list # for testing I get the first page results only
        while(page<=pages):
            try:
                res=br.follow_link(text="next")
                self.__get_book_data_from_page(res.read(), None, False)
                page+=1
            except mechanize._mechanize.LinkNotFoundError:
                break
        return self.match_list

    def __get_book_data_from_page(self, content, book_site_dat_1, is_match=True):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        url_elements = root.xpath(".//button[@class='button button2 text-right']/a/@href")

        for url in url_elements:
            #call function to get book data with url
            url='http://127.0.0.1:8000'+url
            book_site_dat_tmp= self.get_book_data_from_site(url)
            if is_match:
                score = self.match_percentage(book_site_dat_1, book_site_dat_tmp) 
                book_data_score =tuple([score,book_site_dat_tmp])
                self.match_list.append(book_data_score)
            else:
                self.match_list.append(book_site_dat_tmp)

    def convert_book_id_to_url(self,book_id):
        url = self.url_to_book_detail+book_id
        return url

    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1,site_book2)

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
        isbn = root.xpath("/html/body/div[3]/div/div/h6[4]/text()")[0]
        return isbn

    def formatParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        format_type = root.xpath("/html/body/div[3]/div/div/h6[6]/text()")[0]
        return format_type

    def imageParser(self):
        pass

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        try: 
            desc_elements = root.xpath("/html/body/div[3]/div/div/p[@class='indent_this']/text()")[0]
        except IndexError:
            desc_elements = root.xpath("/html/body/div[3]/div/div/p/text()")
            full_desc = ""
            for desc in desc_elements:
                full_desc = full_desc+desc

            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, ' ', full_desc)
            return cleantext
        

        return desc_elements

    def seriesParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        try: 
            series = root.xpath("/html/body/div[3]/div/div/h6[2]/text()")[0]
        except IndexError:
            series = "no series"
        
        return series

    def volumeParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        try: 
            volume = root.xpath("/html/body/div[3]/div/div/h6[3]/text()")[0]
        except IndexError:
            volume = "no volume"
        
        return volume
        

    def saleReadyParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        saleReady = root.xpath("/html/body/div[3]/div/div/p[@style='color: red;' or @style='color: green;']/text()")[0]
        return saleReady

    def priceParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        price = root.xpath("/html/body/div[3]/div/div/h6[1]/text()")[0]
        return price

    def extraParser(self):
        pass

    def imageUrlParser(self):
        pass


############# End of Class #################



def main():

    url = "http://127.0.0.1:8000/books/30/"
    BookSite = TestSite()
    content = fetch(url)
    #print(BookSite.formatParser(content))
    #BookSite.parseAll(content)
    BookSite.get_book_data_from_site(url).print_all()
    print(BookSite.find_matches_at_site(BookSite.get_book_data_from_site(url)))

    
    
    

  
def fetch(url):
    response = requests.get(url)
    return response.content

if __name__ == "__main__":
    main()
