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
import checkmate
from bookSite import BookSite
import re

class GoogleBooks(BookSite):
    def __init__(self):
        self.site_slug = "GB"
        #self.search_url = "https://www.google.com/search?q=&source=lnms&tbm=bks&sa=X&ved=2ahUKEwj10bG89ZDoAhUEnKwKHcC4B-YQ_AUoAXoECBQQCQ&biw=1235&bih=634"
        self.search_url = "https://books.google.com/"
        self.url_to_book_detail = "https://www.books.google.com/book?vid=ISBN"
        self.match_list = []

    """
    str -> SiteBookData

    Given a direct link to a book page at a site,
    parse it and return the SiteBookData of the info.
    args:
        url: direct url to a book.
    return:
        book_site_data: a SiteBookData object
    """
    def get_book_data_from_site(self, url, content=None):
        if url:
            url=url.replace('&printsec=frontcover','')#make sure the link does not take you to the preview page.
            content = requests.get(url).content#special case when the content is passed
        return super().get_book_data_from_site(url,content)

    """
    SiteBookData -> List[Tuple[SiteBookData, float]]
    
    Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
    likely matches paired with how good of a match it is (1.0 is an exact match). 
    This should take into account all the info we have about a book, including the cover.
    Works for kobo and Test Book store. To be overriden by some site site.
    params:
        book_data: a  bookSiteData.
    returns:
        match:List[Tuple[SiteBookData, float]]
    """
    #override
    def find_book_matches_at_site(self, site_book_data, formats=None,pages=2):
        url = self.search_url
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        res= br.open(url)      
        br.select_form(id="oc-search-form")
        search_txt = ''
        if site_book_data.isbn_13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        br['q'] = search_txt

        res = br.submit()
        content = res.read()
        found=self.get_search_book_data_from_page(content,br, site_book_data,formats)
        page=2
        offset =10
        while page<=pages and not found:
            url = 'https://www.google.com/search?tbm=bks&q='+search_txt+'&start='+str(offset)
            res = br.open(url)
            #br.select_form(id="oc-search-form")
            found=self.get_search_book_data_from_page(res.read(), br, site_book_data,formats)
            offset+=10
            page+=1
        self.filter_results_by_score(formats)
        return self.match_list
    """
    returns a list of tuple(score, book_data).

    Some parsers would need to override this method if necessary. For a single page of results, gets 
    urls and gets bookData from the the detail page of the book. 
    Works for Google books only.
    params:
        content: html content of a given page
        book_site_data_original:bookSiteData object. can be null if searching using attr.
       br:browser object to help us handle redirect 
    return: 
        None: 
    """
    #override
    def get_search_book_data_from_page(self, content, br, book_site_data_original, formats):
        root =super().get_root(url=None, content=content)
        url_elements = root.xpath('//a[@class="fuLhoc ZWRArf"]/@href')
        for url in url_elements:
            #book_site_dat_temp = self.get_book_data_from_site(url)
            book_site_dat_temp=self.navigate_to_view_ebook_page(br, url)
            if not book_site_dat_temp:
                continue
            score = self.match_percentage(book_site_data_original, book_site_dat_temp)
            #print('score', score)
            #book_site_dat_temp.print_all()
            if score >=0.90 and book_site_dat_temp.format.lower() in formats:#Perfect match found
                self.match_list=[]
                book_data_score =tuple([score,book_site_dat_temp])
                self.match_list.append(book_data_score)
                return True
            book_data_score = tuple([score,book_site_dat_temp])
            self.match_list.append(book_data_score)
        return False

    """
    goes to the page where book details can be found.

    params:
        br: browser object to help us click links
        url: to be passed to get book details
    """
    def navigate_to_view_ebook_page(self,br, url):
        try:
            res=br.follow_link(text="View eBook")
        except mechanize._mechanize.LinkNotFoundError:
            return self.get_book_data_from_site(url)
                    
        content = res.read()
        return self.get_book_data_from_site(url=None,content=content)
        
    #override
    def convert_book_id_to_url(self, book_id):
        return self.url_to_book_detail+book_id

    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1, site_book2)

###############################################Utility Content Parser  Methods#########################################################################
    #override
    def title_parser(self, root):
        if root.xpath("//h1[@class='booktitle']/span/span"):
            #class website
            title_element = root.xpath("//h1[@class='booktitle']/span/span")[0]
            title = title_element.text
        elif root.xpath("//div[@class='zNLTKd']"):
            #New website
            title_element = root.xpath("//div[@class='zNLTKd']")[0]
            title = title_element.text
        else: 
            title=None
        return title
    
    #override
    def subtitle_parser(self,root):
        if root.xpath("//h1[@class='booktitle']//span[2]//span"):
            #classic website
            subtitle = root.xpath("//h1[@class='booktitle']//span[2]//span")[0].text
        elif root.xpath("//div[@class='Cxh5Uc']"):
            #classic website
            subtitle = root.xpath("//div[@class='Cxh5Uc']")[0].text
        else:
            #New website
            subtitle = None# Fail
        return subtitle
    
    #override
    def authors_parser(self,root):
        authors = []
        try:
            if root.xpath("//div[@class='bookinfo_sectionwrap']/div[1]/a/span"):
                #classic website 
                author_elements = root.xpath("//div[@class='bookinfo_sectionwrap']/div[1]/a/span")
            
                for auth_element in author_elements:
                    authors.append(auth_element.text)
            elif root.path("//div[@class='RQZ6xb']/a"):
                author_elements = root.xpath("//div[@class='RQZ6xb']/a")
                for auth_el in  author_elements:
                    authors.append(auth_el.text)
        except:
            authors = None #Fail
        return authors
    #override
    def book_id_parser(self, url):
        return None
    #override
    def isbn_parser(self, root):
        try:
            if root.xpath("//tr[4]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[4]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[5]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[5]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[6]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[6]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[7]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[7]//td[@class='metadata_value']//span")[0].text
            isbns = str.split(isbn_element)
            return isbns[1]
        except:
            #New 
            return None 

    #override
    def image_url_parser(self, root):
        try:#imple
            imgUrl = root.xpath("//*[@id='summary-frontcover']/@src")[0]
        except:
            imgUrl = None
        return imgUrl

    #override
    def desc_parser(self, root):
        path = self.get_desc_path()
        try:
            desc_element = root.xpath(path)[0]
            desc = desc_element.text
        except:
            desc = None    
        return desc

    #override
    def sale_ready_parser(self, root):
        sale_flag = 0
        status = ""
        try:
            sales_element = root.xpath("//*[@id='gb-get-book-content']")[0].text
            if "print" in sales_element.lower():
                sale_flag = 0
                status = "Find Print"
            elif "ebook" in sales_element.lower():
                status = 0
                status = "Buy Now"
            elif "pre-order" in sales_element.lower():
                sale_flag = 1
                status = "Pre-order"
        except:
            return None
        return status

    
    #override
    def format_parser(self, root):
        fmt = None
        try:
            sales_element = root.xpath("//*[@id='gb-get-book-content']")[0].text
            if "print" in sales_element.lower():
                format = "print"
            elif "ebook" in sales_element.lower():
                format = "ebook"
            elif "pre-order" in sales_element.lower():
                format = "pre-order"
            format=super().format_mapper(format)
        except:
            format=None
        return format

    #method specific to this parser.
    def price_parser(self, root):
        try :
            price = root.xpath("//a[@id='gb-get-book-content']")[0].text
            price = price.split('-')[1].strip()#get only the amount
        except:
            price =None
        return price 

    #override
    def extra_parser(self, root):
        return {"price":self.price_parser(root)}

    #override
    def volume_parser(self, root):
        return None
    #override
    def get_parse_status(self,title, isbn13, desc, authors):
         #determine parse_status checks if we have the most basic data about a book
        if title and isbn13 and authors:
            return "FULLY PARSED"
        if title or isbn13 or desc or authors:
            return "PARTIALLY PARSED"
        return "UNSUCCESSFUL"

        
   

#######################################Get XPath Functions####################
    def get_title_path(self):
        return None
    
    def get_subtitle_path(self):
        return None
    
    def get_authors_path(self):
        return None

    def get_isbn_path(self):
        return None

    def get_format_path(self):
        return None

    def get_img_url_path(self):
        return None

    def get_desc_path(self):
        return "//*[@id='synopsistext']"

    def get_series_path(self):
        return "//td[@class='metadata_value']/a[1]/i/span"   

    def get_volume_path(self):
        return None

    def get_sale_ready_path(self):
        return None
    def get_search_urls_after_search_path(self):
        return  None
