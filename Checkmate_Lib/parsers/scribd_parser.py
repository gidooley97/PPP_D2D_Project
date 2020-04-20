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
import json
############ Scribd Site Class ################
"""parses the book data from Scribd"""
class ScribdSite(BookSite):
    def __init__(self):
        self.site_slug = "SC"
        self.search_url = "https://www.scribd.com/search"
        self.url_to_book_detail ="https://www.scribd.com/book"#set to ebook bcs D2D deals with ebooks mainly
        self.match_list=[]
    """
    str -> SiteBookData

    Given a direct link to a book page at a site,
    parse it and return the SiteBookData of the info.
    args:
        url: direct url to a book.
    return:
        book_site_data: a SiteBookData object
    """
    def get_book_data_from_site(self,url):
       return super().get_book_data_from_site(url)

    

    def find_book_matches_at_site(self,site_book_data, formats,pages = 2):
        self.match_list=[]
        search_txt =None
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn_13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        #print('searc',search_txt)
        if not search_txt:
            return []
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        page =1
        url=self.search_url+'?content_type=books&page=1&language=1&query='+search_txt
        content = br.open(url).read() 
        #print('content', content)
        page_count = self.get_page_count_from_js(content)#gets number of pages of results
        #print('page count', page_count)
        while page <= pages and page <= page_count:  #for testing we want to get a few pages
            payload ={'content_type':'books', 'language':'1', 'page':page, 'query':search_txt}
            content = requests.get(self.search_url,params=payload).content
            urls=self.get_urls_js(content)
            page+=1
        self.get_search_book_data_from_page(urls,site_book_data, formats)    
        self.filter_results_by_score(formats)    
        return self.match_list

##################################### Find Matches util methods #################################
    """
    parse the javascript code and returns how many pages of results are there.

    This method parses javascript content of the page to get this info.
    params:
        content: html page of results
    return:
        page_count:number of pages of results
    """
    def get_page_count_from_js(self, content):
        root = super().get_root(url=None, content=content)#given html content returns the root
        js_text=""
        for el in root.xpath(".//script"):
            if el.text is not None:
                js_text+=el.text
        
        dom_txt =js_text

        tmp_txt = dom_txt.split('"page_count":')[1].split(',')[0]
        page_count=int(tmp_txt)
        return page_count
    
    """
    gets the resuts as a json from the json in the javascript of the results page 
        
    params: 
        content: results page content
    return:
        urls: direct urls to book detail pages 
    """ 
    def get_urls_js(self,content):
        root = super().get_root(url=None, content=content)
        try:   
            js_text=""
            for el in root.xpath(".//script"):
                if el.text is not None:
                    js_text+=el.text 
            dom_txt = js_text

            tmp_txt = dom_txt.split('"results":{"books":{"content":{"documents":')[1].split(']')[0]
        
            #print('{"results":'+tmp_txt+"]}")//"results":{"books":{"content":{"documents":
            un_parsed_json='{"results":'+tmp_txt+']}'
            #m=json.dumps(un_parsed_json)
            my_json = json.loads(un_parsed_json)
        
            #only getting results for books
        
            results = my_json["results"]
        
            urls = []
            for r in results:
                urls.append(r["book_preview_url"])
        except:
            return []
        return urls

    
    #passed urls and returns the bookDataSite objects with their scores
    def get_search_book_data_from_page(self, urls, book_site_data_original, formats):
        #print('urls',urls)
        for url in urls:
            #call function to get book data with url
            book_site_data_new= self.get_book_data_from_site(url)
            #book_site_data_new.print_all()

            score = self.match_percentage(book_site_data_original, book_site_data_new) 
            if score >=0.90 and book_site_data_new.format in formats:#found the perfect match
                self.match_list=[]
                book_data_score =tuple([score,book_site_data_new])
                self.match_list.append(book_data_score)
                return 
            book_data_score =tuple([score,book_site_data_new])
            self.match_list.append(book_data_score)
            

    
    def convert_book_id_to_url(self,book_id):
        url = "https://www.scribd.com/book/"+book_id
        return url

    
#---------------------------------------- Utility Methods ---------------------------------------
    
    #override
    def subtitle_parser(self,root):
        return None

    #override
    def book_id_parser(self, url): 
        try:
            book_id = url.split('/')[len(url.split('/'))-2]
        except:
            return None
        return book_id

    #verride
    def isbn_parser(self, root):
        path = self.get_isbn_path()
        try: 
            isbn_element = root.xpath(path)[0]
            isbn = isbn_element
        except:
            isbn = None
        return isbn

    #override
    def image_url_parser(self, root):
        path = self.get_img_url_path()
        try:
            imageUrlParser_element = root.xpath(path)
            imageURL = imageUrlParser_element[0]
        except:
            imageURL = None
        return imageURL

    #override
    def series_parser(self, title):
        series = None
        try:
            for ser in title:
              if ser.isdigit() and ("Series" in title or "series" in title):
                series = ser
                return series
        except:
            series = None
        return series

    #override
    def volume_parser(self, title):
        volume = None
        try:
            for vol in title:
                if vol.isdigit() and ("Volume" in title or "volume" in title):
                    volume = vol
                    return volume
        except:
            volume = None
        return volume
    #override
    def desc_parser(self, root):
        path = self.get_desc_path()
        try:
            desc_element = root.xpath(path)[0]
            desc = desc_element
        except:
            desc = None    
        return desc

    #override
    def format_parser(self, root):
        path = self.get_format_path()
        try: 
            format = super().format_mapper(root.xpath(path)[0])
        except:
            format = None
        return format
    #override
    def sale_ready_parser(self, root):
        saleReady = "Avalaible"
        return saleReady
    
   

#######################################Get XPath Functions####################
    def get_title_path(self):
        return ".//h1[@class='document_title']"
    
    def get_subtitle_path(self):
        return None
    
    def get_authors_path(self):
        return ".//a[contains(@href,'https://www.scribd.com/author')]"

    def get_isbn_path(self):
        return "/html/head/meta[18]/@content"

    def get_format_path(self):
        return "/html/head/meta[13]/@content"

    def get_img_url_path(self):
        return "/html/head/link[5]/@href"

    def get_desc_path(self):
        return "/html/head/meta[16]/@content"

    def get_series_path(self):
        return None   

    def get_volume_path(self):
        return None

    def get_sale_ready_path(self):
        return None
    def get_search_urls_after_search_path(self):
        return  None
