from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from PIL import Image
from io import BytesIO
import urllib.request
from bookSite import BookSite
import mechanize
from bs4 import BeautifulSoup
import urllib

############ AudioBookSite Class ################
"""parses the book data from AudioBook"""
class AudioBookSite(BookSite):

    def __init__(self):
        super().__init__()
        self.search_url="https://www.audiobooks.com/search/book/"
        self.url_to_book_detail ="https://www.audiobooks.com/audiobook/"
        self.site_slug = 'AU'

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

    
    """
    SiteBookData -> List[Tuple[SiteBookData, float]]
    
    Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
    likely matches paired with how good of a match it is (1.0 is an exact match). 
    This should take into account all the info we have about a book, including the cover.
    Different for every site. To be overriden by every site.
    params:
        book_data: a  bookSiteData.
    returns:
        match:List[Tuple[SiteBookData, float]]
    """
    #override
    def find_book_matches_at_site(self,site_book_data, pages=2):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        search_txt =''
        #populate the field. You may need to check if this is actually working
        if site_book_data.isbn_13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []

        url = "https://www.audiobooks.com/search/book/"+search_txt
        self.match_list=[]
        print(url)
        res=br.open(url)
        content = res.read()
        found = self.get_search_book_data_from_page(content, site_book_data)#get page 1 of results
        #return self.match_list # for testing I get the first page results only
        page=2
        while page <=pages and not found:#limit the results we will get
            try:
                res= br.open(url+'/page/'+str(page))
                found=self.get_search_book_data_from_page(res.read(), site_book_data)
                page+=1
            except mechanize._mechanize.LinkNotFoundError:#end of results
                break
        return self.match_list

    """
    returns a list of tuple(score, book_data).

    Some parsers would need to override this method if necessary. For a single page of results, gets 
    urls and gets bookData from the the detail page of the book. 
    Works mainly for Kobo and TestBookStore.
    params:
        content: html content of a given page
        book_site_data_original:bookSiteData object. can be null if searching using attr.
       
    return: 
        None: 
    """
    def get_search_book_data_from_page(self, content,  book_site_data_original):
        root = self.get_root(url=None, content=content)#force this method to work with content
        #expects a path that will help us get the urls
        url_elements = root.xpath(self.get_search_urls_after_search_path())
        # print('urls', url_elements)
        if len(url_elements)==0:
            self.match_list.append(tuple([1.00,super().get_book_data_from_site(url=None, content=content)]))
            return True
        for url in url_elements:
            # print('url', url)
            book_site_data_new= self.get_book_data_from_site(url)
            #book_site_dat_tmp.print_all()
            score = self.match_percentage(book_site_data_original, book_site_data_new) 
            book_data_score =tuple([score,book_site_data_new])
            self.match_list.append(book_data_score)
            self.filter_results_by_score()
        return False
       
   
    """
    Given a book_id, return the direct url for the book.
    To be overriden by all sites.
    params:
        book_id: the book unique identifier.
    return:
        url:direct url to the book. 
    """
    #override
    def convert_book_id_to_url(self,book_id):
        return self.url_to_book_detail+book_id
################################# Get Xpath Methods########################################
    #override
    def get_search_urls_after_search_path(self):
        return  "//div[@class='browseContainer__bookItem flexer']/a/@href"
    #override
    def get_title_path(self):
        return "//h1[@class='audiobookTitle']"
    #override
    def get_subtitle_path(self):
        return None
    #override
    def get_authors_path(self):
        return None
    #override
    def get_isbn_path(self):
        return None
    #override
    def get_format_path(self):
        return None
    #override
    def get_img_url_path(self):
        return "//div[@class='book-details-sidenav']/img/@src"
    #override
    def get_desc_path(self):
        return "//div[@class='book-description']"
    #override
    def get_series_path(self):
        return None
    #override
    def get_volume_path(self):
        return None 
    #override
    def get_sale_ready_path(self):
        return None
###############################################################################################################
#---------------------------------------- Get Content Methods ---------------------------------------
    #override
    def authors_parser(self,root):
        path = "//h4[@class='book-written-by']/span/span"
        try: 
            authors=[]
            count=1
            while True:
                
                if root.xpath(path+'['+str(count)+']'):
                    auth= root.xpath(path+'['+str(count)+']/a')[0].text
                    authors.append(auth)
                    count+=1
                    continue
                else:
                    break
        except:
            authors = None #Fail
        return authors

    #override 
    def subtitle_parser(self,root):
        return None

    #override
    def isbn_parser(self, root):
        return None

    #override
    def format_parser(self, root):
        return "Audiobook"

    #override
    def image_url_parser(self, root):
        path = self.get_img_url_path()
        try:
            imgUrl_element = root.xpath(path)[0] 
            imgUrl = "http:" + imgUrl_element
        except:
            imgUrl = None
        return imgUrl
    
     #override
    def desc_parser(self, root):
        path = self.get_desc_path()
        try:
            desc_element_list = root.xpath(path)[0]
            xmlstr = etree.tostring(desc_element_list, encoding='utf8', method='xml')  
            desc = BeautifulSoup(xmlstr,features="lxml") 
        except:
            desc = None    
        return desc.get_text()
    #override
    def series_parser(self, root):
        series = None
        try:
            for ser in title:
              if ser.isdigit() and ("Series" in title or "series" in title):
                series = ser
                return series
        except:
            series =None
        return series  
    #override
    def book_id_parser(self, url):
        try:
            arr = url.split('/')
            book_id  =arr[len(url.split('/'))-2]+'/'+arr[len(url.split('/'))-1]
        except:
            book_id=None
        return book_id 
    #override
    def extra_parser(self, root):
        return {"Narrators":self.narrators_parser(root)}
    #extra content for audiobooks
    def narrators_parser(self,root):
        path = "//h4[@class='book-narrated-by']/span/span"
        try: 
            narrators = []
            count=1
            while True:
                
                if root.xpath(path+'['+str(count)+']'):
                    narrator= root.xpath(path+'['+str(count)+']/a')[0].text
                    narrators.append(narrator)
                    count+=1
                    continue
                else:
                    break
        except:
            narrators = None #Fail
        return narrators
        
#--------------------------------------------------------------------------------------------------------------#
